from flask_mail import Message
from run import mail  # 已经初始化过的mail对象
import threading
from flask  import current_app
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import JSONWebSignatureSerializer as Serializer_forever
def async_send_mail(app,msg):
    '''异步发送邮件'''
    # 刚开始app还没创建，所在在使用到的时候再导入

    # 创建应用上下文（这里是最关键的）
    print('mail')
    with app.app_context():
        mail.send(message=msg)
        print('mail')


def send_mail(email=None, token=None,send_type=None):
    '''发送激活邮件
	email:收件人邮箱
	token：加密传输令牌
	'''
    app = current_app._get_current_object()
    msg = Message(subject='主题', recipients=[email])
    if send_type=='forget':
        msg.html = '''
                    <h1>欢迎修改密码</h1>
                    点击下面链接激活账号(1小时后过期)<br>
                    <a href="http://127.0.0.1:5000/forgetactivate?token='''+token+'''">立即激活</a>
                    '''         
    else:
        msg.html = '''
                    <h1>欢迎注册</h1>
                    点击下面链接激活账号(1小时后过期)<br>
                    <a href="http://127.0.0.1:5000/activate?token='''+token+'''">立即激活</a>
                    ''' 
    # 创建一个线程，并启动
    t = threading.Thread(target=async_send_mail, args=(app,msg))
    t.start()

def generate_activate_token(id, expiration=3600):
    # 这个函数需要两个参数，一个密匙，从配置文件获取，一个时间，这里1小时
    
    s = Serializer(current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
    # 为ID生成一个加密签名，然后再对数据和签名进行序列化，生成令牌版字符串（就是一长串乱七八糟的东西）,然后返回
    return s.dumps({'id': id})

# 账户激活（静态方法），所有用户共用此方法？
def generate_activate_token_forever(id):
    s = Serializer_forever(current_app.config['SECRET_KEY'])
    # 为ID生成一个加密签名，然后再对数据和签名进行序列化，生成令牌版字符串（就是一长串乱七八糟的东西）,然后返回
    return s.dumps({'id': id})  
def check_activate_token(token):
    # 传入和刚才一样的密匙，解码要用
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)   # 解码
    except:
        return False
    return data
def check_activate_token_forever(token):
    # 传入和刚才一样的密匙，解码要用
    s = Serializer_forever(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)   # 解码
    except:
        return False
    return data
def validateEmail(s):
    temp="^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
    #temp ='^(?=.*[(a-z)|(A-Z)])(?=.*\d)[^]{6,16}$'
    try:
        if re.match(temp,s)!=None:
            return True
        else :
            return False
    except:
        return False
import hashlib

def md5(str):
    hl = hashlib.md5()
    hl.update(str.encode("utf-8"))
    return hl.hexdigest()
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random
 
def validate_picture():
    total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
    width = 120
    heighth = 30
    im = Image.new('RGB',(width, heighth), 'white')
    font = ImageFont.truetype('fonts/Arial.ttf',20)
    draw = ImageDraw.Draw(im)
    str = ''
    for item in range(5):
        text = random.choice(total)
        str += text
        draw.text((5+random.randint(4,7)+20*item,2+random.randint(3,7)), text=text, fill='black',font=font )
 
    for num in range(8):
        x1 = random.randint(0, width/2)
        y1 = random.randint(0, heighth/2)
        x2 = random.randint(0, width)
        y2 = random.randint(heighth/2, heighth)
        draw.line(((x1, y1),(x2,y2)), fill='black', width=1)
 
    im = im.filter(ImageFilter.FIND_EDGES)
    return im, str
#返回验证码图片和验证码字符串
if __name__ == '__main__':
    print('pass')

