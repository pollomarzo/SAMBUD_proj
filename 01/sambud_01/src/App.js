import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import { Button } from '@mui/material';
import { useReadCypher, useLazyWriteCypher } from 'use-neo4j'

function App() {
  const [message, setMessage] = useState("");
  const query = `Match (m:Movie) where m.released > 2000 RETURN m limit 5`
  const params = { title: 'The Matrix' }


  const { cypher, error, loading, result, records, first } = useReadCypher(query, params)

  if (loading || !result) return (<div>Loading...</div>)
  if (error) return (<div>ERROR</div>)

  // Get `m` from the first row
  const movie = first.get('m')
  console.log(cypher, error, !loading, result, records, first, movie)

  return (
    <div className="App">
      {movie.properties.title} was retrieved from database
      {/* <Button onClick={handleSubmit}>
        Carica dati
      </Button> */}
    </div >
  );
}

export default App;
