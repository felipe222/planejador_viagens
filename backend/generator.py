from typing import List
from datetime import date
import itertools
from models import TripRequest, Leg, Stay, SolverInput
from scraper import Scraper

class Generator:
    def __init__(self, scraper: Scraper):
        self.scraper = scraper

    def generate_scenario(self, request: TripRequest) -> SolverInput:
        # Simplificação: Por enquanto, assumir um caminho linear baseado na ordem das paradas se fornecido, 
        # ou permutação simplificada, se necessário. 
        # O requisito do usuário diz "Gera combinacoes (ordens) para as localidades flexiveis."
        
        # Esta versão básica assume uma ordem fixa por enquanto para fazer o E2E funcionar, 
        # ou captura a ordem da solicitação.
        
        stops = request.stops
        # Início: Origem -> Parada 1 -> Parada 2 ... -> Parada N -> Destino
        # Se o destino for separado. Na verdade, a solicitação tem Origem e Destino.
        
        legs = []
        stays = []
        
        current_loc = request.origin.iata_code
        current_date = request.start_date_min # Suposição de data simplificada
        
        # Iterar pelas paradas para construir trechos e estadias
        for i, stop in enumerate(stops):
            next_loc = stop.location.iata_code
            
            # Trecho do atual para o próximo
            leg_id = f"leg_{i}"
            transport_opts = self.scraper.get_transport_options(current_loc, next_loc, current_date)
            legs.append(Leg(id=leg_id, origin=current_loc, destination=next_loc, options=transport_opts))
            
            # Estada no próximo
            stay_id = f"stay_{i}"
            # Para fins de mock, apenas pegue uma janela. A lógica real precisa de mais flexibilidade de data.
            # Vamos buscar opções para um intervalo de datas genérico ou com base em min_days.
            # No Solucionador, otimizamos QUAIS datas específicas. Aqui pegamos TODAS as opções potenciais.
            # Mas o Scraper precisa de datas.
            # Hack: Obter opções para a janela "provável".
            checkin_guess = current_date
            checkout_guess = date.fromordinal(current_date.toordinal() + stop.min_days)
            
            accom_opts = self.scraper.get_accommodation_options(next_loc, checkin_guess, checkout_guess)
            stays.append(Stay(id=stay_id, location=next_loc, min_nights=stop.min_days, options=accom_opts))
            
            current_loc = next_loc
            current_date = checkout_guess
            
        # Trecho Final: Última Parada -> Destino
        if current_loc != request.destination.iata_code:
            leg_id = f"leg_final"
            transport_opts = self.scraper.get_transport_options(current_loc, request.destination.iata_code, current_date)
            legs.append(Leg(id=leg_id, origin=current_loc, destination=request.destination.iata_code, options=transport_opts))

        return SolverInput(legs=legs, stays=stays, config={"travelers": request.travelers})
