const API_BASE_URL = 'http://localhost:8001';

export interface Location {
  iata_code: string;
  name?: string;
}

export interface StopRequest {
  location: Location;
  min_days: number;
}

export interface TripRequest {
  origin: Location;
  destination: Location;
  start_date_min: string;
  end_date_max: string;
  stops: StopRequest[];
  travelers: number;
  sort_preference: 'price' | 'duration' | 'cost_benefit';
}

export interface LegBreakdown {
  type: string;
  origin: string;
  destination: string;
  cost: number;
  duration_minutes: number;
  [key: string]: unknown;
}

export interface StayBreakdown {
  name: string;
  location: string;
  cost_per_night: number;
  [key: string]: unknown;
}

export interface SelectedOption {
  leg_id?: string;
  stay_id?: string;
  option_id: string;
  type: 'transport' | 'accommodation';
  cost: number;
  details: Record<string, unknown>;
}

export interface ItinerarySolution {
  total_cost: number;
  total_duration_minutes: number;
  selections: SelectedOption[];
  legs_breakdown: LegBreakdown[];
  stays_breakdown: StayBreakdown[];
}

export interface OptimizationResult {
  solutions: ItinerarySolution[];
  metadata: Record<string, unknown>;
}

export async function optimizeTrip(request: TripRequest): Promise<OptimizationResult> {
  const response = await fetch(`${API_BASE_URL}/optimize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}
