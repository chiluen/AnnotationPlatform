import * as React from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

import DashboardIcon from '@mui/icons-material/Dashboard';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import EditIcon from '@mui/icons-material/Edit';
import GradingIcon from '@mui/icons-material/Grading';
import StorageIcon from '@mui/icons-material/Storage';

const MainListItems = (props) =>{
  return(
    <div>
      <ListItem button onClick={()=>{props.func(0)}}>
        <ListItemIcon>
          <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Main Page" />
      </ListItem>
      <ListItem button onClick={()=>{props.func(1)}}>
        <ListItemIcon>
          <CloudUploadIcon />
        </ListItemIcon>
        <ListItemText primary="Upload" />
      </ListItem>
      <ListItem button onClick={()=>{props.func(2)}}>
        <ListItemIcon>
          <EditIcon/>
        </ListItemIcon>
        <ListItemText primary="Annotation" />
      </ListItem>
      <ListItem button onClick={()=>{props.func(3)}}>
        <ListItemIcon>
          <GradingIcon/>
        </ListItemIcon>
        <ListItemText primary="Review" />
      </ListItem>
      <ListItem button onClick={()=>{props.func(4)}}>
        <ListItemIcon>
          <StorageIcon/>
        </ListItemIcon>
        <ListItemText primary="DB" />
      </ListItem>
    </div>
  )
}
export default MainListItems

