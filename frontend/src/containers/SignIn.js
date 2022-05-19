import '../css/SignIn.css';
import * as React from 'react';
import { useState } from "react";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';

import { login_data } from '../test_data';

/* 
Todo:
建立一個api 跟後端聯繫並且獲得information

*/

const SignIn = (props) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  //登入
  const callLoginApi = async (e) => {
    e.preventDefault();
    
    if (email === login_data.email && password === login_data.password){
      alert("Welcome");
      // props.func(username);
      props.func(email);
    }
    else
      alert("Wrong username or password")
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
                    <input type="text" value={email} placeholder="Username" onChange={(e) => setEmail(e.target.value)} className="inputbar"/>
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
              <div align="center">
                <button className="submit" onClick={callLoginApi}>登入</button><br/>
              </div>
            </div>                            
        </div>
      </div>
    </div>
  );

}
export default SignIn ;


