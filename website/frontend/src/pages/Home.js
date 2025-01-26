import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
    const [activeTab, setActiveTab] = useState('Last Day'); // Manage active tab state

    const handleTabClick = (tab) => {
        setActiveTab(tab);
        // Add logic to fetch relevant data for the selected time range
    };

    return (
        <div className="p-6">
            <header className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">MarketPulse</h1>
                <div className="w-1/3">
                    <input
                        type="text"
                        placeholder="Search stocks..."
                        className="border p-2 rounded w-full"
                    />
                </div>
            </header>

            <section>
                <h2 className="text-xl font-semibold mb-4">View News Summary</h2>
                {/* Tabs Section */}
                <div className="flex space-x-4 mb-4">
                    {['Last Day', 'Last Week', 'Last Month'].map((tab) => (
                        <button
                            key={tab}
                            className={`px-4 py-2 rounded ${
                                activeTab === tab ? 'bg-black text-white' : 'bg-gray-200 text-black'
                            }`}
                            onClick={() => handleTabClick(tab)}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                {/* Events Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Sample Event Card */}
                    <div className="border p-4 rounded shadow">
                        <h3 className="text-lg font-bold">Event Title</h3>
                        <p className="text-sm text-gray-600 mb-2">
                            A brief description of the event...
                        </p>
                        <div className="grid grid-cols-2 gap-2">
                            {/* Affected Stocks */}
                            <div className="border p-2 rounded bg-gray-100">
                                <Link to="/stock/1" className="text-blue-500 text-sm font-medium">
                                    Stock A
                                </Link>
                            </div>
                            <div className="border p-2 rounded bg-gray-100">
                                <Link to="/stock/2" className="text-blue-500 text-sm font-medium">
                                    Stock B
                                </Link>
                            </div>
                        </div>
                        <Link to="/event/1" className="text-blue-500 text-sm mt-2 inline-block">
                            View Details
                        </Link>
                    </div>
                    {/* Repeat Event Cards dynamically */}
                </div>
            </section>
        </div>
    );
}
