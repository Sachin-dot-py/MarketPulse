import React from "react";
import { BrowserRouter as Router, Routes, Route, useParams } from "react-router-dom";
import "./StockPage.css";

const StockPage = () => {
    const { ticker } = useParams();
    return (
        <>
            <h1>{ticker}</h1>
            <p>You are viewing details for stock with ticker: {ticker}</p>
        </>
    );
};

export default StockPage;