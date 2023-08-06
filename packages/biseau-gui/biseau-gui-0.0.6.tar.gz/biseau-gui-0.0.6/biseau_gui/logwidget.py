from PySide2.QtWidgets import *
from PySide2.QtCore import *


class LogWidget(QWidget):
    def __init__(self, main_focus:callable):
        super().__init__()
        self.main_focus = main_focus
        self.tab_widget = QTabWidget()
        self.log_editor = QPlainTextEdit()
        self.erase_all()
        self.log_editor.cursorPositionChanged.connect(self.focus_on_click)

        _layout = QVBoxLayout()
        _layout.addWidget(self.tab_widget)
        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        self.tab_widget.setTabPosition(QTabWidget.South)
        self.add_widget(self.log_editor, "ASP syntax error")

    def add_widget(self, widget, name):
        self.tab_widget.addTab(widget, name)

    def add_message(self, msg, error=None):
        assert msg.count('\n') <= 1, (msg.replace('\n', '\\n'), msg.count('\n'))
        self.log_editor.appendPlainText(msg)
        self.last_line += 1  # NB: assume each msg is one line
        self.errors[self.last_line] = error

    def erase_all(self, msg:str=''):
        self.log_editor.setPlainText(msg)
        self.last_line = 0  # current line number, incremented at each self.add_message
        self.errors = {}  # line number -> ASPSyntaxError

    @Slot()
    def focus_on_click(self):
        cursor = self.log_editor.textCursor()
        lineno = cursor.blockNumber()
        # line = self.log_editor.toPlainText().splitlines()[lineno]
        # print(lineno, line)
        if lineno in self.errors:
            err = self.errors[lineno]
            self.main_focus('asp', err.lineno-1, err.offset-1)  # indexing starts at 0, but not for clingo
