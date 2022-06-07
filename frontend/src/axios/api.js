import axios from 'axios'
const instance = axios.create({baseURL:'http://192.168.49.2:30001'})

export default instance;