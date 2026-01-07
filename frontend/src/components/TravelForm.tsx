import React, { useState } from 'react';
import { TripRequest, StopRequest } from '../lib/api';
import AutocompleteInput from './AutocompleteInput';

interface TravelFormProps {
    onSearch: (request: TripRequest) => void;
    isLoading: boolean;
}

// Reuse or adapt interface
interface ApiAirport {
    iata: string;
    name: string;
    city: string;
    country: string;
}

export default function TravelForm({ onSearch, isLoading }: TravelFormProps) {
    // State for IATA codes (sent to API)
    const [originIata, setOriginIata] = useState('');
    const [destinationIata, setDestinationIata] = useState('');

    // State for Display text (shown in Input)
    const [originDisplay, setOriginDisplay] = useState('');
    const [destinationDisplay, setDestinationDisplay] = useState('');

    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [travelers, setTravelers] = useState(1);
    const [stops, setStops] = useState<StopRequest[]>([]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!originIata || !destinationIata || !startDate || !endDate) {
            alert("Preencha os campos obrigatórios e selecione aeroportos válidos da lista.");
            return;
        }

        const request: TripRequest = {
            origin: { iata_code: originIata },
            destination: { iata_code: destinationIata },
            start_date_min: startDate,
            end_date_max: endDate,
            travelers: Number(travelers),
            sort_preference: 'cost_benefit',
            stops: stops
        };
        onSearch(request);
    };

    // Helper to handle selection
    const handleOriginSelect = (airport: ApiAirport) => {
        setOriginIata(airport.iata);
        setOriginDisplay(`${airport.city}, ${airport.country} (${airport.iata})`);
    };

    const handleDestinationSelect = (airport: ApiAirport) => {
        setDestinationIata(airport.iata);
        setDestinationDisplay(`${airport.city}, ${airport.country} (${airport.iata})`);
    };

    // Helper for stops (simplified for now, stops might needed similar refactor if they want rich display too)
    // For now we keep stops simple or refactor later
    const addStop = () => {
        setStops([...stops, { location: { iata_code: '' }, min_days: 2 }]);
    };

    const updateStop = (idx: number, field: string, value: string | number) => {
        const newStops = [...stops];
        if (field === 'iata') newStops[idx].location.iata_code = String(value);
        if (field === 'days') newStops[idx].min_days = Number(value);
        setStops(newStops);
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md max-w-2xl mx-auto">
            <h2 className="text-xl font-bold mb-4">Planeje sua Viagem</h2>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <AutocompleteInput
                        label="Origem"
                        value={originDisplay}
                        onChange={setOriginDisplay}
                        onSelect={handleOriginSelect}
                        placeholder="Cidade ou Aeroporto"
                    />
                </div>
                <div>
                    <AutocompleteInput
                        label="Destino"
                        value={destinationDisplay}
                        onChange={setDestinationDisplay}
                        onSelect={handleDestinationSelect}
                        placeholder="Cidade ou Aeroporto"
                    />
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Início Mínimo</label>
                    <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)}
                        className="w-full border rounded p-2" />
                </div>
                <div>
                    <label className="block text-sm font-medium mb-1">Fim Máximo</label>
                    <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)}
                        className="w-full border rounded p-2" />
                </div>
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium mb-1">Viajantes</label>
                <input type="number" value={travelers} onChange={(e) => setTravelers(Number(e.target.value))}
                    className="w-full border rounded p-2" min={1} max={10} />
            </div>

            {stops.length > 0 && (
                <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Paradas Intermediárias</label>
                    {stops.map((stop, idx) => (
                        <div key={idx} className="flex gap-2 mb-2">
                            <div className="w-48">
                                <AutocompleteInput
                                    label=""
                                    value={stop.location.iata_code}
                                    onChange={(val) => updateStop(idx, 'iata', val)}
                                    placeholder="IATA"
                                    maxLength={3}
                                />
                            </div>
                            <input type="number" value={stop.min_days} onChange={(e) => updateStop(idx, 'days', e.target.value)}
                                className="w-20 border rounded p-2" placeholder="Dias" min={1} />
                        </div>
                    ))}
                </div>
            )}

            <div className="flex justify-between items-center">
                <button type="button" onClick={addStop} className="text-blue-600 text-sm hover:underline">
                    + Adicionar Parada
                </button>
                <button type="submit" disabled={isLoading}
                    className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
                    {isLoading ? 'Otimizando...' : 'Buscar Minha Viagem'}
                </button>
            </div>
        </form>
    );
}
