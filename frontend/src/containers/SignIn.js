import '../css/SignIn.css';
import * as React from 'react';
import { useState } from "react";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import { Button } from '@mui/material';
import { getsigninresult } from '../axios/Signin';

const SignIn = (props) => {
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");

  //登入
  const callLoginApi = async (e) => {
    e.preventDefault();

    const payload = { 
      user: user,
      password: password
    }

    const login_info = await getsigninresult(payload)
    
    if (login_info.result){
      props.func("dashboard");
      props.func_2(user)
      alert("歡迎使用Annotation Platform!");
    }
    else{
      setUser("")
      setPassword("")
      alert("用戶名稱或密碼錯誤")
    }
  };

  const [values, setValues] = React.useState({
    password: "",
    showPassword: false,
  });

  const handleClickShowPassword = () => {
    setValues({ ...values, showPassword: !values.showPassword });
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <div className="backscreen">
      <div className='screen'>
        <div className="card_container" align='center'>
            <div className="card_center">
              <div className="input_content">
                <h4>使用者名稱</h4>
                <div className='password-content'>
                    <input type="text" value={user} placeholder="Username" onChange={(e) => setUser(e.target.value)} className="inputbar"/>
                  </div>
              </div>
              <p></p>
              <div className="input_content">
                <h4>密碼</h4>
                  <div className='password-content'>
                    <input type={values.showPassword ? "text" : "password"} value={password} placeholder="Password" 
                    onChange={(e) => setPassword(e.target.value)} className="inputbar"/>
                    <button className='eye' onClick={handleClickShowPassword} onMouseDown={handleMouseDownPassword}>
                      {values.showPassword ? <VisibilityIcon size='20px'/> : <VisibilityOffIcon size='20px'/>}
                    </button>
                  </div>
              </div>
              <div>
                <br/>
                <Box   display="flex" justifyContent="center" alignItems="center">
                  <Button     style={{color: 'black', backgroundColor: "#FFEEDD"}}variant="contained"onClick={callLoginApi} >登入</Button>
                </Box>
                <br/>
                <Box display="flex" justifyContent="center" alignItems="center">
                  <Link component="button" variant="body2"
                    onClick={() => {
                      props.func("register");;
                    }}
                  >{'註冊'}</Link>
                </Box>
              </div>
            </div>                        
        </div>
      </div>
    </div>
  );
}
export default SignIn ;


