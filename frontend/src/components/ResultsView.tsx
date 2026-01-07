import React from 'react';
import { OptimizationResult } from '../lib/api';
import ItineraryCard from './ItineraryCard';

interface ResultsViewProps {
    result: OptimizationResult;
}

export default function ResultsView({ result }: ResultsViewProps) {
    if (!result || !result.solutions || result.solutions.length === 0) {
        return <div className="p-4 text-center text-gray-500">Nenhuma solução encontrada.</div>;
    }

    return (
        <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Melhores Opções Encontradas</h2>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {result.solutions.map((sol, idx) => (
                    <ItineraryCard key={idx} solution={sol} rank={idx + 1} />
                ))}
            </div>
        </div>
    );
}
