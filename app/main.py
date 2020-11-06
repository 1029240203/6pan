#! /usr/bin/env python
from flask import request, Flask, render_template,jsonify
import requests
import hashlib
import json
import os
import xmltodict
import time

basedir = os.path.abspath(os.path.dirname(__file__))
usersdir = basedir+'/users/'


app = Flask(__name__)

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'}
@app.route('/favicon.ico')
def get_fav():
    return app.send_static_file('favicon.ico')


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/6pan')
def sixpan():
    return render_template('main.html')


@app.route('/movies')
def palyer():
    return render_template('player.html')


@app.route('/getplayer',methods=['POST'])
def getplayer():
    data = request.get_json(silent=True)
    url = data['apiurl']
    pagecount = 0
    page = 1
    pagesize = 20
    recordcount = 0

    if 'videolist' in url:
        listurl = url.replace('videolist','list')
        ids=''
        try:
            rl = requests.get(listurl, verify=False, headers=headers, timeout=40)
            docl = xmltodict.parse(rl.text)
            pagecount = docl['rss']['list']['@pagecount']
            pagesize = docl['rss']['list']['@pagesize']
            page = docl['rss']['list']['@page']
            recordcount = docl['rss']['list']['@recordcount']
            idst = [x.get('id') for x in docl['rss']['list']['video']]
            ids=','.join(idst)
        except:
            return 'error'

        videolisturl = url.replace('pg=', 'k=')+'&ids='+ids
        try:
            r = requests.get(videolisturl, verify=False, headers=headers, timeout=40)
            doc = xmltodict.parse(r.text)
            doc['rss']['list']['@pagecount']=pagecount
            doc['rss']['list']['@pagesize']=pagesize
            doc['rss']['list']['@page']=page
            doc['rss']['list']['@recordcount']=recordcount
        except:
            return 'error'
        else:
            if doc is None:
                return "error"
            else:
                return json.dumps(doc)
    else:
        ids=''
        ty=[]
        print(url)
        try:
            rl = requests.get(url, verify=False, headers=headers, timeout=40)
            docl = xmltodict.parse(rl.text)
            pagecount = docl['rss']['list']['@pagecount']
            pagesize = docl['rss']['list']['@pagesize']
            page = docl['rss']['list']['@page']
            recordcount = docl['rss']['list']['@recordcount']
            idst = [x.get('id') for x in docl['rss']['list']['video']]
            ty = docl['rss']['class']
            ids=','.join(idst)
        except:
            return 'error'

        videolisturl = url.replace('pg=', 'k=')+'&ac=videolist&ids='+ids
        try:
            r = requests.get(videolisturl, verify=False, headers=headers, timeout=40)
            doc = xmltodict.parse(r.text)
            doc['rss']['list']['@pagesize']=pagesize
            doc['rss']['list']['@pagecount']=pagecount
            doc['rss']['list']['@page']=page
            doc['rss']['list']['@recordcount']=recordcount
            doc['rss']['class'] = ty
            print(json.dumps(doc))
        except:
            return 'error'
        else:
            if doc is None:
                return "error"
            else:
                return json.dumps(doc)



   

    
    



