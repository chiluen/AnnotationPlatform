import instance from './api'

const postannotationtext = async (payload, user)=>{
    const data = await instance.post('annotation/postannotation', payload, {params:{user:user}})
}

const getannotationtext = async (user)=>{
    
    const data = await instance.get('annotation/getannotation', {params:{user:user}})
    return data.data
}

export {postannotationtext, getannotationtext}