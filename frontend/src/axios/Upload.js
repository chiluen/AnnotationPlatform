import instance from './api'

const postfile = async (payload, category,user)=>{
    console.log(payload)
    console.log(category)
    const data = await instance.post('upload/upload', payload, {params:{category:category, user:user}})
}

export {postfile}