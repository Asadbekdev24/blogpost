from PyQt5.QtWidgets import QApplication, QMessageBox, QListWidget, QWidget, QVBoxLayout, QTextEdit, QListWidgetItem

from mainpage import MainPage
from loginpage import LoginPage
from registerpage import RegisterPage
from myposts import MyPostsPage
from addpost import AddPostPage
from allposts import AllPostsPage

from components import TextArea

from database import Database
from errors import UsernameAlreadyExistsError
from os import system



system("cls")


class ListWidgetWithTextArea(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(50, 120, 350, 450)

    def addTextAreaItem(self, text: str):
        widget = QWidget()

        layout = QVBoxLayout()

        text_edit = TextArea(widget, 0)
        text_edit.setText(text)
        text_edit.setEnabled(False)

        layout.addWidget(text_edit)

        widget.setLayout(layout)

        item = QListWidgetItem()

        item.setSizeHint(widget.sizeHint())

        self.addItem(item)

        self.setItemWidget(item, widget)




class App:
    USER = None
    ALL_POSTS = []

    def __init__(self) -> None:
        self.boshSahifaOyna = MainPage()
        self.loginOyna = LoginPage()
        self.registerOyna = RegisterPage()
        self.meningPostlarimOyna = MyPostsPage()
        self.postQoshishOyna = AddPostPage()
        self.hammaPostlarOyna = AllPostsPage()

        self.database = Database()
        self.postsCollectionLW = ListWidgetWithTextArea(self.hammaPostlarOyna)
        self.myPostlarim=ListWidgetWithTextArea(self.meningPostlarimOyna)

        self.boshSahifaOyna.loginBtn.clicked.connect(self.showLoginPage)
        self.boshSahifaOyna.registerBtn.clicked.connect(self.showRegisterPage)

        self.loginOyna.loginBtn.clicked.connect(self.loginFunction)
        self.registerOyna.registerBtn.clicked.connect(self.registerFunction)

        self.boshSahifaOyna.show()


    def loginFunction(self):
        username = self.loginOyna.usernameInput.text()
        password = self.loginOyna.passwordInput.text()

        foundUser = self.database.login(username, password)

        if not foundUser:
            return self.alert("Foydalanuvchi nomi topilmadi!",1)

        self.USER = foundUser
        self.showAllPostsPage()


    def registerFunction(self):
        try:
            name = self.registerOyna.nameInput.text().strip()
            surname = self.registerOyna.surnameInput.text().strip()
            username = self.registerOyna.usernameInput.text().strip()
            password = self.registerOyna.passwordInput.text().strip()

            new_user = self.database.register(name, surname, username, password)
            self.USER = new_user

            return self.showAllPostsPage()
        except UsernameAlreadyExistsError as message:
            errorMessage = message.args[0]
            return self.alert(errorMessage,1)


    def alert(self, text: str, turi:int):
        msgbox = QMessageBox()
        if turi==1:
            msgbox.setIcon(QMessageBox.Warning)
        if turi==2:
            msgbox.setIcon(QMessageBox.Information)
        msgbox.setText(text)
        msgbox.setStandardButtons(QMessageBox.Ok)

        return msgbox.exec()


    def showLoginPage(self):
        self.loginOyna.show()
        self.boshSahifaOyna.close()


    def showRegisterPage(self):
        self.registerOyna.show()
        self.boshSahifaOyna.close()




    def showAllPostsPage(self):
        self.ALL_POSTS = self.database.selectAllPosts()

        for POST in self.ALL_POSTS:
            self.postsCollectionLW.addTextAreaItem(POST['text'])

        self.hammaPostlarOyna.show()
        self.postQoshishOyna.close()
        self.loginOyna.close()
        self.registerOyna.close()
        self.hammaPostlarOyna.writePostBtn.clicked.connect(self.yozish)
        self.hammaPostlarOyna.myPostsBtn.clicked.connect(self.myPost)

    def myPost(self):
        self.hammaPostlarOyna.close()
        post=self.database.selectUserPosts(self.USER['id'])
        for element in post:
            self.myPostlarim.addTextAreaItem(element['text'])
        self.meningPostlarimOyna.show()

    def yozish(self):
        self.hammaPostlarOyna.close()
        self.postQoshishOyna.show()
        self.postQoshishOyna.addPostBtn.clicked.connect(self.qoshish)
    def qoshish(self):
        user=self.USER
        tekst=self.postQoshishOyna.postTextArea.toPlainText()
        if tekst=="":
            self.alert("Siz ma'lumot kiritmadingiz!", 1)
        if tekst!="":
            self.database.addPost(user_id=user['id'],post_text=tekst)
            self.alert("Post qo'shildi!", 2)
            self.postQoshishOyna.close()
            self.showAllPostsPage()








app = QApplication([])

dastur = App()

app.exec()