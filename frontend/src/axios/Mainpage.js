import instance from './api'

const getuserprofile = async (name)=>{
    const {data:{user,
                 numberOfUpload,
                 numberOfReview,
                 reviewRank}} = await instance.get('/mainpage/userprofile', {params:{ user:name }});
    
    return {user, numberOfUpload, numberOfReview, reviewRank}
}

const getfinishpercentage = async (user)=>{
    const{data:{finish, unfinish}} = await instance.get('/mainpage/finishinfo', {params:{user:user}});
    return {finish, unfinish}
}

const getdbstat = async (user)=>{
    const data = await instance.get('mainpage/dbstat', {params:{user:user}})
    return data.data
}

const getpieinfo = async (user)=>{
    const data = await instance.get('mainpage/pieinfo', {params:{user:user}})
    return data.data
}

const gettableinfo = async (user)=>{
    const data = await instance.get('mainpage/tableinfo', {params:{user:user}})
    return data.data
}

export {getuserprofile, getfinishpercentage, getdbstat, getpieinfo, gettableinfo}