from PySide6.QtWidgets import QProgressBar
import time

class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setMaximum(100)
        self._active = False
    
    def updateBar(self, i):
        print(i)
        time.sleep(0.1)
        value = self.value() + i
        print(value)
        self.setValue(value)
        if value >= 50:
            self.changeColor('green')
        
        if value >= self.maximum() or self._active:
            self.setValue(100)

            
    
    def changeColor(self, color):
        css = """
        ::chunk {{
            background: {0};
        }}""".format(color)
        self.setStyleSheet(css)