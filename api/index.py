from flask import Flask,jsonify,request
import requests
from bs4 import BeautifulSoup


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
                overall+=int(val[3].text.strip())
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
            except:
                continue
        if len(result)!=0:
            result["overall_percent"]=overall//count
            return {"Status":"Success","message":result}
        else:
            return {"Status":"Failed","message":"No Data retrived!!!"}

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
            result[table_header[i].text.strip()]=table_value[i].text.strip()
        return {"Status":"Success","message":result}
    else:
        return {"Status":"Failed","message":logged_in["message"].strip()}

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
                    result[mini_data[0].text].append(mini_data[j].text.strip())
            except:
                continue
        return {"Status":"Success","message":result}
    else:
        return {"Status":"Failed","message":logged_in["message"].strip()}

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

@app.route("/get_attendance_full",methods=["POST"])
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
