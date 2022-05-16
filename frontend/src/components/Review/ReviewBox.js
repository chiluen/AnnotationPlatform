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

import { postreviewtext, getreviewtext } from '../../axios/Review';

//import { review_example } from '../../test_data';

const review_example = {
    remain: 0,
    data: "",
    classification: "Positive"
}

var index = 0; // for testing

const ReviewBox = ()=> {

  const [data, setData] = React.useState(review_example.data)
  const [classification, setClassification] = React.useState(review_example.classification)
  const [remain, setRemain] = React.useState(review_example.remain)


  React.useEffect(()=>{
    getText('init')
    console.log("enter use effect")
  },[])

  const getText = async (decision) =>{
    if(decision === 'init' || decision === 'skip'){
        const new_data = await getreviewtext()
        setData(new_data.data)
        setRemain(new_data.remain)
        setClassification(new_data.classification)
    }
    else{ //星星個數
        //先post, 再get
        const payload = { //這邊之後改成傳data ID或許比較好, 傳data太慢了
            data: data,
            decision: decision
        }
        await postreviewtext(payload)
        const new_data = await getreviewtext()
        setData(new_data.data)
        setRemain(new_data.remain)
        setClassification(new_data.classification)
    }
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
                <IconButton aria-label="delete" onClick={()=>{getText("skip")}}>
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
                <Rating onChange={(_, value)=>{getText(value)}}/>
            </Paper>
        </Grid>
        
        
        
    </Grid>
  );
}

export default ReviewBox;