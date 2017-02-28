# -*- coding: utf-8 -*-
__author__ = 'NuSs'
import requests
import json

import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Substitution, Mail
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib

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
        sg = sendgrid.SendGridAPIClient(apikey="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")
        my_template_id = 'd2111ea7-0cea-4e1c-a9ad-345cc0937958'
        from_email = Email("sapazad@gmail.com")
        subject = "Hello World from the SendGrid Python Library!"
        to_email = Email(to)
        content = Content("text/html", "I'm replacing the <strong>body tag</strong>")
        mail = Mail(from_email, subject, to_email, content)
        # mail.personalizations[0].add_substitution(Substitution("-name-", "Example User"))
        # mail.personalizations[0].add_substitution(Substitution("-city-", "Denver"))
        mail.set_template_id(my_template_id)
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except urllib.HTTPError as e:
            print e.read()
            exit()
        print(response.status_code)
        print(response.body)
        print(response.headers)

if __name__ == '__main__':
    interfaz = Interfaz()
    interfaz.send_push_web_notification("Hola Mundo")
    interfaz.send_mail_notification("sapazad@gmail.com", "Starting to send mail!")






