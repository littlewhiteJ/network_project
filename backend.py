from flask import Flask
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
import os
from flask_sqlalchemy import SQLAlchemy
import time
import json


app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'userConfigBase.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
userdb=SQLAlchemy(app)

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
    userdb.create_all()
    haveregisted = userInfoTable.query.filter_by(username=request.form['username']).all()
    if haveregisted.__len__() is not 0: # judge if or not register
        return '0' # 'this name is occupied'
    userInfo=userInfoTable(username=request.form['username'],password=request.form['password'])
    userdb.session.add(userInfo)
    userdb.session.commit()
    return '1' # 'register is okay'

# record
@app.route('/record', methods = ['POST'])
def record():
    username = request.form['username']
    localtime = time.localtime(time.time())
    today = str(localtime.tm_year) + '_' + str(localtime.tm_mon) + '_' + str(localtime.tm_mday)
    now = str(localtime.tm_hour) + '_' + str(localtime.tm_min) + '_' + str(localtime.tm_sec)
    filename = '/data/' + today + '.json'
    if(os.path.exists(filename)):
        jsonf = open(filename, 'r+')
        todaydict = json.load(jsonf)
        namelst = todaydict['namelst']
        if username in namelst:
            jsonf.close()
            return '0' # you have had your record
        namelst.append(username)
        recordlst = todaydict['recordlst']
        userdict = {}
        userdict['username'] = username
        userdict['time'] = now
        recordlst.append(userdict)
        todaydict['recordlst'] = recordlst
    else:
        jsonf = open(filename, 'w')
        todaydict = {}
        namelst = []
        namelst.append(username)
        recordlst = []
        userdict = {}
        userdict['username'] = username
        userdict['time'] = now
        recordlst.append(userdict)
        todaydict['today'] = today
        todaydict['namelst'] = namelst
        todaydict['recordlst'] = recordlst

    json.dump(todaydict, jsonf)
    jsonf.close()
    return '1'

@app.route('/get_today_record', methods = ['POST'])
def get_today_record():
    localtime = time.localtime(time.time())
    today = str(localtime.tm_year) + '_' + str(localtime.tm_mon) + '_' + str(localtime.tm_mday)
    filename = '/data/' + today + '.json'
    if(os.path.exists(filename)):
        jsonf = open(filename, 'r+')
        todaydict = json.load(jsonf)
        recordlst = todaydict['recordlst']
        record_string = json.dumps(recordlst)
        return record_string
    else:
        return '1'
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0')

