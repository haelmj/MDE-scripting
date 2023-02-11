from PySide6.QtWidgets import (
    QApplication
    ,QMainWindow
)
from app.start import StartScreen
from app.profile import Profile

# app opens showing graphical ui with option to select a profile or create a profile
# profiles represent different tenants or apps
# user selects create a profile and is asked to input a profile(client) name, tenant id and app id
# the user clicks the Create button and is then taken to the actions page
# on the actions page, the user clicks the upload file button as is prompted to select a csv file
# the user selects the csv and selects the action: trigger AV Scan.
# the scan is triggered and a page shows revealing the id's that were successful, those that were not compatible and those that were unsuccessful
# an option is presented to run another scan
# A switch profile icon is displayed at the top of the window


class MainApplication(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle('Azure PowerTool')

        # menubar and menus
        menu_bar = self.menuBar()
        quit_menu = menu_bar.addMenu("Tools")
        quit_menu.addAction("Quit")

        central_widget = StartScreen()
        self.profile = Profile()
        central_widget.create_profile_button.clicked.connect(self.create_profile_view)
        central_widget.select_profile_button.clicked.connect(self.select_profile_view)
        self.setCentralWidget(central_widget)

    def create_profile_view(self):
        self.profile.layout.addWidget(self.profile.profile_name)
        self.profile.layout.addWidget(self.profile.tenant_id)
        self.profile.layout.addWidget(self.profile.application_id)
        self.profile.layout.addWidget(self.profile.application_secret)
        self.profile.layout.addWidget(self.profile.create_profile_button)
        self.setCentralWidget(self.profile)
    
    def select_profile_view(self):
        self.select_view = self.profile.select_profile()
        if self.select_view is not None:
            self.setCentralWidget(self.profile)
    
    def quit_app(self):
        self.app.quit()

if __name__ == "__main__":
    app = QApplication([])

    window = MainApplication(app)
    window.show()

    app.exec()