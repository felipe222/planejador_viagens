from pydantic import BaseModel
from typing import List, Optional, Literal, Dict
from datetime import date

# --- Modelos de Entrada ---

class Location(BaseModel):
    iata_code: str # e.g., GRU, CDG
    name: Optional[str] = None

class TripRequest(BaseModel):
    origin: Location
    destination: Location
    start_date_min: date
    end_date_max: date
    stops: List['StopRequest']
    travelers: int = 1
    sort_preference: Literal["price", "duration", "cost_benefit"] = "cost_benefit"

class StopRequest(BaseModel):
    location: Location
    min_days: int = 1
    max_days: Optional[int] = None
    fixed_dates: Optional[List[date]] = None

TripRequest.model_rebuild()

# --- Entidades Principais ---

class TransportOption(BaseModel):
    id: str
    type: Literal["flight", "car", "mixed"] 
    origin: str
    destination: str
    departure_time: str # formato ISO
    arrival_time: str   # formato ISO
    duration_minutes: int
    cost: float
    distance_km: Optional[float] = None
    details: Dict = {} # Número de voo, locadora de veículos, etc.

class AccommodationOption(BaseModel):
    id: str
    location: str
    name: str
    cost_per_night: float
    rating: Optional[float] = None
    details: Dict = {} # Endereço, amenidades

class Leg(BaseModel):
    id: str
    origin: str
    destination: str
    options: List[TransportOption] = []

class Stay(BaseModel):
    id: str
    location: str
    min_nights: int
    options: List[AccommodationOption] = []

# --- Entrada/Saída do Solucionador ---

class SolverInput(BaseModel):
    legs: List[Leg]
    stays: List[Stay]
    config: Dict = {}

class SelectedOption(BaseModel):
    leg_id: Optional[str] = None
    stay_id: Optional[str] = None
    option_id: str
    type: Literal["transport", "accommodation"]
    cost: float
    details: Dict = {}

class ItinerarySolution(BaseModel):
    total_cost: float
    total_duration_minutes: float
    selections: List[SelectedOption]
    legs_breakdown: List[Dict] # Detalhamento descritivo
    stays_breakdown: List[Dict]

class OptimizationResult(BaseModel):
    solutions: List[ItinerarySolution]
    metadata: Dict = {}
