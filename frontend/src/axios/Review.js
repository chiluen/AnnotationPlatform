import instance from './api'

const postreviewtext = async (payload)=>{
    const data = await instance.post('review/postreview', payload)
}

const getreviewtext = async ()=>{
    const data = await instance.get('review/getreview')
    return data.data
}

export {postreviewtext, getreviewtext}