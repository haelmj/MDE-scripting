import json
from PySide6.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QDialog, QMessageBox)
from app.batch_scan import BatchScan
import requests

class Profile(QDialog):
    def __init__(self, parent=None):
        super(Profile, self).__init__(parent)

        self.profile_name = QLineEdit()
        self.profile_name.setPlaceholderText("Enter Profile Name")
        self.tenant_id = QLineEdit()
        self.tenant_id.setPlaceholderText("Enter Tenant Id")
        self.application_id = QLineEdit()
        self.application_id.setPlaceholderText("Enter Application Id")
        self.application_secret = QLineEdit()
        self.application_secret.setPlaceholderText("Enter Application Secret")
        self.create_profile_button = QPushButton("Create")

        self.layout = QVBoxLayout(self)
        
        self.setLayout(self.layout)
        self.create_profile_button.clicked.connect(self.create_profile)
    
    def create_profile(self):
        print("Profile Created")
        self.save_profile(self.profile_name.text(), self.tenant_id.text(), self.application_id.text())
        self.access_token = self.get_access_token(self.tenant_id.text(), self.application_id.text(), self.application_secret.text())
        # create profile
        batch_scan_view = BatchScan(self.access_token)
        batch_scan_view.exec()
    
    def select_profile(self):
        self.data = self.load_profile()
        if self.data is not None:
            profile_names = [d["profile"] for d in self.data]
            for name in profile_names:
                profile_button = QPushButton(name, clicked=lambda a=name: self.use_profile(a))
                self.layout.addWidget(profile_button)
            return self.layout


    def get_access_token(self, tenantId, application_id, application_secret):
        url = f"https://login.microsoftonline.com/{tenantId}/oauth2/token"

        resourceAppIdUri = "https://api.securitycenter.microsoft.com"
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        body = {"resource": resourceAppIdUri,"client_id": application_id,"client_secret": application_secret,"grant_type": "client_credentials"}
        response = requests.post(url, body, headers)
        jsonResponse = response.json()
        aadToken = jsonResponse["access_token"]
        return aadToken

    def use_profile(self, name):
        for data in self.data:
            if data["profile"] == name:
                self.tenant_id = data['tenantID']
                self.application_id = data['appID']
                self.request_application_secret()
                break
        self.access_token = self.get_access_token(self.tenant_id, self.application_id, self.application_secret.text())
        batch_scan_view = BatchScan(self.access_token)
        batch_scan_view.exec()

    def save_profile(self, profile_name, tenantId, appId):
        data ={}
        data["profile"] = profile_name
        data['tenantID'] = tenantId
        data['appID'] = appId
        try:
            with open('app.json', 'r+') as f:
                content = json.load(f)
                content.append(data)
                f.seek(0)
                json.dump(content, f)
        except FileNotFoundError:
            content = [data]
            with open('app.json', 'w') as f:
                json.dump(content, f)
        
    def load_profile(self):
        try:
            with open('app.json', 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            QMessageBox.warning(self, 'Profile Not Found', 'No Saved Profiles Available',QMessageBox.Ok)

    def request_application_secret(self):
        newDialog = QDialog()
        self.application_secret = QLineEdit()
        self.application_secret.setPlaceholderText("Enter Application Secret")
        def submit():
            newDialog.close()
        submit_button = QPushButton("Submit", clicked=submit)
        layout = QVBoxLayout()
        layout.addWidget(self.application_secret)
        layout.addWidget(submit_button)
        
        newDialog.setLayout(layout)
        newDialog.exec()