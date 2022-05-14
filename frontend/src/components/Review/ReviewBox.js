import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Rating from '@mui/material/Rating';

import IconButton from '@mui/material/IconButton';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import SentimentNeutralIcon from '@mui/icons-material/SentimentNeutral';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';

import { review_example } from '../../test_data';

var index = 0; // for testing

const ReviewBox = ()=> {

  const [data, setData] = React.useState(review_example[index].data)
  const [classification, setClassification] = React.useState(review_example[index].classification)
  const [remain, setRemain] = React.useState(review_example[index].remain)

  //一共有skip, positive, neurtal, negative四種選項，先回傳給DB，然後再改變文章
  const changeText = (decision) =>{
    /**
     Todo:
     send decision to the backend and receive new data
    */
    index = (index+1) % 3;
    setData(review_example[index].data);
    setRemain(review_example[index].remain)
    setClassification(review_example[index].classification)
    console.log(decision)
  }

  const anootationIcon = (classification)=>{
    if (classification === "Positive"){
        return <div style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}><SentimentSatisfiedAltIcon style={{fontSize: 75}}/>{classification}</div>
    }
    else if(classification === "Negative"){
        return <div style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}><SentimentVeryDissatisfiedIcon style={{fontSize: 75}}/>{classification}</div>
    }
    else{
        return <div style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}><SentimentNeutralIcon style={{fontSize: 75}}/>{classification}</div>
    }
  }
  

  return (
    <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 1, md: 1 }} >
        
        {/*時間 推文數 ID */}
        <Grid item xs={5} >
            <Paper sx={{ width: '100%', height:'60px', overflow: 'hidden', display: 'flex', justifyContent: "center" , alignItems: "center"}}>
                {/*<Title>時間:{props.content["time"]}</Title> */}
                <Title>剩餘可評論篇數: {remain} </Title>  
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
        
        <Grid item xs={9}>
            <Paper elevation={5}  sx={{ width: '100%', height:'30rem', overflow: 'auto', padding: "20px 20px 20px 20px"}}> {/*overflow可以自動產生scroll bar */}
                <Typography component="p" variant="h4">
                    {data}
                </Typography>
            </Paper>
        </Grid>
        <Grid item xs={3}>
            <Paper elevation={5}  xs={4} sx={{ width: '100%', height:'30rem', overflow: 'auto', padding: "20px 20px 20px 20px", display: 'flex', justifyContent: "center" , alignItems: "center"}}> {/*overflow可以自動產生scroll bar */}
                <Typography component="p" variant="h3">
                    {anootationIcon(classification)}
                </Typography>
            </Paper>
        </Grid>
        <Grid item xs={12}>
            <Paper elevation={5}  xs={4} sx={{ width: '100%', height:'5rem', overflow: 'auto', padding: "20px 20px 20px 20px", display: 'flex', justifyContent: "center" , alignItems: "center"}}>
                <Rating onChange={(_, value)=>{changeText(value)}}/>
            </Paper>
        </Grid>
        
        
        
    </Grid>
  );
}

export default ReviewBox;