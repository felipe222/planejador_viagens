import requests
from datetime import date, timedelta
import json

def test_optimize():
    url = "http://localhost:8001/optimize"
    
    # Carga útil (Payload)
    today = date.today()
    payload = {
        "origin": {"iata_code": "GRU", "name": "Sao Paulo"},
        "destination": {"iata_code": "CDG", "name": "Paris"},
        "start_date_min": (today + timedelta(days=30)).isoformat(),
        "end_date_max": (today + timedelta(days=45)).isoformat(),
        "stops": [
            {
                "location": {"iata_code": "LIS", "name": "Lisbon"},
                "min_days": 3
            }
        ],
        "travelers": 2,
        "sort_preference": "cost_benefit"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        result = response.json()
        print(f"DEBUG: Status Code: {response.status_code}")
        print(f"DEBUG: Response Headers: {response.headers}")
        print("Sucesso! Soluções encontradas:", len(result["solutions"]))
        if result["solutions"]:
            best = result["solutions"][0]
            print("Custo da Melhor Solução:", best["total_cost"])
            print("Duração da Melhor Solução:", best["total_duration_minutes"])
            print("DEBUG: Detalhes da Melhor Solução:", json.dumps(best, indent=2))
    except Exception as e:
        print(f"Erro: {e}")
        if 'response' in locals():
            print(response.text)

if __name__ == "__main__":
    test_optimize()
