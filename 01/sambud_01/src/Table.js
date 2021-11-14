import { TableRow, TableCell, TableHead } from "@mui/material";

import { DataGrid } from "@mui/x-data-grid";

const Table = ({ data }) => {
  console.log(data);

  if (data.error) return <div>{data.error}</div>;
  if (!data.records) return <div>No data...</div>;
  data = data.records;

  const keys = data[0].keys;
  var columns = [];
  for (const key of keys) {
    columns.push({ field: key, flex: 1, minWidth: 100 });
  }
  var rows = [];

  for (let j = 0; j < data.length; j++) {
    rows[j] = [];
    rows[j]["id"] = j;
    for (let i = 0; i < columns.length; i++) {
      rows[j][columns[i].field] = data[j]._fields[i];
    }
  }

  for (let i = 0; i < columns.length; i++) {
    rows[i].id = i;
  }

  return (
    <div style={{ height: "95%", width: "100%" }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={25}
        rowsPerPageOptions={[25]}
      />
    </div>
  );
};

export default Table;
