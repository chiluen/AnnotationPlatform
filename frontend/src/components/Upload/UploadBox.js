import * as React from 'react';
import {useRef } from 'react';
import { useState } from "react";
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Title from './Title';
import Paper from '@mui/material/Paper';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import IconButton from '@mui/material/IconButton';
import DoneIcon from '@mui/icons-material/Done';
import CardContent from '@mui/material/CardContent';
import AddIcon from '@mui/icons-material/Add';
import AttachFileIcon from '@mui/icons-material/AttachFile';
// import { Box } from '@mui/system';

// import Button from '@mui/material/Button';
// import SendIcon from '@mui/icons-material/Send';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';

import { postfile, postselecttableinfo  } from '../../axios/Upload';

const constructSelect = (label, func, options)=>{
    return(
        <FormControl fullWidth variant="standard" size="small"  enctype="multipart/form-data">
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

const UploadBox = ()=> {
    const [files,setFiles] = useState("");
    const dt = null;
    const time = null;
    const [ctime,setTime] = useState(time); 
    const [cdate,setDate] = useState(dt); 
    const [category, setcategory] = React.useState('');
    const inputFile = useRef(null) 

    // const handleChange = (event) => {
    //     setCategory(event.target.value);
    // };

    const changeHandler = (event) => {
        event.preventDefault();
        console.log(event.target.files)
		setFiles(event.target.files[0]);
	};

    // const[agree, setAgree] = useState(null);


    const submitHandler = async (event) => {
        
        const data = new FormData() 
        data.append('file', files)
        const result = await postfile(data)

        // setAgree(true);

        let dt = new Date().toLocaleDateString();
        setDate(dt);
        let time = new Date().toLocaleTimeString();
        setTime(time);
        // if (data.status === 200){
        //     // callrefresh("reload");
        //     console.log("upload success")
        // }
        alert("upload success")
    
        const categorydata = await postselecttableinfo(category)
    
	};
  
    return (
        <Grid container rowSpacing={3} columnSpacing={{ xs: 1, sm: 1, md: 1 }} >
          <Grid item xs={5} >
              <Paper sx={{ width: '50%', height:'60px', overflow: 'hidden', display: 'flex', justifyContent: "center" , alignItems: "center"}}>
                  <Title>上傳檔案 </Title>  
              </Paper>
          </Grid>
          <Grid item xs={8}>
              <Paper elevation={5} sx={{ width: '100%', height:'100%', overflow: 'auto', padding: "20px 20px 20px 20px"}}> {/*overflow可以自動產生scroll bar */}
                  <Typography>
                    <CardContent>
                        <Title>注意事項</Title>
                        <Paper className='notice' sx={{ width: '60%', height:'120px', display: 'flex', justifyContent: "center" ,alignItems: "left"}}>
                            <Typography component="p" variant='h6' style={{display: 'flex', alignItems: 'center',flexWrap: 'wrap',}}>
                                <DoneIcon/> 注意上傳格式
                            </Typography>
                            <Typography component="p" variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                                <DoneIcon/>檔名
                            </Typography>
                            <Typography component="p" variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                                <DoneIcon/>vvvvv
                            </Typography>
                        </Paper>
                    </CardContent >  
                    <Grid item xs={20} container={true}>
                        <Paper sx={{width:"800%",height:'350px',margin:"0px 0px 0px 15px"}}>
                            <Paper sx={{ width: '80%', height:'60px',overflow: 'hidden', display: 'flex', justifyContent: "center" ,alignItems: "center",margin:"20px 0px 0px 70px"}}>
                                <IconButton style={{ fontSize: '20px' }} onClick={()=>inputFile.current.click()}>
                                    選擇檔案 < FileUploadIcon/>
                                </IconButton>
                                <input className='Btn SurveyOptionBtn' ref={inputFile} type="file" name="myImage" onChange={changeHandler} style={{display:'none'}}/>
                            </Paper>
                            <Typography>&nbsp;</Typography>
                            <Typography component="Text" variant='h9' style={{display: 'flex', justifyContent: "center" ,alignItems: 'center',flexWrap: 'wrap',}}>
                                <AttachFileIcon/> {files.name}
                            </Typography>

                            <div className="input_content">
                                <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 1, md: 1 }} >
                                    <Grid item xs={8} style={{margin:"30px 0px 0px 60px"}}>
                                        {constructSelect("Category", setcategory, ["Finance","Sports","Technology","Science","Other"])}
                                    </Grid>
                                </Grid>
                                <Paper sx={{ width: '25%', height:'50px',overflow: 'hidden', display: 'flex', justifyContent: "center" ,alignItems: "center",margin:"40px 0px 0px 140px"}}>
                                    <IconButton style={{ fontSize: '15px' }} name='comment' onClick={submitHandler}>
                                        Submit <AddIcon/>
                                    </IconButton>
                                </Paper>
                            </div>
                        </Paper>
                    </Grid>
                  </Typography>
              
              </Paper>
              <Paper elevation={5}sx={{ width: '100%' }}>       
              </Paper>
          </Grid>
          <Grid container item xs={4}>
            <Paper className='check' sx={{ width: '330px', height:'250px', overflow: 'hidden', display: 'flex', justifyContent: "center" , alignItems: "center",margin:"0px 0px 0px 20px"}}>
                <Typography component="Text" variant='h9' style={{display: 'flex', alignItems: 'left',flexWrap: 'wrap',}}>
                    **這裡會顯示上傳狀態
                </Typography>
                <Typography component="Text" variant='h9' style={{display: 'flex', alignItems: 'left',flexWrap: 'wrap',}}>
                    Date {cdate}
                </Typography>
                <Typography component="Text" variant='h9' style={{display: 'flex', alignItems: 'left',flexWrap: 'wrap',}}>
                    Time {ctime}
                </Typography>
                {/* {agree && <h>{text_}</h>} */}
            </Paper>
          </Grid>
        </Grid>
    );

}
export default UploadBox;