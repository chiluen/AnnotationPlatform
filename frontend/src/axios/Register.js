import instance from './api'

const postregister = async (payload)=>{
    const data = await instance.post('register/register', payload)
    return data.data
}

export {postregister}