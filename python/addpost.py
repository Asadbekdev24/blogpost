from PyQt5.QtWidgets import QWidget
from components import Button, Input, Label, TextArea


class AddPostPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600, 400)
        self.setWindowTitle("Add Post Page")

        self.label = Label("Post yozish", self, 50)
        self.postTextArea = TextArea(self, 110)

        self.addPostBtn = Button("Add", self, 320)

    def yubor(self):
        print(type(self.postTextArea))