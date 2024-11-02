import logo from './logo.jpg';
import React, { useEffect, useState } from 'react';
import './App.css';
import BASE_URL from './services/base_url'; // Import the base URL
import Chatbot from './components/Chatbot'; // Import the Chatbot components

function App() {
    return (
        <div className="App">
            <Chatbot /> {/* Render the Chatbot component */}
        </div>
    );
}

export default App;
