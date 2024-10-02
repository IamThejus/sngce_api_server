from flask import Flask,jsonify,request
import requests
from bs4 import BeautifulSoup


message="This is an API Server.\nInorder to acess you can use get_attendance,get_timetable,get_materials\nUse Username and Password as payload"

url="https://sngce.etlab.in/user/login"

def check_n(data):
    split_n=data.split("\n")
    if len(split_n)==1:
        return split_n[0]
    else:
        for i in split_n:
            if len(i)>0:
                return i
            
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
        result={"request":False,"message":check_n(message.text)}
    return result




def get_attendance(usrid,passwd):
    attendance="https://sngce.etlab.in/ktuacademics/student/viewattendancesubject/11"
    logged_in=get_loggedin(usrid,passwd)
    if logged_in["request"]==True:
        logged_in=logged_in["session"]
        data=logged_in.get(url=attendance)
        data_content=BeautifulSoup(data.content,"html.parser")
        result={}
        table_header=data_content.find_all("th")
        table_value=data_content.find_all("td")
        for i in range(len(table_header)):
            result[check_n(table_header[i].text)]=check_n(table_value[i].text)
            ordered_keys = ['Name', 'UNi Reg No', 'Roll No'] + \
                   [key for key in result if key not in ['Name', 'UNi Reg No', 'Roll No', 'Percentage']] + \
                   ['Percentage']
            result = {key: result[key] for key in ordered_keys}
        return {"Status":"Success","message":result}
    else:
        return {"Status":"Failed","message":logged_in["message"]}

def get_time_table(usrid,passwd):
    timetable="https://sngce.etlab.in/student/timetable"
    logged_in=get_loggedin(usrid,passwd)
    if logged_in["request"]==True:
        logged_in=logged_in["session"]
        data=logged_in.get(url=timetable)
        data_content=BeautifulSoup(data.content,"html.parser")
        data=data_content.find_all("tr")
        result={}
        for i in data:
            try:
                mini_data=i.find_all("td")
                result[mini_data[0].text]=[]
                for j in range(1,len(mini_data)):
                    result[mini_data[0].text].append(check_n(mini_data[j].text))
            except:
                continue
        return {"Status":"Success","message":result}
    else:
        return {"Status":"Failed","message":logged_in["message"]}

def get_materials(userid,passwd):
    url="https://sngce.etlab.in/student/materials"
    logged_in=get_loggedin(userid,passwd)
    if logged_in["request"]==True:
        logged_in=logged_in["session"]
        data=logged_in.get(url)
        data_content=BeautifulSoup(data.content,"html.parser")
        new_data=data_content.find_all('tr')
        result=[]
        headers=[]
        datas=new_data[0].find_all("th")
        for m in datas:
            headers.append(m.text)
        for i in range(1,len(new_data)):
            try:
                data={}
                mini_data=new_data[i].find_all("td")
                for j in range(len(mini_data)):
                    if j!=6:
                        data[headers[j]]=mini_data[j].text
                    else:
                        if mini_data[j].find("a").get("href")==None:
                            data[headers[j]]=None
                        else:
                            data[headers[j]]="https://sngce.etlab.in"+str(mini_data[j].find("a").get("href"))
                result.append(data)
            except:
                continue
        return {"Status":"Success","message":result}
    else:
        return {"Status":"Failed","message":logged_in["message"]}

app=Flask(__name__)

@app.route("/")
def home():
    return message
@app.route("/get_attendance",methods=["POST"])
def attendance():
    if request.method=="POST":
        data=request.json
        if ("Username" in data) and ("Password" in data):
            usrname=data["Username"]
            passwd=data["Password"]
            data=get_attendance(usrname,passwd)
        else:
            data={"Status":"Failed","message":"Used parameters might be wrong use 'Username' for username and 'Password' for password"}
    return jsonify(data)


@app.route("/get_timetable",methods=["POST"])
def timetable():
    if request.method=="POST":
        data=request.json
        if ("Username" in data) and ("Password" in data):
            usrname=data["Username"]
            passwd=data["Password"]
            data=get_attendance(usrname,passwd)
        else:
            data={"Status":"Failed","message":"Used parameters might be wrong use 'Username' for username and 'Password' for password"}
    return jsonify(data)

@app.route("/get_materials",methods=["POST"])
def materials():
    if request.method=="POST":
        data=request.json
        if ("Username" in data) and ("Password" in data):
            usrname=data["Username"]
            passwd=data["Password"]
            data=get_attendance(usrname,passwd)
        else:
            data={"Status":"Failed","message":"Used parameters might be wrong use 'Username' for username and 'Password' for password"}
    return jsonify(data)


if __name__=="__main__":
    app.run()