import instance from './api'

const postreviewtext = async (payload, user)=>{
    const data = await instance.post('review/postreview', payload, {params:{user:user}})
}

const getreviewtext = async (user)=>{
    const data = await instance.get('review/getreview', {params:{user:user}})
    return data.data
}

export {postreviewtext, getreviewtext}