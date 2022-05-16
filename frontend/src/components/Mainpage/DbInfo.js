import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { getdbstat } from '../../axios/Mainpage';

const db_sample = {
    avg_words:0,
    positive_rate:0,
    total_data:0
}

const DbInfo = () => {
    const [datas, setdatas] = React.useState(db_sample);

    React.useEffect( async()=>{
        const data = await getdbstat()
        setdatas(data)
    },[])

    return (
        <div>
            <Typography style={{ fontSize:20}} sx={{ mt: 1 }} variant="h5" component="div" align="center">
                Database統計數據
            </Typography>
            <List>
                <ListItem>
                    <ListItemIcon>
                        <CheckCircleOutlineIcon style={{fill: "#FEC89A"}}/>
                    </ListItemIcon>
                    <ListItemText 
                        align="left"
                        primary={<Typography style={{fontSize:18}}>平均詞數量: {datas['avg_words']}</Typography>}
                    />
                </ListItem>
                <ListItem>
                    <ListItemIcon>
                        <CheckCircleOutlineIcon style={{fill: "#FEC89A"}}/>
                    </ListItemIcon>
                    <ListItemText 
                        align="left"
                        primary={<Typography style={{fontSize:18}}>正向比例: {datas['positive_rate']}%</Typography>}
                    />
                </ListItem>
                <ListItem>
                    <ListItemIcon>
                        <CheckCircleOutlineIcon style={{fill: "#FEC89A"}}/>
                    </ListItemIcon>
                    <ListItemText 
                        align="left"
                        primary={<Typography style={{fontSize:18}}>總共筆數: {datas['total_data']}</Typography>}
                    />
                </ListItem>

            </List>
        </div>
    );
}
export default DbInfo;