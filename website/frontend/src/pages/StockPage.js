import React from "react";
import { useParams } from "react-router-dom";
import "./StockPage.css";

const StockPage = () => {
    const { ticker } = useParams();

    return (
        <div className="p-6 bg-gray-50 min-h-screen">
            <header className="bg-gray-800 text-white p-6 mb-10">
                <div className="flex justify-center items-center">
                    <h1 className="text-3xl font-bold">{ticker}</h1>
                </div>
            </header>

            <main className="max-w-6xl mx-auto">
                <h2 className="text-2xl font-semibold mb-6 text-gray-700 text-center">
                    News Articles for {ticker}
                </h2>

                {/* News Articles Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Example News Card */}
                    <div className="bg-white border border-gray-200 rounded shadow-lg p-4 text-center">
                        <h3 className="text-lg font-bold text-gray-800 mb-4">News Title 1</h3>
                        <p className="text-sm text-gray-600 mb-4">
                            A brief summary of the news article goes here...
                        </p>
                        <div className="flex items-center justify-between mt-4">
                            <div className="percentage-box bg-green-100 border border-green-600 text-green-600 font-bold">
                                70%
                            </div>
                        </div>
                    </div>

                    <div className="bg-white border border-gray-200 rounded shadow-lg p-4 text-center">
                        <h3 className="text-lg font-bold text-gray-800 mb-4">News Title 2</h3>
                        <p className="text-sm text-gray-600 mb-4">
                            Another summary of a news article...
                        </p>
                        <div className="flex items-center justify-between mt-4">
                            <div className="percentage-box bg-green-100 border border-green-600 text-green-600 font-bold">
                                40%
                            </div>
                            <div className="percentage-box bg-red-100 border border-red-600 text-red-600 font-bold">
                                60%
                            </div>
                        </div>
                    </div>

                    <div className="bg-white border border-gray-200 rounded shadow-lg p-4 text-center">
                        <h3 className="text-lg font-bold text-gray-800 mb-4">News Title 3</h3>
                        <p className="text-sm text-gray-600 mb-4">
                            A brief summary of the news article goes here...
                        </p>
                        <div className="flex items-center justify-between mt-4">
                            <div className="percentage-box bg-green-100 border border-green-600 text-green-600 font-bold">
                                80%
                            </div>
                            <div className="percentage-box bg-red-100 border border-red-600 text-red-600 font-bold">
                                20%
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default StockPage;
