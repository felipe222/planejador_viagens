import { NextResponse } from 'next/server';
import cidades from '@/lib/data/cidades.json';

interface LocalCity {
  id: string;
  nome: string;
  lat: number;
  lon: number;
  tipo: string;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const nameQuery = searchParams.get('name')?.toLowerCase() || '';
  const cityQuery = searchParams.get('city')?.toLowerCase() || '';

  // If no query, return empty
  if (nameQuery.length < 2 && cityQuery.length < 2) {
    return NextResponse.json([]);
  }

  const query = (nameQuery || cityQuery).normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  try {
    // Filter local data
    const filtered = (cidades as LocalCity[]).filter(c => {
      const idNorm = c.id.toLowerCase();
      const nomeNorm = c.nome.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      return idNorm.includes(query) || nomeNorm.includes(query);
    });


    // Map to expected format
    const results = filtered.map(c => {
      // Simple heuristic to extract city name if possible, or just use full name
      const cityName = c.nome.split('(')[0].trim();
      return {
        iata: c.id,
        name: c.nome,
        city: cityName,
        country: "Brasil"
      };
    });

    return NextResponse.json(results);
  } catch (error) {
    console.error('[API Route] Error processing local data:', error);
    return NextResponse.json({ error: 'Failed to search airports' }, { status: 500 });
  }
}
