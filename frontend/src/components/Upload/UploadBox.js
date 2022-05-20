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

import { postfile } from '../../axios/Upload';

const UploadBox = ()=> {
    const [files,setFiles] = useState("");
    const [text_, setText_] = useState("")
    const dt = null;
    const time = null;
    const [ctime,setTime] = useState(time); 
    const [cdate,setDate] = useState(dt); 
    const inputFile = useRef(null) 

    const changeHandler = (event) => {
        event.preventDefault();
        console.log(event.target.files)
		setFiles(event.target.files[0]);
	};
    const submitHandler = async (event) => {
        
        const data = new FormData() 
        data.append('file', files)
        const result = await postfile(data)

        let dt = new Date().toLocaleDateString();
        setDate(dt);
        let time = new Date().toLocaleTimeString();
        setTime(time);
        alert("upload success")
	};

    // e.preventDefault();
    // const calluploadApi = async (e) => {
    //     const result = await fetch("http://", {
    //             method: "POST",
    //             body: JSON.stringify({
    //                 files:files
    //             }),
    //         });
    //         let resJson = await result.json();
    //         console.log(resJson);
    //         alert(resJson.message);
    // }


    // const uploadHandler = (event) => {
    //     // e.preventDefault();
	// 	setFiles(event.target.files[0]);
	// };
    // const [data, setData] = React.useState(annotation_example[index].data)
    // const [remain, setRemain] = React.useState(annotation_example[index].remain)
  
    // const readFileOnUpload = (uploadedFile) =>{
    //     const fileReader = new FileReader();
    //     fileReader.onloadend = ()=>{
    //        try{
    //           setData(JSON.parse(fileReader.result));
    //           setErrorData(null)
    //        }catch(e){
    //           setErrorData("**Not valid JSON file!**");
    //        }
    //     }
    //     if( uploadedFile!== undefined)
    //        fileReader.readAsText(uploadedFile);
    // }

  
    return (
        <Grid container rowSpacing={3} columnSpacing={{ xs: 1, sm: 1, md: 1 }} >
          
          {/*時間 推文數 ID */}
          <Grid item xs={5} >
              <Paper sx={{ width: '50%', height:'60px', overflow: 'hidden', display: 'flex', justifyContent: "center" , alignItems: "center"}}>
                  {/*<Title>時間:{props.content["time"]}</Title> */}
                  <Title>上傳檔案 </Title>  
              </Paper>
          </Grid>
          <Grid item xs={5}>
              {/* Intentionally Empty */}
          </Grid>
          {/* <Grid item xs={2} >
              <Paper sx={{ width: '100%', height:'60px',overflow: 'hidden', display: 'flex', justifyContent: "center" ,alignItems: "center"}}>
                  <IconButton style={{ fontSize: '20px' }} onClick={()=>inputFile.current.click()}>
                      選擇檔案 < FileUploadIcon/>
                  </IconButton>
                  <button className='Btn SurveyOptionBtn' onClick={()=>inputFile.current.click()}>選擇檔案</button> 
              </Paper>
          </Grid> */}
          
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
                                {/* <button className='Btn SurveyOptionBtn' onClick={()=>inputFile.current.click()}>選擇檔案</button> */}
                            </Paper>
                            <Typography>&nbsp;</Typography>
                            <Typography component="Text" variant='h9' style={{display: 'flex', justifyContent: "center" ,alignItems: 'center',flexWrap: 'wrap',}}>
                                <AttachFileIcon/> {files.name}
                            </Typography>

                            <div className="input_content">
                                <h4>備註</h4>
                                <div className='comment-content'>
                                    <input style={{width:'60%' ,margin:"5px 0px 0px 1px"}} type="text" value={text_} placeholder="備註" onChange={(e) => setText_(e.target.value)} className="inputbar"/>
                                </div>
                            </div>
                            {/* <div className="input_content"> */}
                                {/* <div className="content">
                                    <p>Filename: {files.name}</p>
                                    <p>Filetype: {files.type}</p>
                                    <p>Size in bytes: {files.size}</p>
                                </div> */}
                                {/* <Typography component="Text" variant='h8' style={{display: 'flex', alignItems: 'left',flexWrap: 'wrap',position:'absolute'}}>
                                    <AttachFileIcon/> Filename: {files.name}
                                </Typography> */}
                            {/* </div> */}
                            <Paper sx={{ width: '25%', height:'50px',overflow: 'hidden', display: 'flex', justifyContent: "center" ,alignItems: "center",margin:"30px 0px 0px 70px"}}>
                                <IconButton style={{ fontSize: '15px' }} onClick={submitHandler}>
                                    Submit <AddIcon/>
                                </IconButton>
                                {/* <button className='Btn SurveyOptionBtn' onClick={()=>inputFile.current.click()}>選擇檔案</button> */}
                            </Paper>
                            {/* <div className="input_content">
                                <div>
                                    <p>Date: {cdate}</p>
                                    <p>Time: {ctime}</p>
                                </div>
                            </div> */}
                        </Paper>
                    </Grid>
                      {/*props.content['title']*/}
                      <div className="input_content">
                            <div>
                             {/* <input className='Btn SurveyOptionBtn' ref={inputFile} type="file" name="myImage" onChange={changeHandler} style={{display:'none'}}/> */}
                             {/* <button className='Btn SurveyOptionBtn' onClick={submitHandler}>submit</button> */}
                            </div>
                            {/* <div>
                                <p>Filename: {files.name}</p>
 					            <p>Filetype: {files.type}</p>
 					            <p>Size in bytes: {files.size}</p>
                           </div> */}
                      </div>
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
            </Paper>
          </Grid>
        </Grid>
    );
//     const [selectedFile, setSelectedFile] = React.useState(null);

//     const handleSubmit = (event) => {
//         event.preventDefault()
//         const formData = new FormData();
//         formData.append("selectedFile", selectedFile);
//         try {
//             const response = await axios({
//                 method: "post",
//                 url: "/api/upload/file",
//                 data: formData,
//                 headers: { "Content-Type": "multipart/form-data" },
//             });
//         } catch(error) {
//         console.log(error)
//         }
//     } 

//     const handleFileSelect = (event) => {
//         setSelectedFile(event.target.files[0])
//     }

//   return (
//     <form onSubmit={handleSubmit}>
//       <input type="file" onChange={handleFileSelect}/>
//       <input type="submit" value="Upload File" />
//     </form>
//   )
// }
  
// export default UploadBox;

// const UploadBox = () => {
//     const [files, setFiles] = useState("");
//     // const [image, setImage] = useState({img:null,display:null });
//     const inputFile = useRef(null) 

//     const changeHandler = (event) => {
// 		setFiles(event.target.files[0]);
// 	};
        

//         return(
//             <div className="input_content">
//                     <h3>檔案上傳</h3>
//                         <div>
//                             <input className='Btn SurveyOptionBtn' ref={inputFile} type="file" name="myImage" onChange={changeHandler} style={{display:'none'}}/>
//                             <button className='Btn SurveyOptionBtn' onClick={()=>inputFile.current.click()}>選擇檔案</button>
//                         </div>
//                         <br/>
//                         <div>
//                             <p>Filename: {files.name}</p>
// 					        <p>Filetype: {files.type}</p>
// 					        <p>Size in bytes: {files.size}</p>
//                         </div>
//             </div>


//     );


}
export default UploadBox;