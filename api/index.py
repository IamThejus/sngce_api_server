from flask import Flask,jsonify,request
import os
import requests
import redis
from bs4 import BeautifulSoup
import json


# Get Redis URL from environment variable
REDIS_URL = os.environ.get("REDIS_URL")
r = redis.Redis.from_url(REDIS_URL)

message="This is an API Server.\nInorder to acess you can use get_attendance,get_timetable,get_materials\nUse Username and Password as payload"

url="https://sngce.etlab.in/user/login"



            
def get_loggedin(usrid,passwd):
    payload={
        'LoginForm[username]':usrid,
        'LoginForm[password]':passwd,
        "yt0":""
    }

    session=requests.Session()

    request=session.post(url,data=payload)
    data=BeautifulSoup(request.text,"html.parser")
    result={}
    message=data.find(class_="flash-error")
    if message is None:
        result={"request":True,"session":session}
    else:
        result={"request":False,"message":message.text.strip()}
    return result


def get_attendance_full(usrid,passwd):
    url="https://sngce.etlab.in/ktuacademics/student/results"
    logged_in=get_loggedin(usrid,passwd)
    if logged_in["request"]==True:
        logged_in=logged_in["session"]
        data=logged_in.get(url)
        data_content=BeautifulSoup(data.content,"html.parser")
        odd=data_content.find_all(class_="odd")
        even=data_content.find_all(class_="even")
        result={}
        overall=0
        count=0   
        for i in even:
            val=i.find_all("td")
            try:
                result[val[0].text.strip()]={
                    "sub_name":val[1].text.strip().split("-")[-1],
                    "count":val[2].text.strip(),
                    "percent":val[3].text.strip()
                }
                overall+=int(val[3].text.strip().split("%")[0])
                count+=1
            except:
                continue
        for i in odd:
            val=i.find_all("td")
            try:
                result[val[0].text.strip()]={
                    "sub_name":val[1].text.strip().split("-")[-1],
                    "count":val[2].text.strip(),
                    "percent":val[3].text.strip()
                }
                overall+=int(val[3].text.strip().split("%")[0])
                count+=1
            except:
                continue
        if len(result)!=0:
            return {"Status":"Success","message":result,"overall_percent":overall//count}
        else:
            return {"Status":"Failed","message":"No Data retrived!!!"}


    
app=Flask(__name__)

@app.route("/")
def home():
    return message


@app.route("/get_cached_attendance")
def get_cached_attendance():
    data = r.get("attendance_data")
    if data:
        # Decode bytes to string before loading JSON
        decoded = data.decode('utf-8')
        return jsonify(json.loads(decoded))
    else:
        return jsonify({"error": "No data found"}), 404


@app.route("/get_attendance",methods=["POST"])
def attendancefull():
    if request.method=="POST":
        data=request.json
        if ("Username" in data) and ("Password" in data):
            usrname=data["Username"]
            passwd=data["Password"]
            data=get_attendance_full(usrname,passwd)
        else:
            data={"Status":"Failed","message":"Used parameters might be wrong use 'Username' for username and 'Password' for password"}
    return jsonify(data)


if __name__=="__main__":
    app.run()
