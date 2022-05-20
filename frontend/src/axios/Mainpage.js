import instance from './api'

const getuserprofile = async (name)=>{
    const {data:{user,
                 numberOfUpload,
                 numberOfReview,
                 reviewRank}} = await instance.get('/mainpage/userprofile', {params:{ user:name }});
    
    return {user, numberOfUpload, numberOfReview, reviewRank}
}

const getfinishpercentage = async ()=>{
    const{data:{finish, unfinish}} = await instance.get('/mainpage/finishinfo');
    return {finish, unfinish}
}

const getdbstat = async ()=>{
    const data = await instance.get('mainpage/dbstat')
    return data.data
}

const getpieinfo = async ()=>{
    const data = await instance.get('mainpage/pieinfo')
    return data.data
}

const gettableinfo = async ()=>{
    const data = await instance.get('mainpage/tableinfo')
    return data.data
}

export {getuserprofile, getfinishpercentage, getdbstat, getpieinfo, gettableinfo}