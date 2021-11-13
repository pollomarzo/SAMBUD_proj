import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Neo4jProvider, createDriver } from 'use-neo4j'
import AppThemeProvider from './theme';
import CssBaseline from '@mui/material/CssBaseline';

const driver = createDriver('neo4j+s', '61208074.databases.neo4j.io', '7687', 'neo4j', 'E0hYQi0OjKRI3CPz4wpN8I5PGVgSyw1JCBaJ2sUdZz8')

ReactDOM.render(
  <AppThemeProvider>
    <Neo4jProvider driver={driver}>
      <CssBaseline />
      <App />
    </Neo4jProvider >
  </AppThemeProvider>
  ,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
