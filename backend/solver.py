import random
from typing import List, Tuple
from models import SolverInput, ItinerarySolution, SelectedOption, TransportOption, AccommodationOption
import config

class Solver:
    def __init__(self, input_data: SolverInput):
        self.input = input_data
        self.population_size = config.POPULATION_SIZE
        self.generations = config.GENERATIONS
        self.mutation_rate = config.MUTATION_RATE

    def solve(self) -> List[ItinerarySolution]:
        # Algoritmo Genético Simples para Multi-Objetivo (lógica NSGA-II aproximada)
        population = self._initialize_population()
        
        for gen in range(self.generations):
            offspring = self._crossover_and_mutation(population)
            population = self._selection(population + offspring)
            
        # Converter melhores indivíduos para soluções
        solutions = [self._decode_individual(ind) for ind in population]
        # Remover duplicatas
        unique_solutions = []
        seen = set()
        for sol in solutions:
            key = (sol.total_cost, sol.total_duration_minutes)
            if key not in seen:
                seen.add(key)
                unique_solutions.append(sol)
        
        # Ordenar por custo primariamente
        return unique_solutions[:20] # Retornar top 20

    def _initialize_population(self):
        population = []
        for _ in range(self.population_size):
            genome = self._random_genome()
            if self._is_valid(genome):
                population.append(genome)
        return population

    def _random_genome(self):
        # Um genoma é um dicionário de {leg_index: option_index, stay_index: option_index}
        genome = {}
        for i, leg in enumerate(self.input.legs):
            if leg.options:
                genome[f"leg_{i}"] = random.randint(0, len(leg.options) - 1)
            else:
                genome[f"leg_{i}"] = -1 # Inválido
        
        for i, stay in enumerate(self.input.stays):
            if stay.options:
                genome[f"stay_{i}"] = random.randint(0, len(stay.options) - 1)
            else:
                genome[f"stay_{i}"] = -1
        return genome

    def _is_valid(self, genome):
        # Verificar se todas as seleções são índices válidos
        for k, v in genome.items():
            if v == -1: return False
        return True

    def _evaluate(self, genome):
        # Calcular Objetivos: Z1 (Custo), Z2 (Duração)
        total_cost = 0.0
        total_duration = 0.0
        
        # Custos de Trecho (Transporte)
        for i, leg in enumerate(self.input.legs):
            opt_idx = genome[f"leg_{i}"]
            option = leg.options[opt_idx]
            
            # Mapeamento de Lógica MILP:
            # Voo: Custo é preço do bilhete * viajantes
            # Carro: Custo geralmente é por veículo, mas vamos verificar config.
            # Misto: Não modelado diretamente aqui a menos que o Scraper combine.
            # Assumindo que Scraper retorna opções "Mistas" se existirem, ou lidamos com tipos simples.
            
            travelers = self.input.config.get("travelers", 1)
            
            if option.type == "flight":
                total_cost += option.cost * travelers
            elif option.type == "car":
                # Aluguel de carro geralmente é por dia/viagem, não por pessoa.
                # Mas combustível é por carro.
                total_cost += option.cost 
            
            total_duration += option.duration_minutes

        # Custos de Estada (Acomodação)
        for i, stay in enumerate(self.input.stays):
            opt_idx = genome[f"stay_{i}"]
            option = stay.options[opt_idx]
            # Custo por noite * noites * quartos?
            # Assumindo cost_per_night total para o grupo ou precisamos de quartos.
            # Simplificado: Custo por noite * min_nights
            total_cost += option.cost_per_night * stay.min_nights
            
        return total_cost, total_duration

    def _crossover_and_mutation(self, population):
        offspring = []
        while len(offspring) < self.population_size:
            p1 = random.choice(population)
            p2 = random.choice(population)
            child = p1.copy()
            
            # Cruzamento (Crossover)
            cut = random.randint(0, len(child))
            keys = list(child.keys())
            for k in keys[cut:]:
                child[k] = p2[k]
                
            # Mutação
            if random.random() < self.mutation_rate:
                gene_to_mutate = random.choice(keys)
                # Encontrar max de opções para este gene
                parts = gene_to_mutate.split("_")
                idx = int(parts[1])
                if parts[0] == "leg":
                    opts_len = len(self.input.legs[idx].options)
                else:
                    opts_len = len(self.input.stays[idx].options)
                
                if opts_len > 0:
                    child[gene_to_mutate] = random.randint(0, opts_len - 1)
            
            if self._is_valid(child):
                offspring.append(child)
        return offspring

    def _selection(self, population):
        # Ordenação não dominada (simplificada)
        evaluated = [(ind, self._evaluate(ind)) for ind in population]
        # Fronteiras de Pareto
        # Dominação: A domina B se A.custo <= B.custo E A.dur <= B.dur E (A.custo < B.custo OU A.dur < B.dur)
        
        # Torneio Simples por enquanto para velocidade e robustez no Mock
        selected = []
        while len(selected) < self.population_size:
            a = random.choice(evaluated)
            b = random.choice(evaluated)
            
            # Preferir dominante
            if self._dominates(a[1], b[1]):
                selected.append(a[0])
            elif self._dominates(b[1], a[1]):
                selected.append(b[0])
            else:
                # Desempate aleatório
                selected.append(a[0])
                
        return selected

    def _dominates(self, obj_a, obj_b):
        # obj_a = (cost, dur)
        return (obj_a[0] <= obj_b[0] and obj_a[1] <= obj_b[1]) and (obj_a[0] < obj_b[0] or obj_a[1] < obj_b[1])

    def _decode_individual(self, genome) -> ItinerarySolution:
        selections = []
        legs_desc = []
        stays_desc = []
        
        total_cost, total_duration = self._evaluate(genome)
        
        for i, leg in enumerate(self.input.legs):
            opt_idx = genome[f"leg_{i}"]
            option = leg.options[opt_idx]
            selections.append(SelectedOption(
                leg_id=leg.id,
                option_id=option.id,
                type="transport",
                cost=option.cost
            ))
            legs_desc.append(option.model_dump())
            
        for i, stay in enumerate(self.input.stays):
            opt_idx = genome[f"stay_{i}"]
            option = stay.options[opt_idx]
            selections.append(SelectedOption(
                stay_id=stay.id,
                option_id=option.id,
                type="accommodation",
                cost=option.cost_per_night * stay.min_nights
            ))
            stays_desc.append(option.model_dump())

        return ItinerarySolution(
            total_cost=total_cost,
            total_duration_minutes=total_duration,
            selections=selections,
            legs_breakdown=legs_desc,
            stays_breakdown=stays_desc
        )
