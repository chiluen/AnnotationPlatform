import * as React from 'react';
import { Doughnut } from "react-chartjs-2";
import 'chart.js/auto' //這一定要加
//import { getclassification } from '../../axios/Page_1_axios';

import { datasets_sample } from '../../test_data';

const labels = ["5 stars", "4 stars", "3 stars", "2 stars", "1 stars", "0 stars"]

const options = {
  maintainAspectRatio : false,
  plugins:{
    title: {
      display: true,
      text: '私有檔案品質',
      font: {
        size: 15
      },
    },
    legend:{
      display:true,
      position:'right'
    }
  },
}
const Piegraph = () => {
  const [datasets, setdataset] = React.useState(datasets_sample)

  // React.useEffect( async()=>{
  //   //抓目前所有的資料
  //   let data = await getclassification("all")
  //   let new_data = [
  //     {
  //       data:[data["體育"], data["社會"], data["娛樂"], data["教育"], data["財經"], data["家居"], data["科技"]],
  //       backgroundColor: ["#FEC5BB", "#FAE1DD", "#E8E8E4", "#ECE4DB", "#FFE5D9","#FFD7BA","#FEC89A"]
  //     }
  //   ]
  //   setdataset(new_data)
  // },[])

  return (
      <div style={{height:"300px"}}>
        <Doughnut
        options={options}
        data={{
            labels: labels,
            datasets: datasets
        }}
        />
      </div>
  );
}

export default Piegraph;