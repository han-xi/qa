import ajax from './config'
export default{

    getclassinfo(data){
        return ajax.post('/classinfo',data)
    },
    postclassinfo(data){
        return ajax.post('/postclassinfo',data)
    },
    getclasslist(data){
        return ajax.post('/classlist',data)
    },
    getstudentinfo(data){
        return ajax.post('/studentinfo',data)
    },
    getteacherinfo(data){
        return ajax.post('/teacherinfo',data)
    },
    getstudentlist(data){
        return ajax.post('/studentlist',data)
    },
    addclass(data){
        return ajax.post('/addclass',data)
    },
    deleteclass(data){
        return ajax.post('/deleteclass',data)
    },
    addstudent(data){
        return ajax.post('/addstudent',data)
    },
    deletestudent(data){
        return ajax.post('/deletestudent',data)
    },
    addteacher(data){
        return ajax.post('/addteacher',data)
    },
    deleteteacher(data){
        return ajax.post('/deleteteacher',data)
    },
    getapplystudentlist(data){
        return ajax.post('/getapplystudentlist',data)
    },
    applystudent(data){
        return ajax.post('/applystudent',data)
    },
    getapplyteacherlist(data){
        return ajax.post('/getapplyteacherlist',data)
    },
    applyteacher(data){
        return ajax.post('/applyteacher',data)
    },
    getmessageinfo(){
        return ajax.get('/getmessageinfo')
    },
    getmessagecount(){
        return ajax.get('/getmessagecount')
    }



}