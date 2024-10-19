import requests



def login(username:str,password:str,login_url:str)->requests.Session:
    with requests.Session() as s:
        login_payload = {
            "username": username,
            "password": password
        }
        s.post(login_url,data=login_payload)
        return s

