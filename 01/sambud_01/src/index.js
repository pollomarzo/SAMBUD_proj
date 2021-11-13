import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Neo4jProvider, createDriver } from 'use-neo4j'
import AppThemeProvider from './theme';
import CssBaseline from '@mui/material/CssBaseline';
import {
  NEO4J_HOST_URI,
  NEO4J_USER,
  NEO4J_PASSWORD,
  NEO4J_PROTOCOL} from './secrets';

const driver = createDriver(NEO4J_PROTOCOL, NEO4J_HOST_URI, '7687', NEO4J_USER, NEO4J_PASSWORD);

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
