import instance from './api'

const postfile = async (payload)=>{
    const data = await instance.post('upload/upload', payload)
}

const postselecttableinfo = async (category)=>{
    const data = await instance.post('upload/posttableinfo', {params:{category:category}})
    // return data.data
}

export {postfile,postselecttableinfo}