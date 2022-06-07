import * as React from 'react';
import Dashboard from './containers/Dashboard';
import SignIn from './containers/SignIn';
import Register from './containers/Register';

const NameContext = React.createContext()

const App =() =>{
  const [user,setuser] = React.useState("")
  const [start,setstart] = React.useState(false)
  const [status, setStatus] = React.useState("signin")  //三個status: signin, register, dashboard

  const pageselect = ()=>{
    console.log('Test in App.js')
    console.log(process.env.REACT_APP_HOST_IP_ADDRESS)
    if (status === "signin"){
      return <SignIn func={setStatus} func_2={setuser}/>
    }
    else if(status === "register"){
      return <Register func={setStatus}/>
    }
    else{
      return <Dashboard/>
    }
  }
  
  return (
    <NameContext.Provider value = {user}>
      {pageselect()}
    </NameContext.Provider>
  );
}
export {NameContext};
export default App;
