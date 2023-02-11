from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from profile import Profile

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        h_layout = QHBoxLayout()
        self.create_profile_button = QPushButton("Create Profile")
        self.select_profile_button = QPushButton("Select Profile")

        h_layout.addWidget(self.create_profile_button)
        h_layout.addWidget(self.select_profile_button)

        self.setLayout(h_layout)