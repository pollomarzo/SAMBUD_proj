import React, { useState, useEffect } from 'react';
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
import { useReadCypher, useLazyReadCypher } from 'use-neo4j'
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import * as QUERIES from './queries.json'

const QueryList = ({ setResult, setElements }) => {
    // initialize all queries to be run on button press
    const [positives, dataPositives] = useLazyReadCypher(QUERIES.CONTACT_POSITIVES);
    console.log(dataPositives)

    const handlePositives = e => {
        e.preventDefault()
        console.log("running query...")
        positives()
            .then(res => {
                res && console.log(`result is `, res)
                setResult(res.records)
                // setElements([...res.records.map(record => {
                //     const item = record.get('p');
                //     return {
                //         id: item.identity.low,
                //         data: { label: item.properties.Name },
                //         position: { x: 100, y: 125 },
                //     }
                // })])
            })
            .catch(e => console.error(e))
    }


    // rolled up version for later
    // const blocks = [
    //     {
    //         id: "01",
    //         name: "fetch all items",
    //         description: "this query fetches all items in the database",
    //         query: "MATCH...",
    //     }
    // ];
    // let queryFuns = [];
    // for (let i = 0; i < blocks.length; i++) {
    //     queryFuns.append(useLazyReadCypher(blocks[i].query));
    // };

    return (
        <List sx={{
            maxHeight: '100vh',
            overflow: 'auto',
            flexBasis: 350,
            flexShrink: 0,
            marginRight: '2vh',
        }}>
            <ListItem>
                <ListItemText primary="fetch all positives" />
                <ListItemSecondaryAction>
                    <Tooltip title="run query">
                        <IconButton edge="end" aria-label="run" onClick={handlePositives}>
                            <PlayArrowIcon />
                        </IconButton>
                    </Tooltip>
                </ListItemSecondaryAction>
            </ListItem>
            {/* {blocks.map((block, index) => (
            <Box key={block.id}  >
                <ListItem
                    sx={{
                        boxSizing: 'border-box',
                        maxWidth: 350,
                        paddingTop: 2,
                        paddingBottom: 2,
                        border: '1px solid black',
                        cornerRadius: '2px',
                        display: 'flex',
                        alignItems: 'center',
                        cursor: 'pointer',
                        overflow: 'hidden',
                    }}
                    onClick={() => setSelected(block)}
                >
                    <ListItemText
                        primary={block.name}
                        primaryTypographyProps={{ variant: 'subtitle1' }}
                    />
                </ListItem> 
        {index !== blocks.length - 1 && <Divider />}
    </Box>
                ))}*/}
        </List>)

}
export default QueryList;