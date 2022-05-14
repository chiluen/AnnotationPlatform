import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
//import { gethottitle } from '../../axios/Page_1_axios';

import { db_sample } from '../../test_data';




const DbInfo = () => {
    const [datas, setdatas] = React.useState(db_sample);
    const [secondary, setSecondary] = React.useState();

    // React.useEffect( async()=>{
    //     const data = await gethottitle()
    //     setdatas([data["0"], data["1"], data["2"], data["3"]])
    // },[])

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
                        primary={<Typography style={{fontSize:18}}>平均詞數量: {datas[0]}</Typography>}
                    />
                </ListItem>
                <ListItem>
                    <ListItemIcon>
                        <CheckCircleOutlineIcon style={{fill: "#FEC89A"}}/>
                    </ListItemIcon>
                    <ListItemText 
                        align="left"
                        primary={<Typography style={{fontSize:18}}>正向比例: {datas[1]}</Typography>}
                    />
                </ListItem>
                <ListItem>
                    <ListItemIcon>
                        <CheckCircleOutlineIcon style={{fill: "#FEC89A"}}/>
                    </ListItemIcon>
                    <ListItemText 
                        align="left"
                        primary={<Typography style={{fontSize:18}}>總共筆數: {datas[2]}</Typography>}
                    />
                </ListItem>

            </List>
        </div>
    );
}
export default DbInfo;