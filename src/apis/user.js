import ajax from './config'
export default{
    login(data){
        return ajax.post('/login',data)
    },
    getcode(){
        return ajax.get('/getcode')
    },
    signup(data){
        return ajax.post('/signup',data)
    },
    register(data){
        return ajax.post('/register',data)
    },
    forgetpassword(data){
        return ajax.post('/forgetpassword',data)
    },
    
    home(){
        return ajax.get('/home')
    },
    upgradepermission(){
        return ajax.post('/upgradepermission')
    },
    getupgradepermissionlist(data){
        return ajax.post('/getupgradepermissionlist',data)
    },
    addupgradepermission(data){
        return ajax.post('/addupgradepermission',data)
    },
    deleteupgradepermission(data){
        return ajax.post('/deleteupgradepermission',data)
    }
}