import React from 'react';
import { Link } from 'react-router-dom';
import StockSearch from '../components/StockSearch';
import './Home.css';

export default function Home() {
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

                <section>
                    <h2 className="text-2xl font-semibold mb-6 text-gray-700 text-center">News Summary</h2>

                    {/* Events Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {/* Sample Event Card */}
                        <div className="bg-white border border-gray-200 rounded shadow-lg p-4 text-center">
                            <h3 className="text-lg font-bold text-gray-800 mb-4">Event Title 1</h3>
                            <p className="text-sm text-gray-600 mb-4">
                                A brief description of the event...
                            </p>
                            <div className="grid grid-cols-2 gap-2 mb-4">
                                {/* Affected Stocks */}
                                <div className="bg-green-100 p-2 rounded shadow-sm">
                                    <Link to="/stock/1" className="text-green-600 text-sm font-medium">
                                        Stock A
                                    </Link>
                                </div>
                                <div className="bg-red-100 p-2 rounded shadow-sm">
                                    <Link to="/stock/2" className="text-red-600 text-sm font-medium">
                                        Stock B
                                    </Link>
                                </div>
                            </div>
                            <Link to="/event/1" className="text-blue-500 text-sm font-medium mt-4 block">
                                View Details
                            </Link>
                        </div>

                        <div className="bg-white border border-gray-200 rounded shadow-lg p-4 text-center">
                            <h3 className="text-lg font-bold text-gray-800 mb-4">Event Title 2</h3>
                            <p className="text-sm text-gray-600 mb-4">
                                A brief description of the event...
                            </p>
                            <div className="grid grid-cols-2 gap-2 mb-4">
                                {/* Affected Stocks */}
                                <div className="bg-green-100 p-2 rounded shadow-sm">
                                    <Link to="/stock/3" className="text-green-600 text-sm font-medium">
                                        Stock C
                                    </Link>
                                </div>
                                <div className="bg-red-100 p-2 rounded shadow-sm">
                                    <Link to="/stock/4" className="text-red-600 text-sm font-medium">
                                        Stock D
                                    </Link>
                                </div>
                            </div>
                            <Link to="/event/2" className="text-blue-500 text-sm font-medium mt-4 block">
                                View Details
                            </Link>
                        </div>

                        <div className="bg-white border border-gray-200 rounded shadow-lg p-4 text-center">
                            <h3 className="text-lg font-bold text-gray-800 mb-4">Event Title 3</h3>
                            <p className="text-sm text-gray-600 mb-4">
                                A brief description of the event...
                            </p>
                            <div className="grid grid-cols-2 gap-2 mb-4">
                                {/* Affected Stocks */}
                                <div className="bg-green-100 p-2 rounded shadow-sm">
                                    <Link to="/stock/5" className="text-green-600 text-sm font-medium">
                                        Stock E
                                    </Link>
                                </div>
                                <div className="bg-red-100 p-2 rounded shadow-sm">
                                    <Link to="/stock/6" className="text-red-600 text-sm font-medium">
                                        Stock F
                                    </Link>
                                </div>
                            </div>
                            <Link to="/event/3" className="text-blue-500 text-sm font-medium mt-4 block">
                                View Details
                            </Link>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
