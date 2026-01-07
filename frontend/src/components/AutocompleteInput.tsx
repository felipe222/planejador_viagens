import React, { useState, useEffect, useRef } from 'react';

// Use same interface as mock, or slightly adapted for API response
interface ApiAirport {
    iata: string;
    name: string;
    city: string;
    country: string;
}

interface AutocompleteInputProps {
    value: string;
    onChange: (value: string) => void;
    onSelect?: (airport: ApiAirport) => void;
    label: string;
    placeholder?: string;
    maxLength?: number;
}

export default function AutocompleteInput({ value, onChange, onSelect, label, placeholder, maxLength }: AutocompleteInputProps) {
    const [suggestions, setSuggestions] = useState<ApiAirport[]>([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [loading, setLoading] = useState(false);
    const wrapperRef = useRef<HTMLDivElement>(null);

    // Debounce timer ref
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);

    useEffect(() => {
        // Clear previous timeout
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        // Only search if user types something significant 
        if (value.length >= 2) {
            timeoutRef.current = setTimeout(async () => {
                setLoading(true);
                console.log(`[Autocomplete] Search triggered for: "${value}"`);
                let found: ApiAirport[] = [];

                try {
                    // 1. Try API first
                    const apiUrl = `/api/airports?name=${encodeURIComponent(value)}`;
                    console.log(`[Autocomplete] Fetching API: ${apiUrl}`);
                    const res = await fetch(apiUrl);

                    if (res.ok) {
                        found = await res.json();
                        console.log(`[Autocomplete] API response OK. Items found: ${found?.length}`);
                    } else {
                        console.warn(`[Autocomplete] API returned status: ${res.status}`);
                    }
                } catch (err) {
                    console.error("[Autocomplete] API fetch failed:", err);
                }

                // 2. Fallback removed. We rely on the API (which uses local JSON).
                if (!found || found.length === 0) {
                    console.log('[Autocomplete] No API results.');
                }

                setSuggestions(found.slice(0, 10)); // Limit to 10
                setLoading(false);
            }, 300); // 300ms debounce
        } else {
            console.log('[Autocomplete] Input too short, clearing suggestions');
            setTimeout(() => setSuggestions([]), 0);
        }

        return () => {
            if (timeoutRef.current) clearTimeout(timeoutRef.current);
        };
    }, [value]);

    // Close suggestions when clicking outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
                setShowSuggestions(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [wrapperRef]);

    const handleSelect = (airport: ApiAirport) => {
        if (onSelect) {
            onSelect(airport);
        } else {
            // Fallback for stops which might not have onSelect yet
            onChange(airport.iata);
        }
        setShowSuggestions(false);
    };

    return (
        <div ref={wrapperRef} className="relative">
            <label className="block text-sm font-medium mb-1">{label}</label>
            <input
                type="text"
                value={value}
                onChange={(e) => {
                    onChange(e.target.value); // Allow any case while typing
                    setShowSuggestions(true);
                }}
                onFocus={() => {
                    if (suggestions.length > 0) setShowSuggestions(true);
                }}
                className="w-full border rounded p-2"
                placeholder={placeholder}
                maxLength={maxLength}
            />
            {loading && <div className="absolute right-2 top-9 text-xs text-gray-400">...</div>}

            {showSuggestions && suggestions.length > 0 && (
                <ul className="absolute z-10 w-full bg-white border border-gray-300 rounded mt-1 shadow-lg max-h-60 overflow-auto text-sm">
                    {suggestions.map((airport, idx) => (
                        <li
                            key={`${airport.iata}-${idx}`}
                            onClick={() => handleSelect(airport)}
                            className="p-2 hover:bg-blue-50 cursor-pointer border-b last:border-b-0 text-gray-700 block"
                        >
                            <div className="font-bold inline-block mr-1">{airport.iata}</div>
                            <div className="inline-block">{airport.name}</div>
                            <div className="text-gray-500 text-xs ml-1 block">
                                ({airport.city}, {airport.country})
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
