import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';

import { gettableinfo } from '../../axios/Mainpage';

const rows_example = [
  {
  data: "",
  status: "X",
  rank: 0
  },
]

const columns = [
  { id: 'data', label: 'Data', minWidth: 170 },
  { id: 'status', label: 'Positive/ Negative/ Neutral/ Not Graded', minWidth: 100 },
  {
    id: 'rank',
    label: 'Review Quality',
    minWidth: 170,
    align: 'right',
    format: (value) => value.toLocaleString('en-US'),
  },
];

const StickyHeadTable=() => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [rows, setRows] = React.useState(rows_example)

  React.useEffect( async()=>{

    const data = await gettableinfo()
    setRows(data)
  },[])

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <div>
        <Typography style={{ fontSize:20}} sx={{ mt: 1 }} variant="h5" component="div" align="center">
            私有檔案概覽
        </Typography>
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer sx={{ maxHeight: 440 }}>
            <Table stickyHeader aria-label="sticky table">
            <TableHead>
                <TableRow>
                {columns.map((column) => (
                    <TableCell
                    key={column.id}
                    align={column.align}
                    style={{ minWidth: column.minWidth }}
                    >
                    {column.label}
                    </TableCell>
                ))}
                </TableRow>
            </TableHead>
            <TableBody>
                {rows
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row) => {
                    return (
                    <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>
                        <TableCell key='data' align='left'>
                            {row['data']}
                        </TableCell>
                        <TableCell key='status' align='left'>
                            {row['status']}
                        </TableCell>
                        <TableCell key='rank' align='right'>
                            <Rating value={Number(row['rank'])} readOnly />
                        </TableCell>

                    </TableRow>
                    );
                })}
            </TableBody>
            </Table>
        </TableContainer>
        <TablePagination
            rowsPerPageOptions={[10, 20, 30]}
            component="div"
            count={rows.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
        />
        </Paper>
    </div>
  );
}
export default StickyHeadTable;