@app.route('/login',methods=['POST'])
def login():
    # postdata = request.form['id']
    # file = request.files['file']
    # recognize_info = {'id': postdata, 'info': '收到' + file.filename}
    # return jsonify(recognize_info), 201
    data = request.get_json(silent=True)
    s = requests.session()
    #url = "https://account.6pan.cn/v3/oauth/login"
    url = "https://account.2dland.cn/v3/oauth/login"
    username = data['username']
    password = data['password']
    pwd=hashlib.md5(password.encode("utf-8")).hexdigest()

    d = {'user': username, 'password': pwd, 'countryCode': ''}
    r = s.post(url, verify=False, data=d)
    result = json.loads(r.text)
    if result['success'] == False:
        return 'error'
    else:
        headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        headers["accept-encoding"] = "br, gzip, deflate"
        #checkcookieurl = "https://account.6pan.cn/v3/oauth/checkCookie?appid=3a5654a9ccc9&destination=https:%2F%2Fv3-beta.6pan.cn%2Ffiles&lang=zh-CN&scope=&state=7fjdgjeff&response=redirect"
        checkcookieurl = "https://account.2dland.cn/v3/oauth/checkCookie?appid=3a5654a9ccc9&destination=https:%2F%2F2dland.cn%2Ffiles%2Fall%2F&lang=zh-CN&scope=&state=7hk2fic6c&response=redirect"
        rc = s.get(checkcookieurl, verify=False, headers=headers, timeout=40)
        user = {}
        user['username']=username
        user['password'] = pwd
        user['qingzhen-token'] = s.cookies.get_dict()
        userstring =  json.dumps(user)
        # 打开文件
        fo = open(usersdir+username+".txt", "w")
        fo.write(userstring)
        fo.close()
        return userstring
    return 'error'

@app.route('/relogin',methods=['POST'])
def relogin():
    # postdata = request.form['id']
    # file = request.files['file']
    # recognize_info = {'id': postdata, 'info': '收到' + file.filename}
    # return jsonify(recognize_info), 201
    data = request.get_json(silent=True)
    s = requests.session()
    #url = "https://account.6pan.cn/v3/oauth/login"
    url = "https://account.2dland.cn/v3/oauth/login"
    username = data['username']

    with open(usersdir + username+".txt") as f:
        content = f.read()
        user = json.loads(content)

    password = user['password']
    #pwd=hashlib.md5(password.encode("utf-8")).hexdigest()

    d = {'user': username, 'password': password, 'countryCode': ''}
    r = s.post(url, verify=False, data=d, timeout=40)
    result = json.loads(r.text)
    if result['success'] == False:
        return 'error'
    else:
        headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        headers["accept-encoding"] = "br, gzip, deflate"
        checkcookieurl = "https://account.2dland.cn/v3/oauth/checkCookie?appid=3a5654a9ccc9&destination=https:%2F%2F2dland.cn%2Ffiles%2Fall%2F&lang=zh-CN&scope=&state=7hk2fic6c&response=redirect"
        rc = s.get(checkcookieurl, verify=False, headers=headers, timeout=40)
        user = {}
        user['username']=username
        user['password'] = password
        user['qingzhen-token'] = s.cookies.get_dict()
        userstring =  json.dumps(user)
        # 打开文件
        fo = open(usersdir+username+".txt", "w")
        fo.write(userstring)
        fo.close()
        return userstring
    return 'error'


@app.route('/getUsers')
def getUsers():
    files = os.listdir(usersdir)
    users = []
    for file in files:
        with open(usersdir+file) as f:
            content = f.read()
            user = json.loads(content)
            user.pop('password', None)
            users.append(user)
    info = {}
    info['users'] = users
    return json.dumps(users)

@app.route('/delUser',methods=['POST'])
def delUser():
    # postdata = request.form['id']
    # file = request.files['file']
    # recognize_info = {'id': postdata, 'info': '收到' + file.filename}
    # return jsonify(recognize_info), 201
    data = request.get_json(silent=True)
    userfile = usersdir+data['username']+'.txt'
    if os.path.exists(userfile):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(userfile)
        return 'ok'
    else:
        return 'error'

    return 'error'

@app.route('/getFiles',methods=['POST'])
def getFiles():
    data = request.get_json(silent=True)
    if 'qingzhen-token' not in data.keys():
        return 'error'
    ucookies = data['qingzhen-token']
    url = 'https://api.2dland.cn/v3/files/list'
    start = (int(data['pageno']) - 1) * 20
    rdata = {'parentPath': data['path'], 'name': '', 'limit': 20, 'start': start, "orderby": [["ctime", "DESC"]]}

    headers['referer'] = "https://2dland.cn/files/all/"

    try:
        r = requests.post(url, verify=False, json=rdata, headers=headers, cookies=ucookies, timeout=40)
    except:
        return 'error'
    else:
        result = json.loads(r.text)
        if r.status_code != 200:
            return 'error'
        return json.dumps(result)



