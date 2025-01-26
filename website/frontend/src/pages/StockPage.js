import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./StockPage.css";

const StockPage = () => {
    const { ticker } = useParams();
    const [stockData, setStockData] = useState(null);
    const [relatedNews, setRelatedNews] = useState([]);
    const [loading, setLoading] = useState(true);

    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    function formatNumber(number) {
        if (number >= 1e12) {
            return `${(number / 1e12).toFixed(1)} Trillion`;
        } else if (number >= 1e9) {
            return `${(number / 1e9).toFixed(1)} Billion`;
        } else if (number >= 1e6) {
            return `${(number / 1e6).toFixed(1)} Million`;
        } else {
            return number.toString();
        }
    }

    useEffect(() => {
        const fetchStockData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/get_stock_data?ticker=${ticker}`);
                if (!response.ok) {
                    throw new Error("Failed to fetch stock data");
                }
                const data = await response.json();
                setStockData(data.stock_data);
                setRelatedNews(data.related_news);
            } catch (error) {
                console.error("Error fetching stock data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchStockData();
    }, [ticker]);

    const getPriceChangeStyle = (change) => {
        if (change > 0) return "bg-green-100 text-green-600";
        if (change < 0) return "bg-red-100 text-red-600";
        return "bg-gray-100 text-gray-600";
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen">
            <header className="bg-gray-800 text-white p-6 mb-10">
                <div className="flex justify-center items-center">
                    <h1 className="text-3xl font-bold">{ticker}</h1>
                </div>
            </header>

            <main className="max-w-6xl mx-auto">
                {loading ? (
                    <p className="text-center text-gray-500">Loading...</p>
                ) : (
                    <>
                        <section className="mb-12">
                            <h2 className="text-2xl font-semibold mb-6 text-gray-700 text-center">
                                Stock Data
                            </h2>
                            {stockData ? (
                                <div className="stock-data">
                                    <div className="stock-data-item">
                                        <p>Current Price</p>
                                        <span className="text-green-600">
                                            ${stockData["Current Price"]}
                                        </span>
                                    </div>
                                    <div className="stock-data-item">
                                        <p>Market Cap</p>
                                        <span className="text-blue-600">
                                            ${formatNumber(stockData["Market Cap"])}
                                        </span>
                                    </div>
                                    <div className="stock-data-item">
                                        <p>52 Week Range</p>
                                        <span>${stockData["52 Week Range"]}</span>
                                    </div>
                                    <div className="stock-data-item">
                                        <p>Volume</p>
                                        <span>{formatNumber(stockData["Volume"])}</span>
                                    </div>
                                </div>
                            ) : (
                                <p className="text-center text-gray-500">No data available</p>
                            )}
                        </section>
                        <section>
                            <h2 className="text-2xl font-semibold mb-6 text-gray-700 text-center">
                                News Analysis for {stockData["Company"]} ({ticker})
                            </h2>
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                                {relatedNews.map((news, index) => (
                                    <div
                                        key={index}
                                        className="card"
                                    >
                                        <h3 className="text-lg font-bold text-gray-800 mb-4">
                                            {news.headline}
                                        </h3>
                                        <p className="text-sm text-gray-600 mb-4">{news.summary}</p>
                                        <div className="prediction-label">Prediction</div>
                                        <div
                                            className={`percentage-box ${getPriceChangeStyle(
                                                news.price_change
                                            )} border font-bold`}
                                        >
                                            {news.price_change > 0 ? "+" : ""}
                                            {news.price_change}%
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </section>
                    </>
                )}
            </main>
        </div>
    );
};

export default StockPage;
