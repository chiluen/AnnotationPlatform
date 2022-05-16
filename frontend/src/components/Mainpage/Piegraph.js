import * as React from 'react';
import { Doughnut } from "react-chartjs-2";
import 'chart.js/auto' //這一定要加
import { getpieinfo } from '../../axios/Mainpage';

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

const datasets_sample = [
  {
    data: [0,0,0,0,0,0],
    backgroundColor: ["#FEC5BB", "#FAE1DD", "#E8E8E4", "#ECE4DB", "#FFE5D9"]
  }
]

const Piegraph = () => {
  const [datasets, setdataset] = React.useState(datasets_sample)

  React.useEffect( async()=>{
    
    let data = await getpieinfo("all")
    const new_data = [{data:[data['five_star'], data['four_star'], data['three_star'], data['two_star'], data['one_star'], data['zero_star']],
                      backgroundColor: ["#FEC5BB", "#FAE1DD", "#E8E8E4", "#ECE4DB", "#FFE5D9"]
                      }]
    setdataset(new_data)
  },[])

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