"""Definition of the ASP viewer"""
import biseau as bs
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


# color used to highlight the syntax errors
ERR_LINE_COLOR = QColor(255, 0, 0, 40)
ERR_WORD_COLOR = QColor(255, 0, 0, 80)


class ASPViewer(QWidget):
    """A view on ASP code, able to transmit dot to another widget"""
    def __init__(self, next_viewer):
        super().__init__()
        self.setWindowTitle("ASP")
        self.multishot_mode = False

        self._next_viewer = next_viewer
        self.tool_bar = QToolBar()
        self.tool_bar.addAction('Compile to dot/models',
                                lambda: self.set_asp(self.get_asp()))
        self.editor = QTextEdit()
        self.editor.setFont('Monospace')
        _layout = QVBoxLayout()
        _layout.addWidget(self.tool_bar)
        _layout.addWidget(self.editor)
        _layout.setContentsMargins(0, 0, 0, 0)
        self.set_asp('')
        self.setLayout(_layout)

    def _setup_toolbar(self):
        "Populate the toolbar"

    def set_asp(self, source, compile_and_send=True):
        self.editor.setText(source)
        if not compile_and_send:  return

        if hasattr(self._next_viewer, 'set_dot'):
            if self.multishot_mode:
                dots = bs.compile_context_to_dots(source)
                self._next_viewer.set_dots(dots)
            else:
                dot = bs.compile_context_to_dot(source)
                self._next_viewer.set_dot(dot)
        elif hasattr(self._next_viewer, 'set_models'):
            models = bs.script.solve_context(source)
            self._next_viewer.set_models(models)
        else:
            raise NotImplementedError(f"Behavior for next_viewer {self._next_viewer}")

    def get_asp(self):
        return self.editor.toPlainText()

    def toggle_multishot_mode(self):
        "change multishot mode and update"
        self.multishot_mode = not self.multishot_mode
        if hasattr(self._next_viewer, 'set_models'):  # update next one too
            self._next_viewer.multishot_mode = self.multishot_mode
        self.set_asp(self.get_asp())

    def highlight(self, line:int, char_beg:int, char_end:int, reason:str=''):
        "Highlight given position until change of ASP code"
        # print(f'HIGHTLIGHT TO BE PUT AT {line}:{char_beg}-{char_end}!')
        cursor = QTextCursor(self.editor.document())
        block = self.editor.document().findBlockByLineNumber(line-1)  # indexing starts at 0, but not for clingo
        cursor.setPosition(block.position() + char_beg - 1)  # indexing at 0, again
        cursor.movePosition(cursor.Right, cursor.KeepAnchor, char_end - char_beg)
        line_format = cursor.blockFormat()
        char_format = cursor.charFormat()
        line_format.setBackground(QBrush(ERR_LINE_COLOR))
        char_format.setBackground(QBrush(ERR_WORD_COLOR))
        char_format.setToolTip(reason)
        cursor.setBlockFormat(line_format)
        cursor.setCharFormat(char_format)

    def focus_line(self, lineno:int, char:int):
        "Move the cursor and the scroll in order to show given line and column. Also request the focus"
        # print(f'BLQT:ELD: focus at {lineno}:{char}')
        block = self.editor.document().findBlockByLineNumber(lineno)
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        cursor.setPosition(block.position() + char)
        self.editor.setTextCursor(cursor)
        self.editor.ensureCursorVisible()  # finally, scroll to show the cursor
        self.editor.setFocus()  # make it focus
