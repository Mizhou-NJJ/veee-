import requests
import json
from bs4 import BeautifulSoup
import hashlib
import random
import time

class VeeePackage:
    ea = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']

    def __init__(self,user_id='user_id',pwd='pwd'):
        self.user_id=user_id
        hl = hashlib.md5()
        hl.update(pwd.encode('utf-8'))
        self.pwd= str(hl.hexdigest())
        self.device_id= self.randstr_by_len(10)
        self.device_name='Iphone X'
        self.extend_source='34'
        self.exchange_code=''
        self.platform='1'
        self.app_name='bluerabbit'
        self.app_version='030500'
        self.lang='zh-hk'
        self.code_serialno='null'
        self.source='1'
        self.verify_code='null'
    def randstr_by_len(self,lenstr):
        string =''
        for i in range(0,lenstr):
            string += self.ea[random.randint(0,len(self.ea)-1)]
        return string
    def compare(self):
        pass
    # def package_login(self):
    #     pack = {
    #         'user_id': self.user_id,
    #         'password':self.pwd,
    #         'device_id':self.device_id,
    #         'device_name':self.device_name,
    #         'extend_source':self.extend_source,
    #         'exchange_code':self.exchange_code,
    #         'platform':self.platform,
    #         'app_name':self.app_name,
    #         'app_version':self.app_version,
    #         'lang':self.lang
    #     }
    #     return pack
    def package(self):
        pack = {
            'user_id': self.user_id,
            'password': self.pwd,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'extend_source': self.extend_source,
            'exchange_code': self.exchange_code,
            'platform': self.platform,
            'app_name': self.app_name,
            'app_version': self.app_version,
            'lang': self.lang,
            # end  login pack
            'scene':'1',
            #
            'level':'1',
            'sign':self.randstr_by_len(32),
            'time_stamp':int(time.time())
        }
        return pack
    def package_regist(self,mail,pwd,invate=''):
        hl = hashlib.md5()
        hl.update(pwd.encode('utf-8'))
        pack = {
            'password': str(hl.hexdigest()),
            'user_id': mail,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'extend_source': self.extend_source,
            'platform': self.platform,
            'app_name': self.app_name,
            'app_version': self.app_version,
            'code_serialno':self.code_serialno,
            'inviter':invate,
            'lang': self.lang,
            'verify_code':self.verify_code,
            'source':self.source
        }
        return pack
class Veee:
    ips = []
    gproxies = {}
    error_ag_count = 0
    error_ag_max_count=3
    ar =  ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    status_code_noinv = 200002  # 邀请人不存在
    status_code_exist = 200036  # 账号已存在
    status_code_lim=200001

    authorization = None
    register_url = 'https://ltzproxy.zhxcshop.com/api/v2/register'
    login_url = 'https://ltzproxy.zhxcshop.com/api/v2/login'
    url_getuinfo='https://ltzproxy.zhxcshop.com/api/v2/get_user_info'
    url_sf_user = 'https://ltzproxy.zhxcshop.com/api/v2/get_sf_user_info'
    headers = {
        'Authorization':'',
        "Connection": "keep-alive",
        "Host": "ltzproxy.zhxcshop.com",
        "User-Agent": "okhttp/3.13.1",
    }
    def __init__(self,user_id,pwd):
        self.session = requests.session()
        self.vp = VeeePackage(user_id=user_id, pwd=pwd)
    def lunch_app(self):
        pass
    def login(self):
        pack = self.vp.package()
        resp = None
        resp = self.session.post(self.login_url,headers = self.headers,data=pack)
        jsr = resp.json()
        # print(jsr)
        newheader = {}
        print(jsr['message'])
        if jsr['status_code'] == 200:
            head = resp.headers
            newheader = {
                "Connection": "keep-alive",
                "Host": "ltzproxy.zhxcshop.com",
                "User-Agent": "okhttp/3.13.1",
                'Authorization': head.get('Authorization'),
                'Access-Control-Allow-Headers':head.get('Access-Control-Allow-Headers'),
                'Access-Control-Expose-Headers':head.get('Access-Control-Expose-Headers'),
                'Access-Control-Allow-Credentials':head.get('Access-Control-Allow-Credentials')
            }
            self.authorization = head.get('Authorization')
            self.headers['Authorization'] = head.get('Authorization')
            return  newheader
        return None

    def get_user_info(self,newheader):  # after login
        pack = self.vp.package()
        resp = self.session.post(self.url_getuinfo,headers=newheader,data=pack)
        return  resp.json()



    def registerByme(self,mail,pwd,proxies=None):
        pack = self.vp.package_regist(mail=mail, pwd=pwd,)
        resp = self.session.post(self.register_url, headers=self.headers, data=pack,proxies=proxies)
        jsonr = resp.json()
        if jsonr['status_code'] == 200:
            return True
        else:
            print(jsonr['message'])
        return  False



    def register(self,proxies=None,invite_code='rVbsIzwJ'):
        mail = self.random_mail()
        pwd ='123456'
        pack = self.vp.package_regist(mail=mail,pwd=pwd,invate=invite_code)
        resp = None
        try:
            resp = self.session.post(self.register_url, headers=self.headers, data=pack, proxies=proxies)
        except:
            print('invalid ip :'+proxies['https'])
            return False
        jsr = resp.json()
        if jsr['status_code'] == 200:
            print('+1小时')
            return True
        else:
            if jsr['status_code'] == self.status_code_lim:
                print('message:'+jsr['message'])
                if proxies!=None:
                    print('IP(+' + proxies['https'] + '+无效或已达上限,正在设置代理...')
                else:
                    print('本机IP已达上限...正在设置代理')
                return False


    def random_mail(self):
        mail = '2020'
        for _ in range(4):
            mail+=self.ar[random.randint(0,len(self.ar)-1)]
        mail+='@gmail.com'
        return mail

    def get_xila_ips(self):

        '''
         从西拉免费代理ip获取
         同上
        :param save: 是否保存至本地
        :return: ip列表
        '''
        ips = []
        api = 'http://www.xiladaili.com/https/'
        rep = requests.get(api)
        if rep.status_code == 200:
            bs4 = BeautifulSoup(rep.content, 'lxml')
            tbody = bs4.find_all(name='tbody')[0]
            trs = tbody.contents
            for t in trs:
                if t.name == 'tr':
                    tds = t.contents
                    ip = tds[1].string
                    ip = ip.replace(' ', '')
                    ip = ip.replace('\r\n', '')
                    ips.append(ip)
            # write
        else:
            print('代理获取失败' + str(rep.status_code),end='')
            if self.error_ag_count < self.error_ag_max_count:
                print('即将重新获取...')
            else:
                print('请尝试手动更改代理')
            self.error_ag_count += 1
        return ips


