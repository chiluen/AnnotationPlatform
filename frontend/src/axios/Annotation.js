import instance from './api'

const postannotationtext = async (payload)=>{
    const data = await instance.post('annotation/postannotation', payload)
}

const getannotationtext = async ()=>{
    const data = await instance.get('annotation/getannotation')
    return data.data
}

export {postannotationtext, getannotationtext}