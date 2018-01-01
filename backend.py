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

class User(userdb.Model):
    __tablename__='userInfo'
    id=userdb.Column(userdb.Integer,primary_key=True)
    username=userdb.Column(userdb.String,unique=True)
    password=userdb.Column(userdb.String)
    email=userdb.Column(userdb.String)
    register_sum=userdb.Column(userdb.Integer)
    record_sum=userdb.Column(userdb.Integer)
    continue_record_sum=userdb.Column(userdb.Integer)
    record_detail=userdb.Column(userdb.String)
    def __repr__(self):
        return 'table name is '+self.username

class Date(userdb.Model):
    __tablename__='Date'
    id=userdb.Column(userdb.Integer,primary_key=True)
    today=userdb.Column(userdb.String,unique=True)
    recordToday=userdb.Column(userdb.String)
    def __repr__(self):
        return 'table name is '+self.username

class con_record(userdb.Model):
    __tablename__='con_record'
    id=userdb.Column(userdb.Integer,primary_key=True)
    username=userdb.Column(userdb.String,unique=True)
    con_sum=userdb.Column(userdb.Integer)
    def __repr__(self):
        return 'table name is '+self.username

class all_record(userdb.Model):
    __tablename__='all_record'
    id=userdb.Column(userdb.Integer,primary_key=True)
    username=userdb.Column(userdb.String,unique=True)
    all_sum=userdb.Column(userdb.Integer)
    def __repr__(self):
        return 'table name is '+self.username

@app.route('/user',methods=['POST'])
def check_user():
    user = User.query.filter_by(username=request.form['username']).first()
    if user is not None:
        if user.password == request.form['password']:
            return '0' # 'login okay'
        else:
            return '1' # 'password is wrong'
    else:
        return '2' # 'username is wrong'


#register
@app.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user is not None: # judge if or not register
        return '1' # 'this name is occupied'
    to_addr = request.form['to_addr']
    code = code_generator()
    codedict[username] = code
    maildict[username] = to_addr
    email_(code, to_addr, mail_password)
    return '0' # 'send mail okay'

#register with code
@app.route('/register_with_code',methods = ['POST'])
def register_():
    code = request.form['code']
    username = request.form['username']
    password = request.form['password']
    if code == codedict[username]:
        codedict.pop(username)
        userInfo=User(username=username,password=password,
                      email=maildict[username],register_sum=0,
                      record_sum=0,continue_record_sum=0,
                      record_detail='{}')
        userdb.session.add(userInfo)

        c_record=con_record(username=username,con_sum=0)
        userdb.session.add(c_record)

        a_record=all_record(username=username,all_sum=0)
        userdb.session.add(a_record)

        userdb.session.commit()

        return '0' # register okay
    return '1' # code error


# record
@app.route('/record', methods = ['POST'])
def record():
    username = request.form['username']
    now = time.time()
    localtime = time.localtime(now)
    today = str(localtime.tm_year) + '_' + str(localtime.tm_mon) + '_' + str(localtime.tm_mday)

    # add or append today's data
    todayData = Date.query.filter_by(today=today).first()
    if todayData is not None: # if someone have had record today
        user = User.query.filter_by(username=username).first()
        record_dict = json.loads(user.record_detail)
        if today in record_dict:
            return '1' # you have had your record today
        today_dict = json.loads(todayData.recordToday)
        today_dict[username] = now
        todayData.recordToday = json.dumps(today_dict)
    else: # if nobody records today
        all_user = User.query.all()
        for user in all_user:
            user.register_sum += 1

            todaytime = now
            yesttime = todaytime - 86400
            ylocaltime = time.localtime(yesttime)
            yesterday = str(ylocaltime.tm_year) + '_' + str(ylocaltime.tm_mon) + '_' + str(ylocaltime.tm_mday)
            record_dict = json.loads(user.record_detail)
            if yesterday not in record_dict:
                user.continue_record_sum = 0
        today_dict = {}
        today_dict[username] = now
        todayData = Date(today=today, recordToday = json.dumps(today_dict))
        userdb.session.add(todayData)

 


    # modify user's data
    user = User.query.filter_by(username=username).first()
    user.record_sum += 1
    user.continue_record_sum += 1
    record_dict = json.loads(user.record_detail)
    record_dict[today] = now
    user.record_detail = json.dumps(record_dict)
    
    # modify all_ranking data
    all_r = all_record.query.filter_by(username=username).first()
    all_r.all_sum += 1

    # modify con_ranking data
    con_r = con_record.query.filter_by(username=username).first()
    con_r.con_sum += 1

    userdb.session.commit()
    return '0' # record successfully

@app.route('/get_today_record', methods = ['POST'])
def get_today_record():
    localtime = time.localtime(time.time())
    today = str(localtime.tm_year) + '_' + str(localtime.tm_mon) + '_' + str(localtime.tm_mday)
    todayData = Date.query.filter_by(today=today).first()
    if(todayData is not None):
        return json.dumps(todayData.recordToday)
    else:
        return '1' # no today record
   
@app.route('/get_register_sum', methods = ['POST'])
def get_register_sum():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    return user.register_sum

@app.route('/get_record_sum', methods = ['POST'])
def get_record_sum():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    return user.record_sum

@app.route('/get_continue_record_sum', methods = ['POST'])
def get_continue_record_sum():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    return user.continue_record_sum

@app.route('/get_record_detail', methods = ['POST'])
def get_record_detail():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    return json.dumps(user.record_detail)

@app.route('/if_today_record', methods = ['POST'])
def if_today_record():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    detail_dict = user.record_detail
    localtime = time.localtime(time.time())
    today = str(localtime.tm_year) + '_' + str(localtime.tm_mon) + '_' + str(localtime.tm_mday)
    if today in detail_dict:
        return 1
    else:
        return 0

    return user.continue_record_sum

@app.route('/all_ranking', methods = ['POST'])
def all_ranking():
    username = request.form['username']
    output = all_record.query.order_by(userdb.desc(all_record.all_sum)).limit(6)
    user = all_record.query.filter_by(username=username).first()
    num = user.id
    outdict = {}
    for out in output:
        outdict[out.username] = out.all_sum
    dict = {}
    dict['rank'] = num
    dict['1to6'] = json.dumps(outdict)
    return json.dumps(dict)

@app.route('/con_ranking', methods = ['POST'])
def con_ranking():
    username = request.form['username']
    output = con_record.query.order_by(userdb.desc(con_record.con_sum)).limit(6)
    user = con_record.query.filter_by(username=username).first()
    num = user.id
    outdict = {}
    for out in output:
        outdict[out.username] = out.con_sum
    dict = {}
    dict['rank'] = num
    dict['1to6'] = json.dumps(outdict)
    return json.dumps(dict)

if __name__ == '__main__':
    userdb.create_all()
    app.run(host = '0.0.0.0')
    
