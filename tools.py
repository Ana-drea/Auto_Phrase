import requests
import json


def get_credentials():
    dict = {}
    for line in open('credentials.txt', encoding='utf-8'):
        line = line.strip('\n')
        key = line.split('=')[0]
        value = line.split('=')[1]
        dict[key] = value
    return dict


def get_baseurl():
    with open('baseurl.txt', 'r', encoding='utf-8') as file:
        baseurl = file.read().strip('\n')
        if len(baseurl)==0:
            baseurl = "https://cloud9.memsource.com"
        return baseurl


def get_headers():
    for line in open('token.txt', encoding='utf-8'):
        token = line.strip('\n')
    authorization = "ApiToken " + token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': authorization
    }
    return headers


def update_token():
    # url = "https://cloud9.memsource.com/web/api2/v3/auth/login"
    url = get_baseurl() + "/web/api2/v3/auth/login"

    dict = get_credentials()
    uname = dict['username']
    pword = dict['password']

    payload = json.dumps({
        "password": pword,
        "userName": uname
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    token = response.json()['token']
    print("status: " + str(response.status_code))
    with open('token.txt', 'w', encoding='utf-8') as file:
        file.write(token)


def get_jobs_from_id():
    # url = "https://cloud9.memsource.com/web/api2/v1/projects/Y0K7MFt1qdz9eAPQHfZbB1/jobs/search"
    url = get_baseurl() + "/web/api2/v1/projects/Y0K7MFt1qdz9eAPQHfZbB1/jobs/search"

    payload = json.dumps({
        "jobs": [
            {
                "uid": "nJologjzcLp98tjBhkJY02"
            }
        ]
    })
    headers = get_headers()

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json)


# def list_jobs_from_project(project_id):
#     url = "https://cloud9.memsource.com/web/api2/v2/projects/"+project_id+"/jobs"
#     id_list = []
#     payload = {}
#     headers = get_headers()
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#     res = response.json()['content']
#     for i in res:
#         id_list.append(i['uid'])
#     return id_list
#
# def download_bilingual_file(project_id):
#     url = "https://cloud9.memsource.com/web/api2/v1/projects/"+project_id+"/jobs/bilingualFile?format=XLIFF&preview=true"
#
#     id_list = list_jobs_from_project(project_id)
#
#     headers = get_headers()
#
#     for job_id in id_list:
#         payload = json.dumps({
#             "jobs": [
#                 {
#                     "uid": job_id
#                 }
#             ]
#         })
#
#         response = requests.request("POST", url, headers=headers, data=payload)
#
#         print(response.text)


def list_all_projects():
    update_token()

    url = get_baseurl() + "/web/api2/v1/projects"

    for line in open('token.txt', encoding='utf-8'):
        token = line.strip('\n')
    authorization = "ApiToken " + token

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': authorization
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def Create_project_from_template(template_id,project_name):
    update_token()

    url = get_baseurl() + "/web/api2/v2/projects/applyTemplate/"+template_id
    payload = json.dumps({
        "name": project_name
    })
    headers = get_headers()
    # headers['Accept'] = 'application/json'
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json()['uid'])


