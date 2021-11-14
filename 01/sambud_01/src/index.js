import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { Neo4jProvider, createDriver } from "use-neo4j";
import AppThemeProvider from "./theme";
import CssBaseline from "@mui/material/CssBaseline";
import {
  NEO4J_HOST_URI,
  NEO4J_USER,
  NEO4J_PASSWORD,
  NEO4J_SCHEME,
  NEO4J_FULL_URI,
} from "./secrets";
import Neo4j from "neo4j-driver";

const driver = Neo4j.driver(
  NEO4J_HOST_URI,
  Neo4j.auth.basic(NEO4J_USER, NEO4J_PASSWORD)
);

console.log(driver);

ReactDOM.render(
  <AppThemeProvider>
    <Neo4jProvider driver={driver}>
      <CssBaseline />
      <App />
    </Neo4jProvider>
  </AppThemeProvider>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
