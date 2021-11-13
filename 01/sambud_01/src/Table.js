import {
    TableRow,
    TableCell,
    TableHead
} from '@mui/material';

import { DataGrid } from '@mui/x-data-grid';

const Table = ({ data }) => {
    console.log(data)

    if (!data) return <div>No data...</div>
    console.log(data)
    const keys = data[0].keys
    console.log(keys)
    var columns = []
    for (const key of keys) {
        columns.push({ field: key })
    }
    var rows = []

    for (let j = 0; j < data.length; j++) {
        rows[j] = []
        rows[j]['id'] = j
        for (let i = 0; i < columns.length; i++) {
            rows[j][columns[i].field] = data[j]._fields[i]
        }
    }

    console.log("parsed is", rows)
    for (let i = 0; i < columns.length; i++) {
        rows[i].id = i
    }



    return (
        <DataGrid
            rows={rows}
            columns={columns}
            pageSize={25}
            rowsPerPageOptions={[25]}
        />
    )

    /* return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Dessert (100g serving)</TableCell>
                        <TableCell align="right">Calories</TableCell>
                        <TableCell align="right">Fat&nbsp;(g)</TableCell>
                        <TableCell align="right">Carbs&nbsp;(g)</TableCell>
                        <TableCell align="right">Protein&nbsp;(g)</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <TableRow
                            key={row.name}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">
                                {row.name}
                            </TableCell>
                            <TableCell align="right">{row.calories}</TableCell>
                            <TableCell align="right">{row.fat}</TableCell>
                            <TableCell align="right">{row.carbs}</TableCell>
                            <TableCell align="right">{row.protein}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    ) */
}

export default Table;