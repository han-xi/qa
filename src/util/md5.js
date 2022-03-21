import md5 from 'js-md5';
export default{
    encode(data){
        return md5.base64(data)
    },
    decode(data){
        let A = md5.base64('A')
        let B = md5.base64('B')
        let C = md5.base64('C')
        let D = md5.base64('D')
        let E = md5.base64('E')
        let check =new Array();
        check[A] ='A';
        check[B] ='B';
        check[C] ='C';
        check[D] ='D';
        check[E] ='E';
        if (data in check){
            return check[data]
        }else{
            return ''
        }
    }
}