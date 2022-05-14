import * as React from 'react';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Usercard from '../components/Mainpage/User';
import Piegraph from '../components/Mainpage/Piegraph';
import Bargraph from '../components/Mainpage/Bargraph';
import DbInfo from '../components/Mainpage/DbInfo';
import StickyHeadTable from '../components/Mainpage/Table';

const Mainpage = ()=>{
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
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Grid container rowSpacing={5} columnSpacing={{ xs: 30, sm: 30, md: 53}} > 
            {/* Usercard */}
            <Grid item xs={12} md={4} lg={3}>
              <Paper
                sx={{
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  height: 490,
                  width: 350
                }}
              >
                <Usercard/> 
              </Paper>
            </Grid>

            {/* 主頁右邊的三個grid */}
            <Grid item xs={12} md={6} lg={7}>
              <Grid container rowSpacing={2} columnSpacing={{ xs: 30, sm: 30, md: 30}}>
                  {/*Stack bar */}
                  <Grid item xs={12}>
                    <Paper
                      sx={{
                        p: 2,
                        display: 'flex',
                        flexDirection: 'column',
                        height: 200,
                        width: 700
                      }}
                    >
                      <Bargraph/>
                    </Paper>
                  </Grid>
                  

                  {/*Pie bar */}
                  <Grid item xs={6}>
                    <Paper
                      sx={{
                        p: 2,
                        display: 'flex',
                        flexDirection: 'column',
                        height: 280,
                        width: 350
                      }}
                    >
                      <Piegraph/>
                    </Paper>
                  </Grid>
                  {/*List of db information*/}
                  <Grid item xs={6}>
                    <Paper
                      sx={{
                        p: 2,
                        display: 'flex',
                        flexDirection: 'column',
                        height: 280,
                        width: 335
                      }}
                    >
                      <DbInfo/>
                    </Paper>
                  </Grid>

              </Grid>
            </Grid>
                
            {/* Bar graph */}
            <Grid item xs={12}>
              <StickyHeadTable/>
            </Grid>
          </Grid>
          
        </Container>
      </Box>
    )
}

export default Mainpage;