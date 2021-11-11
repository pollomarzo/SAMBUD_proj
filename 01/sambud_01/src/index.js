import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Neo4jProvider, createDriver } from 'use-neo4j'

const driver = createDriver('neo4j+s://cbdc369d.databases.neo4j.io', 'myauradb.neo4j.io', 7687, 'neo4j', 'mYYGw4dV-v7GLAuwWUuwfhqCJKUs_zSR4ytR-xf-MRk')

ReactDOM.render(
  <React.StrictMode>
    <Neo4jProvider
      driver={driver}
    >
      <App />
    </Neo4jProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
