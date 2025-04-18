from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
import getpass
import shutil
import pathlib
# import pyperclip
import pathlib
# import stat
import psutil
# import typing
# import copy


def set_icon(win):
    window_icon = QIcon()
    window_icon.addFile('FE.ico', QSize(16, 16))
    window_icon.addFile('FE.ico', QSize(24, 24))
    window_icon.addFile('FE.ico', QSize(32, 32))
    window_icon.addFile('FE.ico', QSize(48, 48))
    window_icon.addFile('FE.ico', QSize(64, 64))
    window_icon.addFile('FE.ico', QSize(128, 128))
    window_icon.addFile('FE.ico', QSize(256, 256))
    win.setWindowIcon(window_icon)


class Ui(QtWidgets.QMainWindow):
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.tabs = []
        self.win.adjustSize()
        self.win.resize(800, 600)
        self.index = self.win.tabWidget.currentIndex()
        #self.dir1 = '/'
        self.difs1 = QListWidget()
        self.difs1.installEventFilter(self)
        self.start_appearence()
        self.button_connecter(self.tabs[self.index][1])
        #====================================================
        self.win.show()
        #====================================================


    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source in self.tabs[self.index]:
            self.right_menu(event)
        return super().eventFilter(source, event)


    def goto_fav_folder(self):
        listwidget = self.difs1
        #self.win.ent1.setText()
        sel = list(self.win.favs.selectedItems())
        for i in range(len(sel)):
            sel[i] = sel[i].text()
        items = [self.win.favs.item(i).text() for i in range(self.win.favs.count())]
        print(items)
        for i in range(len(items)):
            if items[i] == sel[0]:
                self.win.ent1.setText(self.default_ways_for_windows[i])
                self.goto(listwidget)
                break


    def right_menu(self, event):
        menu = QMenu()
        # options
        open_option = menu.addAction('Open')
        copy_option = menu.addAction('Copy')
        cut_option = menu.addAction('Cut')
        paste_option = menu.addAction('Paste')
        delete_option = menu.addAction('Delete')
        rename_option = menu.addAction('Rename')
        create_file = menu.addAction('Create file')
        create_folder = menu.addAction('Create_folder')
        
        #customize_option = menu.addAction('Customize')
        """
        newtab_option = menu.addAction('Open in new tab')
        newwinow_option = menu.addAction('Open in new window')
        """
        open_option.triggered.connect(self.open_folder)
        copy_option.triggered.connect(self.copy)
        cut_option.triggered.connect(self.cut)
        paste_option.triggered.connect(self.paste)
        delete_option.triggered.connect(self.delete)
        rename_option.triggered.connect(self.rename)
        create_file.triggered.connect(self.create_file)
        create_folder.triggered.connect(self.create_folder)
        #customize_option.triggered.connect(self.customize)
        """
        newtab_option.triggered.connect(self.open_in_new_tab)
        newwinow_option.triggered.connect(self.open_in_new_window)
        """
        coords = QPoint(self.win.x() + event.x() + 131, self.win.y() + event.y() + 61)
        print(coords.x(), coords.y())
        menu.exec_(self.mapToGlobal(coords))


    def rename(self):
        rename_file_window.win.show()


    def create_folder(self):
        new_folder_window.win.show()


    def create_file(self):
        #os.startfile('C:\\Windows\\notepad.exe')
        text_editor_window.win.show()
        self.goto(self.tabs[self.index][1])


    def customize(self):
        font_window.win.setFocus(True)
        font_window.win.activateWindow()
        font_window.win.raise_()
        font_window.win.show()


    def open_in_new_window(self):
        listwidget = self.difs1
        sel = list(listwidget.selectedItems())
        for i in range(len(sel)):
            sel[i] = sel[i].text()
        self.dir1 = self.win.ent1.text()
        s = self.dir1 + ''.join(sel)
        if os.path.isfile(s): os.startfile(s)
        elif os.path.isdir(s):
            win = uic.loadUi('ui.ui')
            new_window = Ui(win)
            new_window.win.ent1.setText(s + '\\')
            new_window.show()


    def start_appearence(self):
        # adds layout
        self.centralwidget = QWidget()
        self.win.setCentralWidget(self.centralwidget)
        self.grid = QGridLayout(self.centralwidget)
        toplayout = QHBoxLayout()
        lay = QVBoxLayout()
        toplayout.addWidget(self.win.left1)
        toplayout.addWidget(self.win.right1)
        lay.addLayout(toplayout)
        lay.addWidget(self.win.favs)
        filelayout = QVBoxLayout()
        filelayout.addWidget(self.win.ent1)
        filelayout.addWidget(self.win.tabWidget)
        self.grid.addLayout(lay, 0, 0)
        self.grid.addLayout(filelayout, 0, 1, 0, 4)
        self.win.favs.setFixedWidth(120)
        self.win.left1.setFixedWidth(55)
        self.win.right1.setFixedWidth(55)
        # goes to C:\\ 
        if self.win.ent1.text() == '':
            self.dir1 = 'C:\\'
            self.win.ent1.setText('C:\\')
        else:
            self.dir1 = self.win.ent1.text()
        self.goto(listwidget=self.difs1)
        # adds default ways
        user = getpass.getuser()
        self.default_ways_for_windows = ["C:\\Users\\" + user + "\\"] * 7
        self.default_ways_names = ['', 'Desktop\\', 'Documents\\', 'Downloads\\', 'Music\\', 'Pictures\\', 'Videos\\', 'Trash\\']
        for i in range(len(self.default_ways_for_windows)): self.default_ways_for_windows[i] += self.default_ways_names[i]
        self.default_ways_names[0] = user
        for i in range(7): self.win.favs.addItem(self.default_ways_names[i])
        # adds disks labels
        diskparts = psutil.disk_partitions()
        self.disks = list()
        for i in range(len(diskparts)):
            self.win.favs.addItem(diskparts[i].mountpoint)
            self.disks.append(diskparts[i].mountpoint)
        self.win.favs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.win.favs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
       # self.win.favs.setFixedSize(111, self.win.favs.sizeHintForRow(0) * self.win.favs.count() + 2 * self.win.favs.frameWidth())
        self.default_ways_for_windows += self.disks
        # set window icon
        set_icon(self.win)
        # adds first tab
        self.tabs.append((self.dir1, self.difs1, self.win.ent1.text()))
        self.win.tabWidget.addTab(self.difs1, self.dir1)
        self.win.tabWidget.setTabShape(QTabWidget.TabShape.Triangular)
        self.win.tabWidget.setTabsClosable(True)
        # adds size
        self.difs1.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # creates font variable 
        self.font1 = QFont(self.difs1.font())
        # set number of copyes
        self.i = 1
        # set global dir variable
        self.global_dir = ''
        # add hotkeys
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self.win)
        self.shortcut_copy = QShortcut(QKeySequence('Ctrl+C'), self.win)
        self.shortcut_cut = QShortcut(QKeySequence('Ctrl+X'), self.win)
        self.shortcut_paste = QShortcut(QKeySequence('Ctrl+V'), self.win)
        self.shortcut_rename = QShortcut(QKeySequence('Ctrl+R'), self.win)
        self.shortcut_delete = QShortcut(QKeySequence('Shift+Delete'), self.win)
        self.shortcut_open.activated.connect(self.open_folder)
        self.shortcut_copy.activated.connect(self.copy)
        self.shortcut_cut.activated.connect(self.cut)
        self.shortcut_paste.activated.connect(self.paste)
        self.shortcut_rename.activated.connect(self.rename)
        self.shortcut_delete.activated.connect(self.delete)
        # add toolbar
        copy_action = QAction(QIcon('Copy.svg'), 'Copy', self.win)
        cut_action = QAction(QIcon('Cut.svg'), 'Cut', self.win)
        paste_action = QAction(QIcon('Paste.svg'), 'Paste', self.win)
        rename_action = QAction(QIcon('Rename.svg'), 'Rename', self.win)
        delete_action = QAction(QIcon('Delete.svg'), 'Delete', self.win)
        copy_action.setShortcut('Ctrl+C')
        cut_action.setShortcut('Ctrl+X')
        paste_action.setShortcut('Ctrl+V')
        rename_action.setShortcut('Ctrl+R')
        delete_action.setShortcut('Shift+Delete')
        copy_action.triggered.connect(self.copy)
        cut_action.triggered.connect(self.cut)
        paste_action.triggered.connect(self.paste)
        rename_action.triggered.connect(self.rename)
        delete_action.triggered.connect(self.delete)
        self.win.toolbar = self.win.addToolBar('toolbar')
        self.win.toolbar.addAction(copy_action)
        self.win.toolbar.addAction(cut_action)
        self.win.toolbar.addAction(paste_action)
        self.win.toolbar.addAction(rename_action)
        self.win.toolbar.addAction(delete_action)


    def button_connecter(self, listwidget):        
        self.win.favs.itemClicked.connect(self.goto_fav_folder)
        listwidget.itemClicked.connect(self.open_folder)
        self.win.left1.clicked.connect(self.goleft)
        self.win.right1.clicked.connect(self.goright)


    def goto(self, listwidget):
        lof2 = list()
        list_of_folders = list(); list_of_files = list()
        dir = self.win.ent1.text()
        try:
            listwidget.clear()
            with os.scandir(dir) as files:
                for file in files:
                    lof2.append(file.name)
                    if os.path.isfile(file):list_of_files.append(file.name)
                    if os.path.isdir(file): list_of_folders.append(file.name)
            for i in list_of_folders:
                filedir_info = QFileInfo(dir+i)
                iconprovider = QFileIconProvider()
                dir_icon = iconprovider.icon(filedir_info)
                item = QtWidgets.QListWidgetItem(i)
                item.setIcon(dir_icon)
                listwidget.addItem(item)
            for i in list_of_files:
                filedir_info = QFileInfo(dir+i)
                iconprovider = QFileIconProvider()
                dir_icon = iconprovider.icon(filedir_info)
                item = QtWidgets.QListWidgetItem(i)
                item.setIcon(dir_icon)
                listwidget.addItem(item)
            if self.win.ent1.text() == '': self.win.ent1.setText(dir)
            if dir[-1] != '\\': self.win.ent1.insert('\\')
            self.change_tab_text(dir)
        except NotADirectoryError: pass
        except OSError: pass


    def open_in_new_tab(self):
        self.index = self.win.tabWidget.currentIndex()
        listbox = QListWidget()
        dir = self.win.ent1.text()
        self.win.tabWidget.addTab(listbox, self.win.ent1.text())
        self.tabs.append((self.win.ent1.text(), listbox, dir))
        self.tabs[self.index+1][1].itemClicked.connect(self.open_folder)
        self.win.ent1.setText(self.tabs[self.index+1][2])
        self.goto(self.tabs[self.index+1][1])


    def open_folder(self):
        listwidget = self.tabs[self.index][1]
        sel = list(listwidget.selectedItems())
        for i in range(len(sel)):
            sel[i] = sel[i].text()
        self.dir1 = self.win.ent1.text()
        s = self.dir1 + ''.join(sel)
        try:
            if os.path.isfile(s): os.startfile(s)
            elif os.path.isdir(s):
                self.win.ent1.setText(s + '\\')
                self.goto(listwidget)
        except PermissionError: pass
        except OSError: pass


    def change_tab_text(self, s):
        index = self.win.tabWidget.currentIndex()
        filename = ''
        try:
            for i in range(s[:-1].rindex('\\') + 1, len(s[:-1])): filename += s[i]
            self.win.tabWidget.setTabText(index, filename)
        except ValueError:
            for i in range(len(s)): filename += s[i]
            self.win.tabWidget.setTabText(index, filename)


    def delete(self):
        listwidget = self.tabs[self.index][1]
        if self.global_dir == '':
            sel = list(listwidget.selectedItems())
            for i in range(len(sel)):
                sel[i] = sel[i].text()
                self.dir1 = self.win.ent1.text()
            #dir = copy.copy(self.dir1)
            self.dir1 += ''.join(sel)
            print(self.dir1)
        else:
            self.dir1 = self.dir_to_copy
        try:
            if os.path.isdir(self.dir1): shutil.rmtree(self.dir1, ignore_errors=True)
            elif os.path.isfile(self.dir1): os.remove(self.dir1)
        except PermissionError: pass
        else: self.goto(listwidget)
        self.global_dir = ''


    def copy(self):
        listwidget = self.tabs[self.index][1]
        sel = list(listwidget.selectedItems())
        for i in range(len(sel)): sel[i] = sel[i].text()
        self.dir_to_copy = self.win.ent1.text() + ''.join(sel)
        self.dirname = ''.join(sel)
        self.remove_after_paste = False
        self.global_dir = ''


    def cut(self):
        self.copy(listwidget = self.tabs[self.index][1])
        self.remove_after_paste = True
        self.global_dir == ''


    def paste(self):
        listwidget = self.tabs[self.index][1]
        if self.global_dir == '': self.dir_to_paste = self.win.ent1.text() + self.dirname
        else: self.dir_to_paste = self.global_dir
        #for item in self.dir_to_paste:
        if os.path.isdir(self.dir_to_copy):
            try:
                shutil.copytree(self.dir_to_copy, self.dir_to_paste[:len(self.dir_to_paste)])
                self.goto(listwidget)
            except PermissionError: pass
            except FileExistsError: pass
        elif os.path.isfile(self.dir_to_copy):
            print(self.dir_to_copy)
            try:
                shutil.copy(self.dir_to_copy, self.dir_to_paste)
            except:
                SDTP, SDTPext = os.path.splitext(self.dir_to_paste)
                shutil.copy(self.dir_to_copy, SDTP + f'copy({self.i})' + SDTPext)
                self.i += 1
            self.goto(listwidget)
        if self.remove_after_paste:
            try:
                if os.path.isdir(self.dir_to_copy): shutil.rmtree(self.dir_to_copy, ignore_errors=True)
                elif os.path.isfile(self.dir_to_copy): os.remove(self.dir_to_copy)
            except PermissionError: pass
            else: self.goto(listwidget)
            self.i = 1


    def goleft(self):
        listwidget = self.tabs[self.index][1]
        sel = list(listwidget.selectedItems())
        disks = [self.disks[i] for i in range(len(self.disks))]
        print(disks)
        for i in range(len(sel)): sel[i] = sel[i].text()
        dir = self.win.ent1.text() + ''.join(sel)
        self.closed_dir = self.win.ent1.text() + ''.join(sel)
        #self.closed_dir.replace(chr(92), '\\')
        s = str(pathlib.Path(dir).parent.absolute())
        if s not in disks: self.win.ent1.setText(s + '\\')
        else: self.win.ent1.setText(s)
        self.goto(listwidget)


    def goright(self):
        listwidget = self.tabs[self.index][1]
        try: self.win.ent1.setText(self.closed_dir)
        except AttributeError: pass
        else: self.goto(listwidget)


