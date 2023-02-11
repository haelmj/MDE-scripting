from PySide6.QtWidgets import QDialog, QFileDialog, QVBoxLayout, QPushButton, QMessageBox
import csv, requests, logging
from app.progress_bar import ProgressBar
import threading


class BatchScan(QDialog):
    def __init__(self, access_token):
        super().__init__()

        self.setStyleSheet("""
            QProgressBar {
                text-align: center;
                border-style: solid;
                border-radius: 7px;
                border-width: 2px;
                border-color: grey;
            }

            QProgressBar::chunk {
                width: 2px;
                background-color: #de7c09;
                margin: 3px;
            }
        """)

        self.access_token = access_token

        
        v_layout = QVBoxLayout()
        self.select_file_button = QPushButton("Select a csv file")
        self.trigger_scan_button = QPushButton("Trigger Scan")

        v_layout.addWidget(self.select_file_button)
        v_layout.addWidget(self.trigger_scan_button)

        self.progressBar = ProgressBar()
        v_layout.addWidget(self.progressBar)
        self.setLayout(v_layout)

        self.select_file_button.clicked.connect(self.upload_file)
        self.trigger_scan_button.clicked.connect(self.trigger_scan)

        # add a check to prevent clicking trigger scan before file is selected

    def upload_file(self):
        self.select_file = QFileDialog().getOpenFileName(self, "Select File", filter="CSV (*.csv)")

        
    def trigger_scan(self):
        url = "https://api.securitycenter.microsoft.com/api/machines"
        headers = { 
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'Authorization' : "Bearer " + self.access_token
        }
        body = {"Comment": "Check machine for viruses","ScanType": "Full"}

        logging.basicConfig(filename="trigger.log", format='%(asctime)s %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        with open(self.select_file[0]) as f:
            csvreader = csv.reader(f)
            for row in list(csvreader):
                id = row[0]
                if id == "\ufeffDeviceId":
                    continue
                new_url = url + f"/{id}/runAntiVirusScan"
                response = requests.post(new_url, json=body, headers=headers)
                jsonResponse = response.json()
                self.update_progress_bar(self.calculate_percentage((csvreader.line_num - 1), 1))
                logger.info(jsonResponse)
            self.show_message_box('Scans Triggered Successfully!', "success")
    
    def update_progress_bar(self, i):
        t1 = threading.Thread(target=self.progressBar.updateBar, args=(i,))
        t1.start()

    def show_message_box(self, result, result_type):
        message = QMessageBox()
        message.setMinimumSize(700,200)
        message.setWindowTitle('Trigger Result')
        message.setText(result)
        message.setInformativeText("Logs saved to trigger.log")
        if result_type == 'success':
            message.setIcon(QMessageBox.Information)
        else:
            message.setIcon(QMessageBox.Warning)
        message.setStandardButtons(QMessageBox.Ok)

        message.exec()

    def calculate_percentage(self, total: int, current: int):
        division = current / total
        return round(division * 100)
