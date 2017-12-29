from flask import Flask
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
import os
from flask_sqlalchemy import SQLAlchemy
import time
import json
from mail import email_ 
from random_str import code_generator


app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'userConfigBase.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
userdb=SQLAlchemy(app)

mail_password = raw_input('mail password: ')
codedict = {}
maildict = {}


@app.route('/')
def test():
    return 'server is okay'

class userInfoTable(userdb.Model):
    __tablename__='userInfo'
    id=userdb.Column(userdb.Integer,primary_key=True)
    username=userdb.Column(userdb.String,unique=True)
    password=userdb.Column(userdb.String)

    def __repr__(self):
        return 'table name is '+self.username

@app.route('/user',methods=['POST'])
def check_user():
    userdb.create_all()
    haveregisted = userInfoTable.query.filter_by(username=request.form['username']).all()
    if haveregisted.__len__() is not 0: 
        passwordRight = userInfoTable.query.filter_by(username=request.form['username'],password=request.form['password']).all()
        if passwordRight.__len__() is not 0:
            return '0' # 'login okay'
        else:
            return '1' # 'password is wrong'
    else:
        return '2' # 'username is wrong'


#register
@app.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    haveregisted = userInfoTable.query.filter_by(username=username).all()
    if haveregisted.__len__() is not 0: # judge if or not register
        return '0' # 'this name is occupied'
    to_addr = request.form['to_addr']
    code = code_generator()
    codedict[username] = code
    maildict[username] = to_addr
    email_(code, to_addr, mail_password)
    return '1' # 'send mail okay'

#register with code
@app.route('/register_with_code',methods = ['POST'])
def register_():
    code = request.form['code']
    username = request.form['username']
    password = request.form['password']
    if code == codedict[username]:
        codedict.pop(username)
        userInfo=userInfoTable(username=username,password=password)
        userdb.session.add(userInfo)
        userdb.session.commit()
        with open('data/' + username + '.json', 'w') as userf:
	        userdict = {}
	        userdict['username'] = username
	        userdict['email'] = maildict[username]
	        userdict['sum'] = 0
	        userdict['record_sum'] = 0
            userdict['con_record'] = 0
	        userdict['record'] = []
	        json.dump(userdict, userf)
        with open('data/all_ranking.json', 'r+') as arf:
            ardict = json.load(arf)
            ardict[username] = 0
            json.dump(ardict, arf)
        with open('data/con_ranking.json', 'r+') as crf:
            crdict = json.load(crf)
            crdict[username] = 0
            json.dump(crdict, crf)
        return '0' # register okay
    return '1' # code error


# record
@app.route('/record', methods = ['POST'])
def record():
    username = request.form['username']
    localtime = time.localtime(time.time())
    today = str(localtime.tm_year) + '_' + str(localtime.tm_mon) + '_' + str(localtime.tm_mday)
    filename = '/data/' + today + '.json'
    # add or append today's data
    if(os.path.exists(filename)): # if someone have had record today
        jsonf = open(filename, 'r+')
        todaydict = json.load(jsonf)
        namelst = todaydict['namelst']
        if username in namelst:
            jsonf.close()
            return '0' # you have had your record today
        namelst.append(username)
        recordlst = todaydict['recordlst']
        userdict = {}
        userdict['username'] = username
        userdict['time'] = str(time.time())
        recordlst.append(userdict)
        todaydict['recordlst'] = recordlst
    else: # if nobody records today
        haveregisted = userInfoTable.query.filter_by(username=username).all()
        for name in haveregisted:
            with open('data/' + name + '.json') as f:
                udict = json.load(f)
                udict['sum'] += 1

                todaytime = time.time()
                yesttime = todaytime - 86400
                ylocaltime = time.localtime(yesttime)
                yesterday = str(ylocaltime.tm_year) + '_' + str(ylocaltime.tm_mon) + '_' + str(ylocaltime.tm_mday)
                yfile = 'data/' + yesterday + '.json'
                if os.path.isfile(yfile):
                    with open(yfile) as yf:
                        ydict = json.load(yf)
                        ynamelst = ydict['namelst']
                        if name not in ynamelst:
                            udict['con_record'] = 0

        jsonf = open(filename, 'w')
        todaydict = {}
        namelst = []
        namelst.append(username)
        recordlst = []
        userdict = {}
        userdict['username'] = username
        userdict['time'] = str(time.time())
        recordlst.append(userdict)
        todaydict['today'] = today
        todaydict['namelst'] = namelst
        todaydict['recordlst'] = recordlst
 

    json.dump(todaydict, jsonf)
    jsonf.close()

    # modify user's data
    userf = open('data/' + username + '.json', 'r+')
    udict = json.load(userf)
    udict['record_sum'] += 1
    udict['con_record'] += 1
    con_record = udict['con_record']
    ulst = udict['record']
    ulst.append(str(time.time()))
    udict['record'] = ulst
    json.dump(udict, userf)
    userf.close()
    
    # modify all_ranking data
    with open('data/all_ranking.json', 'r+') as arf:
        ardict = json.load(arf)
        ardict[username] += 1
        json.dump(ardict, arf)

    # modify con_ranking data
    with open('data/con_ranking.json', 'r+') as crf:
        crdict = json.load(crf)
        crdict[username] = con_record
        json.dump(crdict, crf)

    return '1' # record successfully

