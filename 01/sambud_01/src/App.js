import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import { Button } from '@mui/material';

function App() {
  const [message, setMessage] = useState("");

  return (
    <div className="App">
      <p>
        {message}
      </p>
      <Button onClick={ }>
        Carica dati
      </Button>
    </div>
  );
}

export default App;