class font_ui(QtWidgets.QMainWindow):
    def __init__(self, win):
        super().__init__()
        global text_editor_window
        self.win = win
        self.font_name = QFont()
        self.font_size = 2
        set_icon(self.win)
        self.win.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(201, 22)
        self.button_connecter()
        # adds fonts size
        self.win.fsize.setEditable(True)
        for i in range(2, 102, 2):
            self.win.fsize.addItems([str(i)])


    def button_connecter(self):
        self.win.apply.clicked.connect(self.set_font)
        self.win.fname.activated[str].connect(self.change_font_name)
        self.win.fsize.activated[str].connect(self.change_font_size)


    def change_font_name(self, font_name):
        self.font_name = font_name
        cursor = text_editor_window.win.textEdit.textCursor()
        text_editor_window.win.textEdit.selectAll()
        try: text_editor_window.win.textEdit.setFont(QFont(self.font_name, self.font_size))
        except TypeError: pass
        text_editor_window.win.textEdit.setTextCursor(cursor)


    def change_font_size(self, font_size):
        self.font_size = int(font_size)
        cursor = text_editor_window.win.textEdit.textCursor()
        text_editor_window.win.textEdit.selectAll()
        try: text_editor_window.win.textEdit.setFont(QFont(self.font_name, self.font_size))
        except TypeError: pass
        text_editor_window.win.textEdit.setTextCursor(cursor)


    def set_font(self):
        self.win.close()


