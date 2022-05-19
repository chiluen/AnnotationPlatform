import '../css/Upload.css';
import * as React from 'react';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
// import Paper from '@mui/material/Paper';
import UploadBox from '../components/Upload/UploadBox'

const Upload = ()=>{
    return(
        <Box
        component="main"
        sx={{
          backgroundColor: (theme) =>
            theme.palette.mode === 'light'
              ? theme.palette.grey[100]
              : theme.palette.grey[900],
          flexGrow: 1,
          height: '100vh',
          overflow: 'auto',
        }}
      >
        <Toolbar />
        <Container maxWidth="lg" sx={{ mt: 4, mb: 5 }}>
          <Grid container rowSpacing={5} columnSpacing={{ xs: 30, sm: 30, md: 53}} > 
            <Grid item xs={12}>
                <UploadBox/>
            </Grid>
          </Grid>
          
        </Container>
      </Box>
    )
}

export default Upload;