'use client';

import React, { useState } from 'react';
import TravelForm from '@/components/TravelForm';
import ResultsView from '@/components/ResultsView';
import { TripRequest, optimizeTrip, OptimizationResult } from '@/lib/api';

export default function Home() {
  const [result, setResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (request: TripRequest) => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await optimizeTrip(request);
      setResult(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Erro ao buscar opções de viagem.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-extrabold text-blue-700 mb-2">✈️ Planejador de Viagens IA</h1>
          <p className="text-gray-600">Otimização multiobjetivo para viagens complexas.</p>
        </header>

        <section className="mb-8">
          <TravelForm onSearch={handleSearch} isLoading={loading} />
        </section>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-center">
            {error}
          </div>
        )}

        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto mb-4"></div>
            <p className="text-gray-500">Buscando as melhores combinações no Kayak (Mock)...</p>
          </div>
        )}

        {result && (
          <section>
            <ResultsView result={result} />
          </section>
        )}
      </div>
    </main>
  );
}
