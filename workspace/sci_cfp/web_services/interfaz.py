# -*- coding: utf-8 -*-
__author__ = 'NuSs'
import requests
import json

class Interfaz():
    def __init__(self):
        # Local settings
        # self.oneSignal_rest_key = "N2EwMTc4ZjYtOGVjNS00MzY5LWI3YzEtYmI1N2E3NzhmMjBm"
        # self.oneSignal_api_key = "bfbbc643-7bca-49dd-ba6d-cd831fe7f3f2"
        # 
        self.oneSignal_rest_key = "MWY0NTI1NjAtOTFkNS00NzVkLWIwZmItNGZkMTVkMzRkMmIx"
        self.oneSignal_api_key = "0a0f5b6b-6cf3-4c11-9239-0a9b4bee8ded"


    def send_push_web_notification(self, message):
        header = {"Content-Type": "application/json; charset=utf-8",
                  "Authorization": "Basic " + self.oneSignal_rest_key}

        payload = {"app_id": self.oneSignal_api_key,
                   "included_segments": ["All"],
                   "contents": {"en": message}}

        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

        print(req.status_code, req.reason)

    def send_mail_notification(self, to, message):

        payload = {"from": "sapazad@gmail.com",
                   "to": to,
                   "message": message}

        req = requests.post("http://localhost:8080/api/send_mail", data=json.dumps(payload))

        print(req.status_code, req.reason)

if __name__ == '__main__':
    interfaz = Interfaz()
    interfaz.send_push_web_notification("Hola Mundo")
    interfaz.send_mail_notification("sapazad@gmail.com", "Starting to send mail!")






