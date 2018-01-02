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
send mail okay
##### return "1"
this name is occupied

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
##### return "1"
you have had record today
##### return "0"
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



{

	"username":str(time)

	"tianguiyu":"12345567" # time.time()

}


### /get_register_sum
#### formbuilder

add ("username", username)

#### return
register num # how many days past from the day you register

### /get_record_sum
#### formbuilder

add ("username", username)

#### return
record num # how many days you record

### /if_today_record
#### formbuilder

add ("username", username)

#### return
"1" # record today
"0" # no record today

### /get_continue_record_sum
#### formbuilder

add ("username", username)

#### return
continue record num # how many days you continue recording

### /get_record_detail
#### formbuilder

add ("username", username)

#### return
a string and its structure is as follows
#### record_detail
{
	today:time
	2018.01.01: "13:55"
}

### /all_ranking
#### formbuilder

add ("username", username)

##### return a string
now i will explain the string

**it contents:**

{

	"rank":ranknum
	
	"1to6":
	
		[
		
			("name", "sum of record")
			
			...
			
		]
		
}

### /con_ranking
#### formbuilder

add ("username", username)

##### return a string
now i will explain the string

**it contents:**

{

	"rank":ranknum
	
	"1to6":
	
		[
		
			("name", "sum of record")
			
			...
			
		]
		
}


## these are the backend data structures, omit it if you do not care about it

**manage by sqlalchemy**
we have several tables to store the data
### User
username
password
email
register_sum
record_sum
continue_record_sum
record_detail

#### record_detail
{
	today:time
	"2018.01.01": "13:55"
}

### Date
today
recordToday

#### recordToday
{
	username:time
	tianguiyu: "13:55"
}

### All_ranking
username
all_sum

### Continue_ranking 
username
con_sum


## to be continued