@app.route('/getVideos',methods=['POST'])
def getVideos():
    data = request.get_json(silent=True)
    if 'qingzhen-token' not in data.keys():
        return 'error'
    ucookies = data['qingzhen-token']
    url = 'https://api.2dland.cn/v3/files/list'
    start = (int(data['pageno']) - 1) * 20
    rdata = {'parentIdentity': '::all', 'name': '', 'limit': 20, 'start': start, 'orderby': '','type': 30}

    headers['referer'] = "https://2dland.cn/files/all/"
    r = requests.post(url, verify=False, data=rdata, headers=headers, cookies=ucookies, timeout=40)
    result = json.loads(r.text)
    if r.status_code != 200:
        return 'error'
    return json.dumps(result)

@app.route('/getDownload',methods=['POST'])
def getDownload():
    data = request.get_json(silent=True)
    if 'qingzhen-token' not in data.keys():
        return 'error'
    ucookies = data['qingzhen-token']
    url = 'https://api.2dland.cn/v3/newfile/download'
    rdata = {'identity': data['identity']}
    headers['referer'] = "https://2dland.cn/files/all/"
    r = requests.post(url, verify=False, data=rdata, headers=headers, cookies=ucookies, timeout=40)
    result = json.loads(r.text)
    if r.status_code != 200:
        return 'error'
    return json.dumps(result)


@app.route('/searchFiles',methods=['POST'])
def searchFiles():
    data = request.get_json(silent=True)
    if 'qingzhen-token' not in data.keys():
        return 'error'
    ucookies = data['qingzhen-token']
    url = 'https://api.2dland.cn/v3/newfile/list'
    start = (int(data['pageno']) - 1) * 20
    keyword = data['keyword']
    rdata = {'limit': 20, 'parentIdentity': "", 'name': keyword,'start': start, 'search': True,}
    headers['referer'] = "https://2dland.cn/files/all/"
    r = requests.post(url, verify=False, data=rdata, headers=headers, cookies=ucookies, timeout=40)
    result = json.loads(r.text)
    if r.status_code != 200:
        return 'error'
    return json.dumps(result)


@app.route('/checkOffline',methods=['POST'])
def checkOffline():
    data = request.get_json(silent=True)
    if 'qingzhen-token' not in data.keys():
        return 'error'
    ucookies = data['qingzhen-token']
    url = 'https://api.2dland.cn/v3/offline/quota'
    t = time.time()
    rdata = {'time': int(round(t * 1000))}
    headers['referer'] = "https://2dland.cn/files/all/"
    r = requests.post(url, verify=False, data=rdata, headers=headers, cookies=ucookies, timeout=40)
    result = json.loads(r.text)
    if r.status_code != 200:
        return 'error'
    return json.dumps(result)  


@app.route('/offline',methods=['POST'])
def offline():
    data = request.get_json(silent=True)
    if 'qingzhen-token' not in data.keys():
        return 'error'
    ucookies = data['qingzhen-token']
    url = 'https://api.2dland.cn/v3/offline/parse'
    keyword = data['textLink']
    rdata = {'textLink': keyword}
    headers['referer'] = "https://2dland.cn/files/all/"
    r = requests.post(url, verify=False, data=rdata, headers=headers, cookies=ucookies, timeout=40)
    result = json.loads(r.text)
    if r.status_code != 200 or result['hash'] is None:
        return 'error'

    ourl = 'https://api.2dland.cn/v3/offline/add'
    odata = {"savePath": "/","task": [{"ignore": [None],"hash": result['hash']}]}
    ore = requests.post(ourl, verify=False, json =odata, headers=headers, cookies=ucookies, timeout=40)
    oresult = json.loads(ore.text)

    if ore.status_code != 200 or oresult['successCount'] is None:
        return 'error'

    return json.dumps(oresult)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10003, debug = True)
