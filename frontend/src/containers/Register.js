import '../css/Register.css';
import * as React from 'react';
import { useState } from "react";
import Paper from '@mui/material/Paper';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { postregister } from '../axios/Register';

const Register = (props) => {
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  //註冊
  const callRegisterApi = async (e) => {
    e.preventDefault();
    if (password !== password2){
      alert('確認密碼輸入錯誤，請重輸')
      setPassword("")
      setPassword2("")
      return
    }
    const payload = { 
      user: user,
      password: password
    }
    const register_info = await postregister(payload)
    if(register_info.result === "repeat"){
      alert('此名稱已被註冊，請更換名稱')
      setUser("")
      setPassword("")
      setPassword2("")
    }
    else{
      alert('成功註冊')
      props.func("signin")
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

  const [values2, setValues2] = React.useState({
    password: "",
    showPassword: false,
  });

  const handleClickShowPassword2 = () => {
    setValues2({ ...values2, showPassword: !values2.showPassword });
  };
  
  const handleMouseDownPassword2 = (event) => {
    event.preventDefault();
  };

  return (
    <div className="backscreen">
      <div className='screen'>
        <div className="card_container" align='center'>
            <div className="card_center">
            <Paper sx={{ width: '30%', height:'35px', overflow: 'hidden', display: 'flex', justifyContent: "center" , alignItems: "center",margin:"5px 0px 0px 225px"}}>
                  <p>建立帳號 </p>  
            </Paper>
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
              <div className="input_content">
                <h4>確認密碼</h4>
                  <div className='password-content'>
                    <input type={values2.showPassword ? "text" : "password"} value={password2} placeholder="Confirm Password" 
                    onChange={(e) => setPassword2(e.target.value)} className="inputbar"/>
                    <button className='eye' onClick={handleClickShowPassword2} onMouseDown={handleMouseDownPassword2}>
                      {values2.showPassword ? <VisibilityIcon size='20px'/> : <VisibilityOffIcon size='20px'/>}
                    </button>
                  </div>
              </div>
              <div>
                <button className="register" onClick={callRegisterApi}>註冊</button><br/>
              </div>
              {/* <div className='registerPart'> 
                <p className="text">尚未註冊<KeyboardDoubleArrowRightIcon/></p>
                <div>
                  <button className="register" onClick={() => {window.location.href='register'}}>註冊</button><br/>
                </div>
              </div> */}
            </div>                        
        </div>
      </div>
    </div>
  );

}
export default Register ;


