import React from 'react';
import { ItinerarySolution } from '../lib/api';

interface ItineraryCardProps {
    solution: ItinerarySolution;
    rank: number;
}

export default function ItineraryCard({ solution, rank }: ItineraryCardProps) {
    const formatMoney = (val: number) => {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
    };

    const formatDuration = (mins: number) => {
        const hours = Math.floor(mins / 60);
        const m = Math.round(mins % 60);
        return `${hours}h ${m}m`;
    };

    return (
        <div className="border border-gray-200 rounded-lg p-4 mb-4 shadow-sm hover:shadow-md transition-shadow bg-white">
            <div className="flex justify-between items-center mb-3">
                <h3 className="text-lg font-bold text-blue-600">Opção #{rank}</h3>
                <div className="text-right">
                    <p className="text-xl font-bold text-green-600">{formatMoney(solution.total_cost)}</p>
                    <p className="text-sm text-gray-500">{formatDuration(solution.total_duration_minutes)} total</p>
                </div>
            </div>

            <div className="space-y-4">
                <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Deslocamentos</h4>
                    {solution.legs_breakdown.map((leg, idx) => (
                        <div key={idx} className="bg-gray-50 p-2 rounded text-sm mb-1 flex justify-between">
                            <span>{leg.type === 'flight' ? '✈️' : '🚗'} {leg.origin} → {leg.destination}</span>
                            <span className="font-mono">{formatMoney(leg.cost)}</span>
                        </div>
                    ))}
                </div>

                <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Hospedagem</h4>
                    {solution.stays_breakdown.map((stay, idx) => (
                        <div key={idx} className="bg-gray-50 p-2 rounded text-sm mb-1 flex justify-between">
                            <span>🏨 {stay.name} ({stay.location})</span>
                            <span className="font-mono">{formatMoney(stay.cost_per_night)}/noite</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
