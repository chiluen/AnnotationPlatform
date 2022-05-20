import instance from './api'

const postfile = async (payload)=>{
    const data = await instance.post('upload/upload', payload)
}

export {postfile}