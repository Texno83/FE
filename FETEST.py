import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QEvent, QPoint, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QFileInfo, QFileIconProvider

# Импортируйте ваш код здесь (предположим, что он в файле file_explorer.py)
from file_explorer import Ui, font_ui, New_Folder_Ui, Save_File_Ui, Text_Editor_Ui, Rename_File_Ui

class TestFileExplorer(unittest.TestCase):

    def setUp(self):
        # Создаем mock-объекты для GUI и файловой системы
        self.mock_win = MagicMock() # Замените это на реальную загрузку UI, если это необходимо для работы тестов.
        self.mock_win.tabWidget.currentIndex.return_value = 0 # Для упрощения работы с табами.
        self.ui = Ui(self.mock_win)
        self.ui.tabs = [('/', self.ui.difs1, '/')] # Инициализация tabs.  Реальные тесты потребуют большей настройки.
        self.ui.disks = []

        # Добавьте необходимые атрибуты к self.mock_win, чтобы они соответствовали тому, что использует Ui.
        self.mock_win.ent1 = MagicMock()
        self.mock_win.favs = MagicMock()
        self.mock_win.left1 = MagicMock()
        self.mock_win.right1 = MagicMock()
        self.mock_win.tabWidget = MagicMock()
        self.mock_win.addToolBar = MagicMock()

    @patch('os.scandir')
    @patch('PyQt5.QtWidgets.QListWidgetItem')
    @patch('PyQt5.QtGui.QFileIconProvider.icon')
    @patch('PyQt5.QtCore.QFileInfo')
    def test_goto(self, mock_qfileinfo, mock_icon, mock_qlistwidgetitem, mock_scandir):
        # Настройка mock-объектов
        mock_entry1 = MagicMock()
        mock_entry1.is_file.return_value = False
        mock_entry1.is_dir.return_value = True
        mock_entry1.name = "TestDir"

        mock_entry2 = MagicMock()
        mock_entry2.is_file.return_value = True
        mock_entry2.is_dir.return_value = False
        mock_entry2.name = "TestFile.txt"
        mock_scandir.return_value.__enter__.return_value = [mock_entry1, mock_entry2]
        self.ui.win.ent1.text.return_value = "TestPath\\"

        # Вызов тестируемой функции
        self.ui.goto(self.ui.difs1)

        # Проверки
        mock_scandir.assert_called_with("TestPath\\")
        self.assertEqual(self.ui.difs1.clear.call_count, 1)
        self.assertEqual(mock_qlistwidgetitem.call_count, 2)

    @patch('os.startfile')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_open_folder_file(self, mock_isdir, mock_isfile, mock_startfile):
        mock_isfile.return_value = True
        mock_isdir.return_value = False
        mock_item = MagicMock()
        mock_item.text.return_value = "TestFile.txt"
        self.ui.tabs[0][1].selectedItems.return_value = [mock_item]
        self.ui.win.ent1.text.return_value = "TestPath\\"

        self.ui.open_folder()
        mock_startfile.assert_called_with("TestPath\\TestFile.txt")

    @patch('os.startfile')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_open_folder_dir(self, mock_isdir, mock_isfile, mock_startfile):
        mock_isfile.return_value = False
        mock_isdir.return_value = True
        mock_item = MagicMock()
        mock_item.text.return_value = "TestDir"
        self.ui.tabs[0][1].selectedItems.return_value = [mock_item]
        self.ui.win.ent1.text.return_value = "TestPath\\"

        self.ui.open_folder()
        self.assertEqual(self.ui.win.ent1.setText.call_count, 1)
        self.assertEqual(self.ui.goto.call_count, 1)

    @patch('shutil.rmtree')
    @patch('os.remove')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_delete_dir(self, mock_isfile, mock_isdir, mock_rmtree, mock_remove):
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        mock_item = MagicMock()
        mock_item.text.return_value = "TestDir"
        self.ui.tabs[0][1].selectedItems.return_value = [mock_item]
        self.ui.win.ent1.text.return_value = "TestPath\\"

        self.ui.delete()
        mock_rmtree.assert_called_with("TestPath\\TestDir", ignore_errors=True)
        self.assertEqual(mock_remove.call_count, 0)
        self.assertEqual(self.ui.goto.call_count, 1)

    @patch('shutil.rmtree')
    @patch('os.remove')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_delete_file(self, mock_isfile, mock_isdir, mock_rmtree, mock_remove):
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        mock_item = MagicMock()
        mock_item.text.return_value = "TestFile.txt"
        self.ui.tabs[0][1].selectedItems.return_value = [mock_item]
        self.ui.win.ent1.text.return_value = "TestPath\\"

        self.ui.delete()
        mock_remove.assert_called_with("TestPath\\TestFile.txt")
        self.assertEqual(mock_rmtree.call_count, 0)
        self.assertEqual(self.ui.goto.call_count, 1)

    @patch('shutil.copytree')
    @patch('shutil.copy')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_copy_paste_dir(self, mock_isfile, mock_isdir, mock_copy, mock_copytree):
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        mock_item = MagicMock()
        mock_item.text.return_value = "TestDir"
        self.ui.tabs[0][1].selectedItems.return_value = [mock_item]
        self.ui.win.ent1.text.return_value = "TestPath\\"

        self.ui.copy()
        self.ui.paste()
        mock_copytree.assert_called_with("TestPath\\TestDir", "TestPath\\TestDir")
        self.assertEqual(mock_copy.call_count, 0)
        self.assertEqual(self.ui.goto.call_count, 1)

    @patch('shutil.copytree')
    @patch('shutil.copy')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_copy_paste_file(self, mock_isfile, mock_isdir, mock_copy, mock_copytree):
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        mock_item = MagicMock()
        mock_item.text.return_value = "TestFile.txt"
        self.ui.tabs[0][1].selectedItems.return_value = [mock_item]
        self.ui.win.ent1.text.return_value = "TestPath\\"

        self.ui.copy()
        self.ui.paste()
        mock_copy.assert_called_with("TestPath\\TestFile.txt", "TestPath\\TestFile.txt")
        self.assertEqual(mock_copytree.call_count, 0)
        self.assertEqual(self.ui.goto.call_count, 1)

