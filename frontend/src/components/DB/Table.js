import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Rating from '@mui/material/Rating';
import { Grid } from '@mui/material';
import { Box } from '@mui/system';

import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';

import { gettableinfo, getselecttableinfo } from '../../axios/DB';

const columns = [
  { id: 'uploader', label: 'Uploader', minWidth:170},
  { id: 'data', label: 'Data', minWidth: 170 },
  { id: 'status', label: 'Positive/ Negative/ Neutral/ Not Graded', minWidth: 100 },
  { id: 'category', label: 'Category', minWidth:170},
  {
    id: 'rank',
    label: 'Review Quality',
    minWidth: 170,
    align: 'right',
    format: (value) => value.toLocaleString('en-US'),
  },
];

const rows_example = [
    {
    data: "",
    status: "X",
    rank: 0
    },
]

const constructSelect = (label, func, options)=>{
    return(
        <FormControl fullWidth>
        <InputLabel>{label}</InputLabel>
            <Select defaultValue="" onChange={(e)=>{func(e.target.value)}}>
                {options.map((option)=>{
                    return(
                         <MenuItem value={option}>{option}</MenuItem>
                    )
                })}
            </Select>
        </FormControl>
    )
}


const StickyHeadTable=() => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [rows, setRows] = React.useState(rows_example);

  const [scope, setScope] = React.useState("self");
  const [minstar, setMinstar] = React.useState(0);
  const [status, setStatus] = React.useState("all");
  const [category_, setCategory] = React.useState("")

  React.useEffect( async()=>{
    const data = await gettableinfo()
    setRows(data)
  },[])

  const handlequery = async()=>{
    //   const data = {
    //       scope: scope,
    //       minstar: minstar,
    //       status: status
    //   }
    //   console.log(data)
    const data = await getselecttableinfo(scope, minstar, status, category_)
    setRows(data)
  }


  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <div>
        <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 1, md: 1 }} >
            <Grid item xs={2} >
                {constructSelect("檔案範圍", setScope, ["self", "all"])}
            </Grid>
            <Grid item xs={2} >
                {constructSelect("最低Review Quality", setMinstar, [0,1,2,3,4,5])}
            </Grid>
            <Grid item xs={2} >
                {constructSelect("標注結果", setStatus, ["Positive", "Neutral", "Negative", "Not Graded","ALL"])}
            </Grid>
            <Grid item xs={2} >
                {constructSelect("分類", setCategory, ["Finance","Sports","Technology","Science","Other"])}
            </Grid>
            <Grid item xs={4} >
                {/*"empty intentionally"*/}
            </Grid>
            <Grid item xs={10} >
                <Box display="flex" justifyContent="flex-end" style={{margin:"-60px 0px 0px 0em"}}>
                    <Button onClick={handlequery}  size="large" variant="contained" endIcon={<SendIcon />}>
                        Search
                    </Button>
                </Box>
            </Grid>
        </Grid>
        <br/>

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
                        <TableCell key='uploader' align='left'>
                            {row['uploader']}
                        </TableCell>
                        <TableCell key='data' align='left'>
                            {row['data']}
                        </TableCell>
                        <TableCell key='status' align='left'>
                            {row['status']}
                        </TableCell>
                        <TableCell key='category' align='left'>
                            {row['tag']}
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
