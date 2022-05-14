import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';

import IconButton from '@mui/material/IconButton';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import BottomNavigation from '@mui/material/BottomNavigation';
import BottomNavigationAction from '@mui/material/BottomNavigationAction';

import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import SentimentNeutralIcon from '@mui/icons-material/SentimentNeutral';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';

import { annotation_example } from '../../test_data';

var index = 0; // for testing


const AnnotationBox = ()=> {

  const [data, setData] = React.useState(annotation_example[index].data)
  const [remain, setRemain] = React.useState(annotation_example[index].remain)

  //一共有skip, positive, neurtal, negative四種選項，先回傳給DB，然後再改變文章
  const changeText = (decision) =>{
    /**
     Todo:
     send decision to the backend and receive new data
    */
    index = (index+1) % 3;
    setData(annotation_example[index].data);
    setRemain(annotation_example[index].remain)
    console.log("here")
  }

  return (
    <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 1, md: 1 }} >
        
        {/*時間 推文數 ID */}
        <Grid item xs={5} >
            <Paper sx={{ width: '100%', height:'60px', overflow: 'hidden', display: 'flex', justifyContent: "center" , alignItems: "center"}}>
                {/*<Title>時間:{props.content["time"]}</Title> */}
                <Title>剩餘可標註篇數: {remain} </Title>  
            </Paper>
        </Grid>
        <Grid item xs={5}>
            {/* Intentionally Empty */}
        </Grid>
        <Grid item xs={2} >
            <Paper sx={{ width: '100%', height:'60px', overflow: 'hidden', display: 'flex', justifyContent: "center" , alignItems: "center"}}>
                <IconButton aria-label="delete" onClick={()=>{changeText("skip")}}>
                    SKIP <SkipNextIcon/>

                </IconButton>
            </Paper>
        </Grid>
        
        <Grid item xs={12} >
            <Paper elevation={5} sx={{ width: '100%', height:'30rem', overflow: 'auto', padding: "20px 20px 20px 20px"}}> {/*overflow可以自動產生scroll bar */}
                <Typography component="p" variant="h4">
                    {/*props.content['title']*/}
                    {data}
                </Typography>
            
            </Paper>
            <Paper elevation={5}sx={{ width: '100%' }}> 
                <BottomNavigation showLabels>
                        <BottomNavigationAction label="Positive" icon={<SentimentSatisfiedAltIcon />}     onClick={()=>{changeText("Positive")}} />
                        <BottomNavigationAction label="Neutral"  icon={<SentimentNeutralIcon />}          onClick={()=>{changeText("Neutral")}}/>
                        <BottomNavigationAction label="Negative" icon={<SentimentVeryDissatisfiedIcon />} onClick={()=>{changeText("Negative")}}/>
                </BottomNavigation>
            </Paper>
        </Grid>
    </Grid>
  );
}

export default AnnotationBox;