class TestFontUI(unittest.TestCase):
    def setUp(self):
        # Мок UI для Font
        self.mock_win = MagicMock()
        self.font_ui = font_ui(self.mock_win)
        self.font_ui.font_size = 14

        self.mock_text_editor_win = MagicMock()
        self.mock_text_editor_win.textEdit = MagicMock()
        self.font_ui.font_name = QFont()

        self.font_ui.button_connecter()

    def test_change_font_name(self):
        text_editor_window = MagicMock()
        text_editor_window.win = self.mock_text_editor_win
        text_editor_window.win.textEdit = MagicMock()

        self.font_ui.change_font_name("Arial")

        self.assertEqual(self.font_ui.font_name, "Arial")
        text_editor_window.win.textEdit.selectAll.assert_called_once()

    def test_change_font_size(self):
        text_editor_window = MagicMock()
        text_editor_window.win = self.mock_text_editor_win
        text_editor_window.win.textEdit = MagicMock()

        self.font_ui.change_font_size("14")

        self.assertEqual(self.font_ui.font_size, 14)
        text_editor_window.win.textEdit.selectAll.assert_called_once()


class TestNewFolderUI(unittest.TestCase):
    @patch('os.mkdir')
    def test_create(self, mock_mkdir):
        mock_win = MagicMock()
        new_folder_ui = New_Folder_Ui(mock_win)
        mock_win.lineEdit.text.return_value = "NewFolder"
        window = MagicMock()
        window.win = MagicMock()
        window.win.ent1.text.return_value = "TestPath\\"
        new_folder_ui.win = mock_win

        window.tabs = [( '/',MagicMock(), '/')]
        window.index = 0
        new_folder_ui.Create()

        mock_mkdir.assert_called_with("TestPath\\NewFolder")
        self.assertEqual(window.goto.call_count, 1)


class TestSaveFileUI(unittest.TestCase):
    @patch('builtins.open', create=True)
    def test_save(self, mock_open):
        mock_win = MagicMock()
        save_file_ui = Save_File_Ui(mock_win)
        mock_win.lineEdit.text.return_value = "TestFile.txt"
        window = MagicMock()
        window.win = MagicMock()
        window.win.ent1.text.return_value = "TestPath\\"
        save_file_ui.win = mock_win

        text_editor_window = MagicMock()
        text_editor_window.win = MagicMock()
        text_editor_window.win.textEdit = MagicMock()
        text_editor_window.win.textEdit.toPlainText.return_value = "Test content"
        save_file_ui.Save()

        self.assertEqual(window.goto.call_count, 1)


class TestTextEditorUI(unittest.TestCase):
    def test_Menu_Connecter(self):
        mock_win = MagicMock()
        text_editor_ui = Text_Editor_Ui(mock_win)
        text_editor_ui.win = mock_win

        mock_win.actionfile = MagicMock()
        mock_win.actionExit = MagicMock()
        mock_win.actionChange_font = MagicMock()
        text_editor_ui.Menu_Connecter()

        mock_win.actionfile.triggered.connect.assert_called_with(text_editor_ui.Save)
        mock_win.actionExit.triggered.connect.assert_called_with(text_editor_ui.Exit)
        mock_win.actionChange_font.triggered.connect.assert_called_with(text_editor_ui.change_font)


class TestRenameFileUI(unittest.TestCase):
    def test_rename(self):
        mock_win = MagicMock()
        rename_file_ui = Rename_File_Ui(mock_win)
        mock_win.lineEdit.text.return_value = "NewFile.txt"

        window = MagicMock()
        window.win = MagicMock()
        window.tabs = [( '/',MagicMock(), '/')]
        window.index = 0
        window.goto = MagicMock()
        window.copy = MagicMock()
        window.paste = MagicMock()
        window.delete = MagicMock()

        rename_file_ui.win = mock_win
        rename_file_ui.Rename()

        self.assertEqual(window.goto.call_count, 1)
        self.assertEqual(window.copy.call_count, 1)
        self.assertEqual(window.paste.call_count, 1)
        self.assertEqual(window.delete.call_count, 1)

if __name__ == '__main__':
    unittest.main()