import os.path

import requests
import json
from tools import get_headers,get_baseurl

format_suffix = {"MXLF":"mxliff","DOCX":"docx","TMX":"tmx","XLIFF":"xlf"}
class Project(object):
    def __init__(self,project_id):
        self.id = project_id
        self.__header = get_headers()
        self.baseurl = get_baseurl()


    def get_jobs(self):
        url = self.baseurl+"/web/api2/v2/projects/" + self.id + "/jobs"

        payload = {}

        job_list = []
        response = requests.request("GET", url, headers=self.__header, data=payload)
        print("status: " + str(response.status_code))
        if response.status_code==200:
            # res = response.json()['content']
            # for i in res:
            #     job_list.append(i['uid'])
            # pages = response.json()['totalPages']
            # print(type(pages))
            # if pages>1:
            #     for i in range(1,pages):
            #         url_new = url+"?pageNumber="+str(i)
            #         response = requests.request("GET", url_new, headers=self.__header, data=payload)
            #         if response.status_code == 200:
            #             res = response.json()['content']
            #             for i in res:
            #                 job_list.append(i['uid'])
            pages = response.json()['totalPages']
            for i in range(0, pages):
                url_new = url + "?pageNumber=" + str(i)
                response = requests.request("GET", url_new, headers=self.__header, data=payload)
                res = response.json()['content']
                for i in res:
                    job_list.append(i['uid'])
        return job_list

    def get_bilingual_files(self, format,target_folder):
        job_list = self.get_jobs()
        url = self.baseurl+"/web/api2/v1/projects/" + self.id + "/jobs/bilingualFile?format="+format+"&preview=true"
        bfiles_list = []
        for job_id in job_list:
            payload = json.dumps({
                "jobs": [
                    {
                        "uid": job_id
                    }
                ]
            })

            response = requests.request("POST", url, headers=self.__header, data=payload)
            print("status: " + str(response.status_code))
            file_name = "bilingual_"+job_id+"."+format_suffix[format]
            # print(response.text)
            file_path = os.path.join(target_folder,file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print("Save bilingual files under "+file_path)

        #     bfile = BilingualFile(response)
        #     bfiles_list.append(bfile)
        # return bfiles_list
    def get_job_number(self):
        url = self.baseurl + "/web/api2/v2/projects/" + self.id + "/jobs"

        payload = {}
        response = requests.request("GET", url, headers=self.__header, data=payload)
        print("status: " + str(response.status_code))
        if response.status_code == 200:
            res = response.json()['totalElements']
            print(res)


class BilingualFile(object):
    def __init__(self,response):
        self.response = response



class Client(object):
    def __init__(self,name):
        self.name = name
        self.__header = get_headers()
        self.baseurl = get_baseurl()

    def get_projects(self):
        url = self.baseurl+"/web/api2/v1/projects?clientName=" + self.name

        payload = {}

        project_list = []
        response = requests.request("GET", url, headers=self.__header, data=payload)
        print("status: " + str(response.status_code))
        if response.status_code==200:
            pages = response.json()['totalPages']
            for i in range(0, pages):
                url_new = url + "&pageNumber=" + str(i)
                response = requests.request("GET", url_new, headers=self.__header, data=payload)
                res = response.json()['content']
                for i in res:
                    project_list.append(i['uid'])
        return project_list

class User(object):
    def __init__(self,id):
        self.id = id
        self.__header = get_headers()
        self.baseurl = get_baseurl()

    def get_projects(self):
        url = self.baseurl+"/web/api2/v1/projects?ownerId=" + str(self.id)

        payload = {}

        project_list = []
        response = requests.request("GET", url, headers=self.__header, data=payload)
        print("status: " + str(response.status_code))
        if response.status_code==200:
            pages = response.json()['totalPages']
            for i in range(0, pages):
                url_new = url + "&pageNumber=" + str(i)
                response = requests.request("GET", url_new, headers=self.__header, data=payload)
                res = response.json()['content']
                for i in res:
                    project_list.append(i['uid'])
        return project_list



# from tools import update_token,get_baseurl
# project_id = "FgahGcykugbQ41GSQxbJq7"
# baseurl = get_baseurl()
# update_token()
# p = Project(project_id)
# p.get_job_number()
# p.get_bilingual_files("MXLF","C:\\Users\\AnZhou\\Downloads\\bilingual")

# from tools import update_token,get_baseurl
# client = Client("ADSK")
# print(client.get_projects())

from tools import update_token,get_baseurl
user = User(105332)
print(user.get_projects())