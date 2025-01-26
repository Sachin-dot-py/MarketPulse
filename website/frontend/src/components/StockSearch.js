import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaSearch } from 'react-icons/fa';
import './StockPage.css';

export default function StockSearch() {
    const [query, setQuery] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const navigate = useNavigate();
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
        setQuery(ticker);
        setSuggestions([]);
    };

    const handleSearchSubmit = (e) => {
        e.preventDefault();
        if (query.trim() !== '') {
            navigate(`/stock/${query}`);
        }
    };

    return (
            <div className="wrapper">
    <form onSubmit={handleSearchSubmit} className="relative flex items-center">
        <input
            type="text"
            placeholder="Search stocks..."
            className="w-full p-4 text-lg rounded-l-lg border border-gray-300 shadow-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={query}
            onChange={handleInputChange}
        />
        <button
            type="submit"
            className="p-4 bg-blue-600 text-white rounded-r-lg shadow-md hover:bg-blue-700 transition duration-300 flex items-center justify-center"
        >
            <FaSearch />
        </button>
    </form>
    {suggestions.length > 0 && (
        <ul className="absolute bg-white border border-gray-200 mt-2 rounded-lg shadow-lg w-full z-10">
            {suggestions.map((stock) => (
                <li
                    key={stock.Ticker}
                    className="p-3 hover:bg-blue-100 cursor-pointer transition duration-200 flex justify-between items-center"
                    onClick={() => handleSuggestionClick(stock.Ticker)}
                >
                    <span className="font-semibold text-gray-700">{stock.Name}</span>
                    <span className="text-sm text-gray-500">{stock.Ticker}</span>
                </li>
            ))}
        </ul>
    )}
</div>
    );
}
