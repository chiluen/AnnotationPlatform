import * as React from 'react';
import { Bar } from "react-chartjs-2";
import 'chart.js/auto' //這一定要加
import { getfinishpercentage } from '../../axios/Mainpage';
import { state_sample } from '../../test_data';

const options = {
  plugins:{
    title: {
      display: true,
      text: '私有檔案已完成標注比率', //你的資料已完成annotate加上review的比率
      font: {
        size: 15,
        color: '0000'
      },
    },
  },
  maintainAspectRatio: false, //要加上這個，然後用div就可以調整資料了
  indexAxis: 'y',
  scales: {
    x: {
      stacked: true,
    },
    y: {
      stacked: true
    }
  }
}
const state_template = {
  labels: ["Percentage"],
  datasets: [
    {
      label: 'Finish',
      backgroundColor: "#FEC5BB", 
      borderColor: 'rgba(0,0,0,1)',
      borderWidth: 2,
      data: [0]
    },
    {
      label: 'Unfinish',
      backgroundColor: "#FAE1DD", 
      borderColor: 'rgba(0,0,0,1)',
      borderWidth: 2,
      data: [0]
    }
  ]
}

const Bargraph = () => {
  const [state, setstate] = React.useState(state_template)

  React.useEffect(async ()=>{
    const {finish, unfinish} = await getfinishpercentage()
    const state_template = {
      labels: ["Percentage"],
      datasets: [
        {
          label: 'Finish',
          backgroundColor: "#FEC5BB", 
          borderColor: 'rgba(0,0,0,1)',
          borderWidth: 2,
          data: [finish]
        },
        {
          label: 'Unfinish',
          backgroundColor: "#FAE1DD", 
          borderColor: 'rgba(0,0,0,1)',
          borderWidth: 2,
          data: [unfinish]
        }
      ]
    }
    setstate(state_template)
  },[])

  return (
      <div style={{height:"300px"}}>
        <Bar 
        options={options}
        data={state}
        />
        
      </div>
  );
}

export default Bargraph;





