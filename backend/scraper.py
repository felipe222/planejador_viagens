import random
from typing import List
from datetime import date, timedelta, datetime
from models import TransportOption, AccommodationOption, Location
import config

import json
import os

import math

class Scraper:
    def __init__(self, mode: str = config.SCRAPER_MODE):
        self.mode = mode
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.hotels_data = self._load_json('hoteis.json')
        self.cars_data = self._load_json('aluguel_carros.json')
        self.distances_data = self._load_json('distancias_carro.json')
        self.cities_data = self._load_json('cidades.json')
        self.flights_data = self._load_json('voos.json')
        
    def _load_json(self, filename: str):
        try:
            path = os.path.join(self.data_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
        return []

    def get_transport_options(self, origin: str, destination: str, travel_date: date) -> List[TransportOption]:
        if self.mode == "mock":
            return self._mock_transport(origin, destination, travel_date)
        else:
            return []

    def get_accommodation_options(self, location: str, checkin: date, checkout: date) -> List[AccommodationOption]:
        if self.mode == "mock":
            return self._mock_accommodation(location, checkin, checkout)
        else:
            return []

    def _mock_transport(self, origin: str, destination: str, travel_date: date) -> List[TransportOption]:
        options = []
        
        # Verificar se existe voo no JSON (Rota Direta)
        flight_entry = next((f for f in self.flights_data if f['origem_id'] == origin and f['destino_id'] == destination), None)
        
        # Se tiver voo no JSON, usa o preço dele. Se não, gera aleatório (fallback)
        base_cost = float(flight_entry['custo_voo_pessoa']) if flight_entry else None
        
        # Gera opções de horário (simulação)
        num_flights = random.randint(2, 5) if not flight_entry else random.randint(1, 3) # Menos voos se for dado específico? Ou mantem simulação de horários
        
        for i in range(num_flights):
            dep_hour = random.randint(6, 22)
            dur_mins = random.randint(60, 600)
            
            # Se temos preço fixo, variamos pouco (ex: classe, horário). Se não, aleatório completo
            if base_cost is not None:
                cost = base_cost * random.uniform(0.9, 1.2) # Pequena variação
            else:
                cost = random.randint(200, 2000)
            
            dep_dt = datetime.combine(travel_date, datetime.min.time().replace(hour=dep_hour))
            arr_dt = dep_dt + timedelta(minutes=dur_mins)

            options.append(TransportOption(
                id=f"flight_{origin}_{destination}_{i}",
                type="flight",
                origin=origin,
                destination=destination,
                departure_time=dep_dt.isoformat(),
                arrival_time=arr_dt.isoformat(),
                duration_minutes=dur_mins,
                cost=float(cost),
                details={
                    "airline": f"MockAir {i}", 
                    "flight_number": f"MA{random.randint(100,999)}",
                    "source": "JSON Data" if base_cost else "Random Mock"
                }
            ))

        # Integração Real de Carros e Distâncias
        dist_entry = next((d for d in self.distances_data if (d['origem_id'] == origin and d['destino_id'] == destination) or (d['origem_id'] == destination and d['destino_id'] == origin)), None)
        
        if dist_entry:
            distance_km = dist_entry['distancia_km']
            # Custo: Combustível/Desgaste (R$ 1.2/km) + Diária Média de Locação (Simplificação)
            # Para ser mais preciso, deveríamos pegar a locadora do 'origin', mas simplificaremos
            rental_cost_avg = 120.0 
            
            # Buscar locadora na origem
            rental_entry = next((c for c in self.cars_data if c['cidade_id'] == origin), None)
            if rental_entry:
                 rental_cost_avg = rental_entry['custo_diaria']
            
            drive_hours = distance_km / config.DRIVE_SPEED_KMH
            drive_mins = int(drive_hours * 60)
            
            # Custo total estimado: (Distância * Custo/km) + (Horas / 24 * Diária ... ou apenas 1 diária por trecho)
            # Vamos assumir 1 diária para o deslocamento
            cost = (distance_km * config.DRIVE_COST_PER_KM) + rental_cost_avg
            
            dep_dt = datetime.combine(travel_date, datetime.min.time().replace(hour=9))
            arr_dt = dep_dt + timedelta(minutes=drive_mins)
            
            options.append(TransportOption(
                id=f"car_{origin}_{destination}_real",
                type="car",
                origin=origin,
                destination=destination,
                departure_time=dep_dt.isoformat(),
                arrival_time=arr_dt.isoformat(),
                duration_minutes=drive_mins,
                cost=cost,
                distance_km=float(distance_km),
                details={"company": rental_entry['nome'] if rental_entry else "Local Rent a Car", "car_type": "Standard"}
            ))

        elif origin != destination: # Fallback se não houver dados carregados
            distance_km = 0
            # Tentar calcular via Haversine se tivermos coords
            city_origin = next((c for c in self.cities_data if c['id'] == origin), None)
            city_dest = next((c for c in self.cities_data if c['id'] == destination), None)

            if city_origin and city_dest:
                 distance_km = self._calculate_haversine(city_origin['lat'], city_origin['lon'], city_dest['lat'], city_dest['lon'])
            else:
                 # Último recurso: aleatório (mantido para robustez)
                 distance_km = random.randint(100, 800)

            drive_hours = distance_km / config.DRIVE_SPEED_KMH
            drive_mins = int(drive_hours * 60)
            cost = distance_km * config.DRIVE_COST_PER_KM
            
            dep_dt = datetime.combine(travel_date, datetime.min.time().replace(hour=9))
            arr_dt = dep_dt + timedelta(minutes=drive_mins)

            options.append(TransportOption(
                id=f"car_{origin}_{destination}",
                type="car",
                origin=origin,
                destination=destination,
                departure_time=dep_dt.isoformat(),
                arrival_time=arr_dt.isoformat(),
                duration_minutes=drive_mins,
                cost=cost,
                distance_km=float(distance_km),
                details={"company": "MockRental", "car_type": "Sedan", "calculation": "Haversine/Estimated"}
            ))

        return options

    def _calculate_haversine(self, lat1, lon1, lat2, lon2):
        R = 6371  # Raio da Terra em km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def _mock_accommodation(self, location: str, checkin: date, checkout: date) -> List[AccommodationOption]:
        options = []
        nights = (checkout - checkin).days
        if nights < 1: nights = 1

        # Integração Real de Hotéis
        city_hotels = [h for h in self.hotels_data if h['cidade_id'] == location]
        
        if city_hotels:
            for h in city_hotels:
                total_cost = h['custo_diaria'] * nights
                options.append(AccommodationOption(
                    id=f"hotel_{location}_{h['nome'].replace(' ', '_')}",
                    location=location,
                    name=h['nome'],
                    cost_per_night=float(h['custo_diaria']),
                    rating=4.5, # Dado não disponível no JSON, assumindo padrão
                    details={"source": "External Data"}
                ))
        else:
            # Fallback
            for i in range(random.randint(3, 8)):
                cost_night = random.randint(150, 800)
                options.append(AccommodationOption(
                    id=f"hotel_{location}_{i}",
                    location=location,
                    name=f"Hotel Mock {location} {i}",
                    cost_per_night=float(cost_night),
                    rating=random.uniform(3.0, 5.0),
                    details={"address": "123 Mock St"}
                ))
        return options
