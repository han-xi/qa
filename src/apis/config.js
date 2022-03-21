import axios from "axios";
import router from "../router";
// axios.defaults.baseURL = ''  //正式
axios.defaults.withCredentials = true; 
const ajax = axios.create({
    baseURL : 'http://localhost:5000' ,
    withCredentials : true,
    timeout : 15000,
})


ajax.interceptors.request.use(
    config => {
        config.data = JSON.stringify(config.data)
        const token = localStorage.getItem("access_token")
        config.headers = { 'Content-Type':"application/json"};

        if(token){
            config.headers.Authorization = `Bearer ${token}`
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

ajax.interceptors.response.use(
    response => {
        if (response.status == 200) {
            return Promise.resolve(response);
        } else {
           
            return Promise.reject(response);
        }
    },
    async error => {
   
        
        if(error.response.status == 401){
            const refreshToken = localStorage.getItem("refresh_token")
            if(refreshToken){
                try {
                    const res = await axios({
                      url: 'http://localhost:5000/token/refresh',
                      method: 'PUT',
                      headers: { // headers 不能按接口文档抄 H不能大写！！！！
                        Authorization: `Bearer ${refreshToken}`,
                        // Access-Control-Allow-Credentials:true
                      }
                    })
                    const newToken = res.data['access_token']
                    localStorage.setItem("access_token",newToken)
                    return ajax(error.config)
                } catch (error) {
                    localStorage.setItem("access_token",'')
                    localStorage.setItem("refresh_token",'')
                    router.push('/?returnUrl=' + encodeURIComponent(router.currentRoute.fullPath))
                    return Promise.reject(new Error('refresh_token清空'))
                }
            }else{
                localStorage.setItem("access_token",'')
                localStorage.setItem("refresh_token",'')
                router.push('/?returnUrl=' + encodeURIComponent(router.currentRoute.fullPath))
                return Promise.reject(new Error('refresh_token清空'))                              
            }
        }
     
        return Promise.reject(error.response);
        // alert(JSON.stringify(error), '请求异常', {
        //     confirmButtonText: '确定',
        //     callback: (action) => {
        //         console.log(action)
        //     }
        // });
    }
);
export default ajax;

