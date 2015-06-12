# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:07:19 2015
@author: xngli
A program to generate G-code for shapeoko
The G-code is to move the spindle along z direction on defined step size
"""
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('G-code Generator')

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
    
    def on_about(self):
        msg = """ A program to generate G-code for Shapeoko
        
        """
        QMessageBox.about(self, "About the demo", msg.strip())
        
    def generate(self):
        self.display.clear()
        self.display.append('G21 G90 G17\nG92 X0 Y0 X0')
        i = 0
        count = self.spinbox_count.value()
        step_size = self.spinbox_size.value()
        while i <= count:
            z = step_size * i
            self.display.append('G0 Z%.3f' % z)
            self.display.append('G4 P5')
            i = i + 1
    
    def save(self):
        file_choices = ".nc"
        path = QFileDialog.getSaveFileName(self, 
                        'Save G-code', 
                        '', 
                        file_choices)
        if path:
            output = open(path, 'w')
            output.write(self.display.toPlainText())
            self.statusBar().showMessage('Saved to %s' % path, 5000)
    
    def create_main_frame(self):
        self.main_frame = QWidget()
        grid = QGridLayout()
         
        self.label_size = QLabel('Step size (mm)')
        grid.addWidget(self.label_size, 0, 0)
        self.spinbox_size = QDoubleSpinBox()
        grid.addWidget(self.spinbox_size, 1, 0)
        
        self.label_count = QLabel('Step count')
        grid.addWidget(self.label_count, 2, 0)
        self.spinbox_count = QSpinBox()
        grid.addWidget(self.spinbox_count, 3, 0)
        
        self.generate_button = QPushButton("&Generate")
        grid.addWidget(self.generate_button, 4, 0)
        self.connect(self.generate_button, SIGNAL('clicked()'), self.generate)
        
        self.save_button = QPushButton("&Save")
        grid.addWidget(self.save_button, 5, 0)
        self.connect(self.save_button, SIGNAL('clicked()'), self.save)
        
        self.display = QTextEdit('Area for displaying generated G-code.')
        grid.addWidget(self.display, 0, 1, 6, 1)
        
        self.main_frame.setLayout(grid)
        self.setCentralWidget(self.main_frame)
    
    def create_status_bar(self):
        self.status_text = QLabel("This is a demo")
        self.statusBar().addWidget(self.status_text, 1)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (quit_action,))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()