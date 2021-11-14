import React, { useState, useEffect, useContext } from "react";
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
  Button,
  TextField,
  Switch,
  FormControlLabel,
  Collapse,
} from "@mui/material";
import { useReadCypher, useLazyReadCypher, Neo4jContext } from "use-neo4j";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import QUERIES from "./queries.json";

const QueryList = ({ setResult, setElements }) => {
  const [personalQuery, setPersonalQuery] = useState("");
  const [graphSwitch, setGraphSwitch] = useState(false);
  const [open, setOpen] = useState(undefined);

  const { driver } = useContext(Neo4jContext);
  // initialize all queries to be run on button press
  let queriesList = [];
  let queryFunction, queryData;
  for (let query of QUERIES) {
    // i know, i shouldn't call hooks in a loop. this never changes though. order is ensured
    // eslint-disable-next-line
    [queryFunction, queryData] = useLazyReadCypher(query.cypher);
    queriesList.push({
      name: query.name,
      execute: queryFunction,
      data: queryData,
      cypher: query.cypher,
      view: query.view,
      description: query.description,
      displayName: query.displayName,
    });
  }

  const handleQuery = (e, query) => {
    e.preventDefault();
    console.log("running query...");
    query
      .execute()
      .then((res) => {
        res && console.log(`result is `, res);
        setResult({
          records: res.records,
          view: query.view,
          cypher: query.cypher,
        });
      })
      .catch((e) => {
        setResult({
          error: "Something went wrong. Try giving it another go?",
        });
        console.error(e);
      });
  };

  const runPersonalQuery = () => {
    console.log("running personal query...");
    driver
      .session()
      .run(personalQuery)
      .then((res) => {
        res && console.log(`result is `, res);
        setResult({
          records: res.records,
          view: graphSwitch ? "graph" : "table",
          query: personalQuery,
        });
      })
      .catch((e) => {
        setResult({
          error: "Something went wrong. Try giving it another go?",
        });
        console.error(e);
      });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <List
        sx={{
          height: "50vh",
          overflow: "auto",
          flexBasis: 350,
          flexShrink: 0,
          marginRight: "2vh",
        }}
      >
        {queriesList.map((query, idx) => (
          <div
            key={idx}
            style={{
              border: "1px solid #000",
              borderRadius: "0.8",
              cursor: "pointer",
              userSelect: "none",
            }}
            onClick={() => (open === idx ? setOpen(undefined) : setOpen(idx))}
          >
            <ListItem>
              <ListItemText>
                <Typography>{query.displayName}</Typography>
              </ListItemText>
              <ListItemSecondaryAction>
                <Tooltip title="run query">
                  <IconButton
                    edge="end"
                    aria-label="run"
                    onClick={(e) => {
                      handleQuery(e, query);
                    }}
                  >
                    <PlayArrowIcon />
                  </IconButton>
                </Tooltip>
              </ListItemSecondaryAction>
            </ListItem>
            <Collapse in={open === idx} timeout="auto" unmountOnExit>
              <div style={{ marginLeft: 10 }}>YOYO</div>
            </Collapse>
          </div>
        ))}
      </List>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          paddingLeft: "2vh",
        }}
      >
        <TextField
          multiline
          minRows={5}
          placeholder="enter your own query"
          value={personalQuery}
          onChange={(e) => setPersonalQuery(e.target.value)}
        />
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            width: "15vw",
            paddingLeft: "2vh",
          }}
        >
          <FormControlLabel
            control={
              <Switch
                checked={graphSwitch}
                onChange={() => setGraphSwitch((val) => !val)}
              />
            }
            label={`${graphSwitch ? "Graph" : "Table"}`}
          />
          <Button
            disabled={!personalQuery || personalQuery.length === 0}
            variant="outlined"
            onClick={runPersonalQuery}
          >
            Run query
          </Button>
        </div>
      </div>
    </div>
  );
};
export default QueryList;
