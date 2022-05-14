import * as React from 'react';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
//import { getuserprofile } from '../../axios/Page_1_axios';
import { NameContext } from '../../App';

import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import GradingIcon from '@mui/icons-material/Grading';
import StarHalfIcon from '@mui/icons-material/StarHalf';
import Rating from '@mui/material/Rating';


import { user_data } from '../../test_data';

const Usercard = ()=>{
    const [dataNum, setdataNum] = React.useState(0)
    const [latest, setlatest] = React.useState("0")

    const timeformat = (latest)=>{
        const ll = new Date(latest)
        const new_time = ll.getFullYear() + "/" + (ll.getMonth()+1) + "/" + ll.getDate() + " " + ll.toISOString().slice(11,16)
        return new_time
    }

    // React.useEffect( async() => {
    //     const {dataNum, latest} = await getuserprofile()
    //     const new_time = timeformat(latest)
    //     setdataNum(dataNum)
    //     setlatest(new_time)
    // },[]);
    
    return(
        <Card sx={{ maxWidth: 400 , maxHeight: 400, height: 300}}>

            <CardContent >
                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <AccountCircleIcon/>  使用者名稱: {user_data.name}
                </Typography>
                <Typography>&nbsp;</Typography>

                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <CloudUploadIcon />  已上傳筆數: {user_data.numberOfUpload}
                </Typography>
                <Typography>&nbsp;</Typography>
                
                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <GradingIcon/>  已評價筆數: {user_data.numberOfReview}
                </Typography>
                <Typography>&nbsp;</Typography>

                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <StarHalfIcon/>  評價星級: <Rating name="half-rating-read" defaultValue={user_data.reviewRank} precision={0.5} readOnly />
                </Typography>
                <Typography>&nbsp;</Typography>

            </CardContent>
        </Card>
    )
}

export default Usercard;



