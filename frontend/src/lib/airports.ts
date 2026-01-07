export interface Airport {
    iata: string;
    name: string;
    city: string;
    country: string;
}

export const airports: Airport[] = [
    { iata: 'GRU', name: 'Guarulhos Intl', city: 'São Paulo', country: 'Brasil' },
    { iata: 'CGH', name: 'Congonhas', city: 'São Paulo', country: 'Brasil' },
    { iata: 'VCP', name: 'Viracopos', city: 'Campinas', country: 'Brasil' },
    { iata: 'GIG', name: 'Galeão Intl', city: 'Rio de Janeiro', country: 'Brasil' },
    { iata: 'SDU', name: 'Santos Dumont', city: 'Rio de Janeiro', country: 'Brasil' },
    { iata: 'BSB', name: 'Pres. Juscelino Kubitschek', city: 'Brasília', country: 'Brasil' },
    { iata: 'CNF', name: 'Confins', city: 'Belo Horizonte', country: 'Brasil' },
    { iata: 'CDG', name: 'Charles de Gaulle', city: 'Paris', country: 'França' },
    { iata: 'ORY', name: 'Orly', city: 'Paris', country: 'França' },
    { iata: 'LIS', name: 'Humberto Delgado', city: 'Lisboa', country: 'Portugal' },
    { iata: 'OPO', name: 'Francisco Sá Carneiro', city: 'Porto', country: 'Portugal' },
    { iata: 'MAD', name: 'Barajas', city: 'Madrid', country: 'Espanha' },
    { iata: 'BCN', name: 'El Prat', city: 'Barcelona', country: 'Espanha' },
    { iata: 'LHR', name: 'Heathrow', city: 'London', country: 'Reino Unido' },
    { iata: 'JFK', name: 'John F. Kennedy', city: 'New York', country: 'EUA' },
    { iata: 'MIA', name: 'Miami Intl', city: 'Miami', country: 'EUA' },
    { iata: 'MCO', name: 'Orlando Intl', city: 'Orlando', country: 'EUA' },
    { iata: 'EZE', name: 'Ezeiza', city: 'Buenos Aires', country: 'Argentina' },
    { iata: 'SCL', name: 'Arturo Merino Benítez', city: 'Santiago', country: 'Chile' },
    { iata: 'DXB', name: 'Dubai Intl', city: 'Dubai', country: 'Emirados Árabes' },
    { iata: 'GYN', name: 'Santa Genoveva', city: 'Goiânia', country: 'Brasil' },
];