class New_Folder_Ui(QMainWindow):
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.win.setFixedSize(271, 95)
        set_icon(self.win)
        self.Button_Connecter()


    def Button_Connecter(self):
        self.win.cancel_button.clicked.connect(self.Cancel)
        self.win.create_button.clicked.connect(self.Create)


    def Create(self):
        self.new_folder_name = self.win.lineEdit.text()
        os.mkdir(window.win.ent1.text() + self.new_folder_name)
        window.goto(window.tabs[window.index][1])
        new_folder_window.win.close()


    def Cancel(self):
        self.win.close()


class Save_File_Ui(QMainWindow):
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.win.setFixedSize(271, 95)
        set_icon(self.win)
        self.Button_Connecter()


    def Button_Connecter(self):
        self.win.cancel_button.clicked.connect(self.Cancel)
        self.win.create_button.clicked.connect(self.Save)


    def Save(self):
        self.new_file_name = self.win.lineEdit.text()
        f = open(window.win.ent1.text() + self.win.lineEdit.text(), 'w')
        f.write(text_editor_window.win.textEdit.toPlainText())
        window.goto(window.tabs[window.index][1])
        save_file_window.win.close()


    def Cancel(self):
        self.win.close()


class Text_Editor_Ui(QMainWindow):
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.win.resize(640, 480)
        set_icon(self.win)
        self.centralwidget = QWidget()
        self.win.setCentralWidget(self.centralwidget)
        self.grid = QGridLayout(self.centralwidget)
        self.grid.addWidget(self.win.textEdit, 0, 0)
        self.font_size = 14
        self.font1 = QFont(self.win.textEdit.font())
        self.Menu_Connecter()


    def Menu_Connecter(self):
        self.win.actionfile.triggered.connect(self.Save)
        self.win.actionExit.triggered.connect(self.Exit)
        self.win.actionChange_font.triggered.connect(self.change_font)


    def change_font(self):
        font_window.win.show()


    def Save(self):
        save_file_window.win.show()


    def Exit(self):
        self.win.textEdit.setText('')
        self.win.close()


