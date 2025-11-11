import React from 'react';
import PharmacySearch from './components/PharmacySearch';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Healthcare - Tìm kiếm thuốc</h1>
        <p>Hệ thống tìm kiếm và tư vấn thuốc thông minh</p>
      </header>
      
      <main>
        <PharmacySearch />
      </main>
      
      <footer className="App-footer">
        <p>&copy; 2025 AI Healthcare. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
