# Server Function Available
## Basically
### Basic url
**Basic url is http://MY_ip:5000/Changeable**

### Basic function
Basic functions to visit my server is not the same cause your language is different

for example: Android (for java) should do this
```
OkHttpClient client = new OkHttpClient();
FormBody.Builder formBuilder = new FormBody.Builder();
formBuilder.add("username", userName);
formBuilder.add("password", passWord);
Request request = new Request.Builder().url(url).post(formBuilder.build()).build();
Call call = client.newCall(request);
```
username and password are strings you should give me.

so find out what kind of functions you need here!!!

## visit Changeable
**you can change 'Changeable' to visit server and ask for things you want**

### /user
#### formbuilder
you should

add ("username", username)

and ("password", password)

#### return
##### return "0"
login okay
##### return "1"
password is wrong
##### return "2"
username is wrong

### /register
#### formbuilder
you should

add ("username", username)

and ("to_addr", to_addr)


#### return
##### return "0"
this name is occupied
##### return "1"
send mail okay

### /register_with_code
#### formbuilder
you should

add ("username", username)

and ("password", password)

and ("code", code)

#### return
##### return "0"
register okay
##### return "1"
code error


### /record
#### formbuilder
you should

add ("username", username)

#### return
##### return "0"
you have had record today
##### return "1"
record saved okay 


### /get_today_record
#### formbuilder

None

#### return
##### return '1'
no today record
##### return a string
now i will explain the string

**it contents:**

[
	{
		"username":USERNAME
		"time":hour_min_second
	}
	{
		"username":littlewhiteJ
		"time":8_15_55
	}
]

### /get_user_record
#### formbuilder

add ("which_user", username)

and ("info", info)
```
switch(info)
case 0: return sum # the sum of his register days
case 1: return record_sum # the sum of his record days
case 2: return the detail of the record( explain by a dict, and the time is timestamp)
```
#### return
##### return '0'
no that user
##### return '1'
info is wrong
##### return a string
explain above

## to be continued
