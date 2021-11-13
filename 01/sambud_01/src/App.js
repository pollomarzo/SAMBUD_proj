// inspired by https://github.dev/its-hmny/M-and-M
// i wrote that one too so no copying here :)

import logo from './logo.svg';
import { Button } from '@mui/material';
import React, { useEffect, useState, useMemo } from 'react';
import ReactFlow from 'react-flow-renderer';
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
  Paper
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

import QueryList from './QueryList';


function App() {
  const [message, setMessage] = useState("");
  const [elements, setElements] = useState([
    {
      id: '1',
      type: 'input', // input node
      data: { label: 'Input Node' },
      position: { x: 250, y: 25 },
    },
    // default node
    {
      id: '2',
      // you can also pass a React component as a label
      data: { label: <div>Default Node</div> },
      position: { x: 100, y: 125 },
    },
    {
      id: '3',
      type: 'output', // output node
      data: { label: 'Output Node' },
      position: { x: 250, y: 250 },
    },
    // animated edge
    { id: 'e1-2', source: '1', target: '2', animated: true },
    { id: 'e2-3', source: '2', target: '3' },
  ]);
  const [selected, setSelected] = useState(undefined);
  const [result, setResult] = useState(undefined);

  console.log("CIAO MI STO RIRENDERIZZANDO")

  return (
    <Container>
      <Typography variant="h3">
        Database explorer
      </Typography>
      <Paper>
        <Box sx={{
          height: '80vh',
          width: '90vw',
          marginTop: '10vh',
          // marginLeft: '5vh',
          display: 'flex',
          flexDirection: 'row',
          overflow: 'hidden',
          bgColor: 'paper.background'
        }}>
          <QueryList setResult={setResult} setElements={setElements} />
          <Box sx={{
            position: 'relative',
            flexGrow: 1,
            flexDirection: 'column',
            display: 'flex',
          }}>
            <Typography variant='body1'>content gang?</Typography>
            <div style={{
              width: 1500,
              height: '100%',
            }}>
              <ReactFlow
                nodesConnectable={false}
                elements={elements}
              />
            </div>
          </Box>
        </Box >
      </Paper>
    </Container>
  );
}

export default App;
