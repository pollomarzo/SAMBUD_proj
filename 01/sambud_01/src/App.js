// inspired by https://github.dev/its-hmny/M-and-M
// i wrote that one too so no copying here :)

import logo from "./logo.svg";
import { Button } from "@mui/material";
import React, { useEffect, useState, useMemo } from "react";
import ReactFlow from "react-flow-renderer";
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Divider,
  Fab,
  Tooltip,
  Box,
  Container,
  Typography,
  Paper,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";

import QueryList from "./QueryList";
import Table from "./Table";
import { NeoGraph, ResponsiveNeoGraph } from "./NeoGraph";
import {
  NEO4J_HOST_URI,
  NEO4J_USER,
  NEO4J_PASSWORD,
  NEO4J_PROTOCOL,
  NEO4J_FULL_URI,
} from "./secrets";

function App({ driver }) {
  const [message, setMessage] = useState("");
  const [elements, setElements] = useState([]);
  const [selected, setSelected] = useState(undefined);
  const [result, setResult] = useState(undefined);

  return (
    <div style={{ padding: "50px 100px" }}>
      <Typography style={{ paddingBottom: 30 }} variant="h3">
        EXPLORER
      </Typography>
      <Paper elevation={4}>
        <Box
          sx={{
            height: "80vh",
            width: "90vw",
            padding: 2,
            // marginLeft: '5vh',
            display: "flex",
            flexDirection: "row",
            overflow: "hidden",
            bgColor: "paper.background",
          }}
        >
          {" "}
          <div style={{ width: "25vw" }}>
            <QueryList setResult={setResult} setElements={setElements} />
          </div>
          <Box
            sx={{
              position: "relative",
              width: "55vw",
              overflow: "hidden",
              backgroundColor: "rgb(211, 211, 211)",
            }}
          >
            {result ? (
              result.view === "graph" ? (
                <ResponsiveNeoGraph
                  driver={driver}
                  containerId={"id0"}
                  neo4jUri={NEO4J_HOST_URI}
                  neo4jUser={NEO4J_USER}
                  neo4jPassword={NEO4J_PASSWORD}
                  height={"100%"}
                  width={"100%"}
                  cypher={result.cypher}
                />
              ) : (
                <Table data={result} />
              )
            ) : (
              <div>Select a query to see the result</div>
            )}
          </Box>
        </Box>
      </Paper>
    </div>
  );
}

export default App;
