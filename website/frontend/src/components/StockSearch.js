import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../pages/StockPage.css';

export default function StockSearch() {
    const [query, setQuery] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const navigate = useNavigate(); // Hook for navigation
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleInputChange = async (e) => {
        const value = e.target.value;
        setQuery(value);

        if (value.trim() === '') {
            setSuggestions([]);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/stocks/autocomplete?q=${value}`);
            const data = await response.json();
            setSuggestions(data);
        } catch (error) {
            console.error('Error fetching autocomplete results:', error);
        }
    };

    const handleSuggestionClick = (ticker) => {
        setQuery(ticker); // Replace input value with the selected suggestion ticker
        setSuggestions([]); // Clear suggestions
    };

    const handleSearchSubmit = (e) => {
        e.preventDefault(); // Prevent form submission behavior
        if (query.trim() !== '') {
            navigate(`/stock/${query}`); // Navigate to the stock page
        }
    };

    return (
        <div className="w-full sm:w-3/4 lg:w-2/3 mx-auto">
            <form onSubmit={handleSearchSubmit} className="relative">
                <input
                    type="text"
                    placeholder="Search stocks..."
                    className="w-full p-6 text-xl rounded-lg border border-gray-300 shadow-md"
                    value={query}
                    onChange={handleInputChange}
                />
                {suggestions.length > 0 && (
                    <ul className="absolute bg-white border border-gray-200 mt-2 rounded-lg shadow-lg w-full z-10">
                        {suggestions.map((stock) => (
                            <li
                                key={stock.Ticker}
                                className="p-2 hover:bg-gray-100 cursor-pointer"
                                onClick={() => handleSuggestionClick(stock.Ticker)}
                            >
                                {stock.Ticker} - {stock.Name}
                            </li>
                        ))}
                    </ul>
                )}
                <button
                    type="submit"
                    className="absolute right-2 top-2 px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md"
                >
                    Search
                </button>
            </form>
        </div>
    );
}
