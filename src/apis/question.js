import ajax from './config'
export default{
    getquestioninfo(data){
        return ajax.post('/questioninfo',data)
    },
    getquestionlist(data){
        return ajax.post('/questionlist',data)
    },
    addquestion(data){
        return ajax.post('/addquestion',data)
    },
    getwronginfo(data){
        return ajax.post('/wronginfo',data)
    },
    getwronglist(data){
        return ajax.post('/wronglist',data)
    },
    getwronglistforhome(data){
        return ajax.post('/wronglistforhome',data)
    },
    getwronglistbyuserid(data){
        return ajax.post('/wronglistbyuserid',data)
    },
    addwrong(data){
        return ajax.post('/addwrong',data)
    },
    deletewrong(data){
        return ajax.post('/deletewrong',data)
    },
    getcollectinfo(data){
        return ajax.post('/collectinfo',data)
    },
    getcollectlist(data){
        return ajax.post('/collectlist',data)
    },
    addcollect(data){
        return ajax.post('/addcollect',data)
    },
    deletecollect(data){
        return ajax.post('/deletecollect',data)
    },
}