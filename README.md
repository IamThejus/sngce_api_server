
# sngce-api-server

This is a simple API server hosted on Vercel that scrapes academic data from the SNGCE college website. The API provides endpoints for fetching student data from the specified academic institution.

## API Reference

#### POST Attendance


Request

    URL: https://sngce-api-server.vercel.app/get_attendance

    Method: POST


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Username`| `string` | **Required**. Your Sngce Username |
| `Password`  |  `string`| **Required**.Your Sngce Password |

#### POST Timetable


Request

    URL: https://sngce-api-server.vercel.app/get_timetable

    Method: POST


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Username`| `string` | **Required**. Your Sngce Username |
| `Password`  |  `string`| **Required**.Your Sngce Password |

#### POST Materials


Request

    URL: https://sngce-api-server.vercel.app/get_materials

    Method: POST


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Username`| `string` | **Required**. Your Sngce Username |
| `Password`  |  `string`| **Required**.Your Sngce Password |


#### Response

The response is similar for the requests which is in json format.

    {
        "Status":<Failed or Passed>,
        "message":<Data basesd on the request used>
    }


#### Sample requests

Using requests module in python

    import requests
    import json
    url1="https://sngce-api-server.vercel.app/get_attendance"
    usr_id=""     ## Your Username
    passwd=""     ## Your Password
    payload={
        "Username":usr_id,
        "Password":passwd
    }
    print(requests.post(url,json=payload).json())

Response

    {'Status': 'Success', 'message': {'UNi Reg No': 'SNG22CS###', 'Roll No':       'CS5255', 'Name': '######', 'CST301 ': '22/24 (92%) ', 'CST303 ': '15/17 (88%) ', 'CST305 ': '21/21 (100%) ', 'CST307 ': '14/17 (82%) ', 'CST309 ': '12/14 (86%) ', 'MCN301 ': '8/10 (80%) ', 'CSL331 ': '7/7 (100%) ', 'CSL333 ': '12/12 (100%) ', 'SSK ': '5/8 (63%) ', 'LNLAB ': '2/3 (67%) ', 'PLTLAB ': '1/1 (100%) ', 'Total': '119/134', 'Percentage': '89%'}}

Using Curl

    curl -X POST https://sngce-api-server.vercel.app/get_attendance \
     -H "Content-Type: application/json" \
     -d '{"Username": "<Your Username>, "Password": "<Your Password>"}'

Response

    {'Status': 'Success', 'message': {'UNi Reg No': 'SNG22CS###', 'Roll No':       'CS5255', 'Name': '####', 'CST301 ': '22/24 (92%) ', 'CST303 ': '15/17 (88%) ', 'CST305 ': '21/21 (100%) ', 'CST307 ': '14/17 (82%) ', 'CST309 ': '12/14 (86%) ', 'MCN301 ': '8/10 (80%) ', 'CSL331 ': '7/7 (100%) ', 'CSL333 ': '12/12 (100%) ', 'SSK ': '5/8 (63%) ', 'LNLAB ': '2/3 (67%) ', 'PLTLAB ': '1/1 (100%) ', 'Total': '119/134', 'Percentage': '89%'}}

#### Error Handling

The errors are automatically handled by the program and gives us the status of the request.

    {'Status': 'Failed', 'message': 'Invalid username or password. '}
    {'Status': 'Failed', 'message': 'Your account is locked due to too many failed     login attempts. Please try again later. '}
    {'Status': 'Failed', 'message': 'Your account is temporarily locked. Please try again after 5 minutes. '}

These are the errors that usually happens due to the user and server side issues.

#### Rate Limiting
This API doesnt have any rate limit for requests.However the etlab have limited the number of requests a users can request its about 5 requests/min (not Sure about the limit,try it yourself and let me know ),after which the Status response return Failed and and message will be "Your account is locked due to too many failed login attempts. Please try again later".So try to use the API under the given limit

#### Contact
* Email: thejusasokan123@gmail.com