class Rename_File_Ui(QMainWindow):
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.win.setFixedSize(271, 95)
        set_icon(self.win)
        self.Button_Connecter()


    def Button_Connecter(self):
        self.win.cancel_button.clicked.connect(self.Cancel)
        self.win.create_button.clicked.connect(self.Rename)


    def Rename(self):
        self.new_file_name = self.win.lineEdit.text()
        window.copy()
        listwidget = window.tabs[window.index][1]
        sel = list(listwidget.selectedItems())
        for i in range(len(sel)): sel[i] = sel[i].text()
        dir = window.win.ent1.text() + ''.join(sel)
        window.dir_to_copy = dir
        window.global_dir = window.win.ent1.text() + self.win.lineEdit.text()
        #window.SDTP, window.SDTPext = os.path.splitext(window.global_dir)
        window.paste()
        window.delete()
        window.goto(listwidget)
        rename_file_window.win.close()


    def Cancel(self):
        self.win.close()


app = QtWidgets.QApplication(sys.argv)
win = uic.loadUi('fileexplorer.ui')
window = Ui(win)
font_win = uic.loadUi('font_menu.ui')
font_window = font_ui(font_win)
folder_win = uic.loadUi('new_folder.ui')
new_folder_window = New_Folder_Ui(folder_win)
text_editor_win = uic.loadUi('text_editor.ui')
text_editor_window = Text_Editor_Ui(text_editor_win)
save_file_win = uic.loadUi('save_file.ui')
save_file_window = Save_File_Ui(save_file_win)
rename_file_win = uic.loadUi('rename_file.ui')
rename_file_window = Rename_File_Ui(rename_file_win)
app.exec_()