@app.route('/get_today_record', methods = ['POST'])
def get_today_record():
    localtime = time.localtime(time.time())
    today = str(localtime.tm_year) + '_' + str(localtime.tm_mon) + '_' + str(localtime.tm_mday)
    filename = 'data/' + today + '.json'
    if(os.path.exists(filename)):
        jsonf = open(filename, 'r+')
        todaydict = json.load(jsonf)
        recordlst = todaydict['recordlst']
        record_string = json.dumps(recordlst)
        return record_string
    else:
        return '0' # no today record
   
@app.route('/get_user_record', methods = ['POST'])
def get_user_record():
    user = request.form['which_user']
    info = request.form['info']
    filename = 'data/' + user + '.json'
    if (os.path.exists(filename)):
        userf = open(filename, 'r')
        userdict = json.load(userf)
        if info == 0:
            return userdict['sum']
        if info == 1:
            return userdict['record_sum']
        if info == 2:
            return json.dumps(userdict['record'])
        if info == 3:
            return userdict['con_record']
        return '1' # info num is wrong
    else:
        return '0' # no that user

@app.route('/all_ranking', methods = ['POST'])
def all_ranking():
    username = request.form['username']
    with open('data/all_ranking.json', 'r') as arf:
        ardict = json.load(arf)
        lst = sorted(ardict.iteritems(), key = lambda d:d[1], reverse = True)
        lstl = len(lst)
        rank = 0
        for i in range(lstl):
            if lst[i][0] == username:
                rank = i + 1
        rankdict = {}
        rankdict['rank'] = rank
        rankdict['first2sixth'] = lst[:6]
        return json.dumps(rankdict)

@app.route('/con_ranking', methods = ['POST'])
def con_ranking():
    username = request.form['username']
    with open('data/con_ranking.json', 'r') as crf:
        crdict = json.load(crf)
        lst = sorted(crdict.iteritems(), key = lambda d:d[1], reverse = True)
        lstl = len(lst)
        rank = 0
        for i in range(lstl):
            if lst[i][0] == username:
                rank = i + 1
        rankdict = {}
        rankdict['rank'] = rank
        rankdict['first2sixth'] = lst[:6]
        return json.dumps(rankdict)

if __name__ == '__main__':
    if !os.path.isfile('data/all_ranking.json'):
        with open('data/all_ranking.json', 'w') as arf:
            ardict = {}
            json.dump(ardict, arf)

    if !os.path.isfile('data/con_ranking'):
        with open('data/con_ranking.json', 'w') as crf:
            crdict = {}
            json.dump(crdict, crf)

    app.run(host = '0.0.0.0')
    
