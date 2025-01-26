import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import StockSearch from '../components/StockSearch';
import './Home.css';

export default function Home() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const FLASK_API_URL = process.env.REACT_APP_API_BASE_URL;

    useEffect(() => {
        // Fetch data from the API
        const fetchEvents = async () => {
            try {
                const response = await fetch(`${FLASK_API_URL}/api/get_events`);
                if (!response.ok) {
                    throw new Error('Failed to fetch events data');
                }
                const data = await response.json();
                setEvents(data);
            } catch (error) {
                console.error('Error fetching events:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
    }, []);

    const getStockStyle = (change) => {
        if (change > 0) {
            return 'bg-green-100 text-green-600';
        } else if (change < 0) {
            return 'bg-red-100 text-red-600';
        } else {
            return 'bg-gray-100 text-gray-600';
        }
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen">
            <header className="bg-gray-800 text-white p-6 mb-10">
                <div className="flex justify-center items-center">
                    <h1 className="text-3xl font-bold">MarketPulse</h1>
                </div>
            </header>
    
            <main className="max-w-6xl mx-auto">
                <section className="text-center mb-12">
                    <StockSearch />
                </section>
                <br /><br />
                <section>
                    <h2 className="text-2xl font-semibold mb-6 text-gray-700 text-center">News Summary</h2>
    
                    {loading ? (
                        <p className="text-center text-gray-500">Loading events...</p>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {events.map((event, index) => (
                                <div
                                    key={index}
                                    className="card"
                                >
                                    <h3 className="text-lg font-bold text-gray-800 mb-4">
                                        {event.headline}
                                    </h3>
                                    <p className="text-sm text-gray-600 mb-4">{event.summary}</p>
                                    <div className="ticker-container">
                                        {Object.entries(event.pricechanges).map(([ticker, change]) => (
                                            <div
                                                key={ticker}
                                                className={`ticker ${
                                                    change > 0 ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                                                }`}
                                            >
                                                <div className="prediction-label">Prediction</div>
                                                <Link
                                                    to={`/stock/${ticker}`}
                                                    className="text-sm font-medium"
                                                >
                                                    {ticker}: {change > 0 ? '+' : ''}{change}%
                                                </Link>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </section>
            </main>
        </div>
    );    
}
