import instance from './api'

const getsigninresult = async (payload)=>{
    const data = await instance.get('signin/signinresult', {params:{ user:payload.user, password:payload.password }})
    return data.data
}

export {getsigninresult}