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

and ("password", password)

#### return
##### return "0"
this name is occupied
##### return "1"
register is okay

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

## to be continued
