import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import Header from './components/Header';
// import Home from './pages/Home';

function App() {
  return (
    <Router>
      {/* <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/recipes" element={<Recipes />} />
          <Route path="/add-item" element={<AddItem />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div> */}
    </Router>
  );
}

export default App;
