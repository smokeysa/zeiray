import datetime
import json
import getpass
import keyring

from simple_salesforce import Salesforce, SalesforceLogin, SFType

class TaskRay:
    def __init__(self):
        self._sf = None      # Salesforce object
        self._user_id = None
        self._session_id = None
        self._instance = None

    def get_password(self, username):
        password = keyring.get_password("salesforce", username)
        if password is None:
            password = getpass.getpass("Enter SF password:")
            keyring.set_password("salesforce", username, password)
        return password

    def login(self):
        if self._sf is not None:
            return # Already logged in

        login_info = json.load(open("sf_creds.json"))
        username = login_info["username"] # User name for logging into SF
        security_token = login_info["security_token"]
        user_id = login_info["user_id"]  # User ID for assigning owner in time entries.
        domain = "login"

        password = self.get_password(username)

        self._session_id, self._instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
        self._sf = Salesforce(instance=self._instance, session_id=self._session_id)

        self._user_id = user_id
        

    def create_time_entry(self, task, start, end):
        # Given two datetime objects, create a TaskRay TIME object.
        time_in_hours = (end - start).total_seconds() / 3600.0

        data = {
            "TASKRAY__Task__c" : task,
            "TASKRAY__Hours__c" : time_in_hours,
            "TASKRAY__Date__c" : start.isoformat(),
            "TASKRAY__trTimerStart__c": start.isoformat(),
            "TASKRAY__trTimerEnd__c": end.isoformat(),
            "TASKRAY__Owner__c" : self._user_id
        }

        print(data)
        
        trtime__c = SFType("TASKRAY__trTaskTime__c", self._session_id, self._instance)
        response = trtime__c.create(data)
        print(response)
        return response["success"]
        
