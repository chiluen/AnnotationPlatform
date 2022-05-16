import instance from './api'

const gettableinfo = async ()=>{
    const data = await instance.get('db/tableinfo')
    return data.data
}

const getselecttableinfo = async (scope, minstar, status)=>{
    const data = await instance.get('db/selecttableinfo', {params:{scope:scope, minstar:minstar, status:status }})
    return data.data
}

export {gettableinfo, getselecttableinfo}