def invitefor(mail,pwd,count):
    '''
    :param mail: 你的已注册账号
    :param pwd: 你的密码
    :param count:  需要的小时数
    :return:
    '''
    vee = Veee(mail, pwd)
    rjson= vee.get_user_info(vee.login())
    invite_code =''
    if rjson['status_code'] == 200:
        invite_code = rjson['invite_code']
    else:
        print('209:'+rjson['message'])
    alcount = 0
    is_localip=True
    ip_index = 0
    # vee.get_user_info(nheader)
    while alcount<count:
        ip_index = 0
        if vee.error_ag_count > vee.error_ag_max_count:
            print('多次失败')
            return
        if is_localip:
            result = vee.register(invite_code=invite_code)
            if result:
                alcount += 1
            else:
                is_localip=False
        else:
            ip = vee.get_xila_ips()
            if len(ip) > 0:
               print('代理获取成功...')
               while alcount<count:
                   vee.ips = ip
                   if ip_index < len(vee.ips):
                       proxies = {'https': vee.ips[ip_index]}
                       result = vee.register(proxies, invite_code=invite_code)
                       if result:
                           alcount += 1
                       else:
                           ip_index += 1
                   else:
                       break


def login(mail,pwd):
    vee = Veee(mail, pwd)
    vee.login()
    # rjson = vee.get_user_info(vee.login())

def regist(mail,pwd,proxies):
    '''
    注册一个新账号
    :param mail:
    :param pwd:
    :return:
    '''
    vee = Veee('null','null')
    if vee.registerByme(mail,pwd,proxies):
        print('注册成功')
    else:
        print('注册失败')

if __name__ == '__main__':
    # vee = Veee('null','null')
    # vee.register(proxies={'https':'150.138.253.71:808'})
    '''
    ############################
    一般情况下，如果已有账号，调用 { @method invitefor(mail,pwd,count) 方法即可
    如果没有帐号,可调用{@method regist(mail,pwd)} l来注册一个帐号,后再调用{@method invitefor(mail.pwd,count)}
     :param mail: 你的已注册账号
    :param pwd: 你的密码
    ：param count: 要白嫖的小时数
    ############################
    如执行以下方法后，再不出问题的情况下，会为 hig@gmail.com 续费2小时的时间
  '''
    # regist('hib@gmail.com','123456',proxies={'https':'171.96.231.3:8080'})
    # login()
    invitefor('hib@gmail.com','123456',10)