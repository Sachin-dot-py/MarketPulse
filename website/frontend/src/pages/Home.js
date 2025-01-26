import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'

export default function Home() {
    return (
        <div className="p-6 bg-gray-50 min-h-screen">
            <header className="bg-gray-800 text-white p-4 mb-6">
                <div className="flex justify-between items-center max-w-6xl mx-auto">
                    <h1 className="text-2xl font-bold">MarketPulse</h1>
                    <div className="w-1/3">
                        <input
                            type="text"
                            placeholder="Search stocks..."
                            className="w-full p-2 rounded border border-gray-300"
                        />
                    </div>
                </div>
            </header>

            <main className="max-w-6xl mx-auto">
                <section>
                    <h2 className="text-xl font-semibold mb-4 text-gray-700">News Summary</h2>

                    {/* Events Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {/* Sample Event Card */}
                        <div className="bg-white border border-gray-200 rounded shadow-sm p-4">
                            <h3 className="text-lg font-bold text-gray-800">Event Title 1</h3>
                            <p className="text-sm text-gray-600 mb-4">
                                A brief description of the event...
                            </p>
                            <div className="grid grid-cols-2 gap-2 mb-4">
                                {/* Affected Stocks */}
                                <div className="bg-gray-100 p-2 rounded text-center">
                                    <Link to="/stock/1" className="text-blue-500 text-sm font-medium">
                                        Stock A
                                    </Link>
                                </div>
                                <div className="bg-gray-100 p-2 rounded text-center">
                                    <Link to="/stock/2" className="text-blue-500 text-sm font-medium">
                                        Stock B
                                    </Link>
                                </div>
                            </div>
                            <Link to="/event/1" className="text-blue-500 text-sm font-medium">
                                View Details
                            </Link>
                        </div>

                        <div className="bg-white border border-gray-200 rounded shadow-sm p-4">
                            <h3 className="text-lg font-bold text-gray-800">Event Title 2</h3>
                            <p className="text-sm text-gray-600 mb-4">
                                A brief description of the event...
                            </p>
                            <div className="grid grid-cols-2 gap-2 mb-4">
                                {/* Affected Stocks */}
                                <div className="bg-gray-100 p-2 rounded text-center">
                                    <Link to="/stock/3" className="text-blue-500 text-sm font-medium">
                                        Stock C
                                    </Link>
                                </div>
                                <div className="bg-gray-100 p-2 rounded text-center">
                                    <Link to="/stock/4" className="text-blue-500 text-sm font-medium">
                                        Stock D
                                    </Link>
                                </div>
                            </div>
                            <Link to="/event/2" className="text-blue-500 text-sm font-medium">
                                View Details
                            </Link>
                        </div>

                        <div className="bg-white border border-gray-200 rounded shadow-sm p-4">
                            <h3 className="text-lg font-bold text-gray-800">Event Title 3</h3>
                            <p className="text-sm text-gray-600 mb-4">
                                A brief description of the event...
                            </p>
                            <div className="grid grid-cols-2 gap-2 mb-4">
                                {/* Affected Stocks */}
                                <div className="bg-gray-100 p-2 rounded text-center">
                                    <Link to="/stock/5" className="text-blue-500 text-sm font-medium">
                                        Stock E
                                    </Link>
                                </div>
                                <div className="bg-gray-100 p-2 rounded text-center">
                                    <Link to="/stock/6" className="text-blue-500 text-sm font-medium">
                                        Stock F
                                    </Link>
                                </div>
                            </div>
                            <Link to="/event/3" className="text-blue-500 text-sm font-medium">
                                View Details
                            </Link>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
