import os

# Configurações do Scraper
# Modos: "mock" (padrão), "live"
SCRAPER_MODE = os.getenv("SCRAPER_MODE", "mock")
KAYAK_BASE_URL = "https://www.kayak.com.br"

# Configurações de Otimização
DEFAULT_MAX_ITEMS = 50  # Máximo de itens a considerar por trecho/estadia
GAP_FILL_DAYS = 2       # Dias a adicionar para preenchimento de lacunas, se necessário

# Configurações do NSGA-II
POPULATION_SIZE = 50
GENERATIONS = 20
MUTATION_RATE = 0.1

# Fatores de Custo (Aproximações para Mock)
FLIGHT_COST_PER_KM = 0.5   # R$/km
DRIVE_COST_PER_KM = 1.2    # R$/km (Combustível + Desgaste)
HOTEL_AVG_COST = 350.0     # R$/night

# Limites de Condução
MAX_DRIVE_DISTANCE_KM = 800
DRIVE_SPEED_KMH = 80
