import React, { useState, useEffect, useRef, useCallback } from 'react';
import './Chatbot.css'; // Ensure to import the CSS
import logo from '../logo.jpg'; // Import your logo
import BASE_URL from '../services/base_url.js';

const Chatbot = ({ currentUser, handleLogout }) => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [maxHeight, setMaxHeight] = useState(0);
    const [context, setContext] = useState({
        intent: null,
        collectedParams: {},
        currentParamIndex: 0,
    });
    const messagesContainerRef = useRef(null);

    const parameters = ['Make', 'Model', 'Variant', 'Year', 'Price', 'Kilometers Driven', 'Fuel Type'];

    const fetchData = async () => {
        if (newMessage.trim() !== '') {
            try {
                const requestBody = {
                    message: newMessage,
                    context: context // Send context with the request
                };
                const response = await fetch(`${BASE_URL}/get_chatbot_response`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include', // Ensure cookies are included in the request
                    body: JSON.stringify(requestBody)
                });
                const data = await response.json();

                // Update messages state
                setMessages(prevMessages => [
                    ...prevMessages,
                    { text: newMessage, isSystem: false },
                    { text: data.message, isSystem: true }
                ]);

                // Update context with the new state from the response
                setContext(data.context);
                setNewMessage('');
            } catch (error) {
                console.error('Error:', error);
            }
        }
    };

    const scrollToBottom = () => {
        if (messagesContainerRef.current) {
            messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
        }
    };

    const adjustMaxHeight = useCallback(() => {
        const singleLineHeight = 30;
        const linesToShow = 6;
        const minimumHeight = singleLineHeight * 2;
        let totalLines = 0;
        messages.forEach(message => {
            totalLines += Math.ceil(message.text.length / 50);
        });

        setMaxHeight(Math.max(totalLines * singleLineHeight, minimumHeight, singleLineHeight * linesToShow));
    }, [messages]);

    const populateInput = (text) => {
        setNewMessage(text);
    };

    useEffect(() => {
        scrollToBottom();
        adjustMaxHeight();
    }, [messages, adjustMaxHeight]);

    return (
        <div className="container">
            <div className="center">
                <img src={logo} alt="Logo" className="logo" />
                <h1><span className="welcome-text">Welcome to CarXstream</span></h1>
            </div>
            <div className="strip">
                <div className="center faded-text">Gaadi ka Sapna</div>
            </div>
            <div className="card-container">
                <div className="card" onClick={() => populateInput("I want to Buy a Car")}>I want to Buy a Car</div>
                <div className="card" onClick={() => populateInput("I want to Sell a Car")}>I want to Sell a Car</div>
            </div>
            {messages.length > 0 && (
                <div className="messages-container" style={{ maxHeight: `${maxHeight}px`, border: '1px solid #ccc' }} ref={messagesContainerRef}>
                    {messages.map((message, index) => (
                        <div key={index} className={message.isSystem ? 'system-message-container' : 'user-message-container'}>
                            {message.isSystem && <img src={logo} alt="Logo" className="small-logo" />}
                            <div className={message.isSystem ? 'system-message' : 'user-message'}>{message.text}</div>
                        </div>
                    ))}
                </div>
            )}
            <div className="input-container">
                <input
                    type="text"
                    className="input-field"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyUp={(e) => { if (e.key === 'Enter') fetchData(); }}
                    placeholder="Ask a question..."
                />
                <button className="input-btn" onClick={fetchData}>Enter</button>
            </div>
        </div>
    );
};

export default Chatbot;
