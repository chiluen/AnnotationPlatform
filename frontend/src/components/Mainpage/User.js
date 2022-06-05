import * as React from 'react';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { getuserprofile } from '../../axios/Mainpage';

import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import GradingIcon from '@mui/icons-material/Grading';
import StarHalfIcon from '@mui/icons-material/StarHalf';
import Rating from '@mui/material/Rating';

const Usercard = (props)=>{
    const [name, setName] = React.useState("")
    const [numberOfUpload, setNumberOfUpload] = React.useState(0)
    const [numberOfReview, setNumberOfReview] = React.useState(0)
    const [reviewRank, setReviewRank] = React.useState(1)


    React.useEffect( async () => {
        if(!props.user){ //這個很重要，因為useEffect在props initialize以前就會啟動
            return
        }
        const {user, numberOfUpload, numberOfReview, reviewRank} = await getuserprofile(props.user)
        setName(user)
        setNumberOfUpload(numberOfUpload)
        setNumberOfReview(numberOfReview)
        setReviewRank(reviewRank)
    },[props.user]);
    
    
    
    return(
        <Card sx={{ maxWidth: 400 , maxHeight: 400, height: 300}}>
            <CardContent >
                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <AccountCircleIcon/>  使用者名稱: {name}
                </Typography>
                <Typography>&nbsp;</Typography>

                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <CloudUploadIcon />  已上傳筆數: {numberOfUpload}
                </Typography>
                <Typography>&nbsp;</Typography>
                
                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <GradingIcon/>  已評價筆數: {numberOfReview}
                </Typography>
                <Typography>&nbsp;</Typography>

                <Typography variant='h6' style={{display: 'flex', alignItems: 'center', flexWrap: 'wrap',}}>
                    <StarHalfIcon/>  評價星級: <Rating name="half-rating-read" value={reviewRank} precision={0.5} readOnly />
                </Typography>
                <Typography>&nbsp;</Typography>

            </CardContent>
        </Card>
    )
}

export default Usercard;



