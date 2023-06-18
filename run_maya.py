import sys
import logging

logger = logging.getLogger(__name__)
IS_PY2 = True if sys.version_info.major < 3 else False


def maya_qt5_main_window():
    '''
    Use with Qt5 or PySide2, with support for both Python 2 and 3.
    :rtype: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QMainWindow
    '''
    logger.info("Getting Maya main window")
    if IS_PY2:
        from maya.OpenMayaUI import MQtUtil
        from shiboken2 import wrapInstance
        from PySide2.QtWidgets import QWidget
        main_window_ptr = MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QWidget)  # type: ignore
    else:
        # `long` is obsolete and `int` doesn't work properly with `wrapInstance`
        from PySide2.QtWidgets import QApplication
        # get the QApplication instance if it exists
        app = QApplication.instance()

        if not app:
            app = QApplication(sys.argv)

        def maya_window():
            maya_win = next(w for w in app.topLevelWidgets()
                            if w.objectName() == 'MayaWindow')
            return maya_win

        return maya_window()

import sys
import logging

try:
    import maya.OpenMayaUI as omui
    from PySide2 import QtWidgets, QtCore
    import shiboken2
    MAYA = True
except ImportError:
    from PyQt5 import QtWidgets
    MAYA = False

class MyWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setWindowTitle("My Widget")

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        '''Create your widgets here'''
        self.label1 = QtWidgets.QLabel("Hello World 1")
        self.label2 = QtWidgets.QLabel("Hello World 2")

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItem("Item 1")
        self.list_widget.addItem("Item 2")
        self.list_widget.addItem("Item 3")

        self.button = QtWidgets.QPushButton("Execute")

    def create_layout(self):
        '''Create your layouts here'''
        main_layout = QtWidgets.QVBoxLayout(self)

        label_layout = QtWidgets.QHBoxLayout(self)
        label_layout.addWidget(self.label1)
        label_layout.addWidget(self.label2)

        main_layout.addLayout(label_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.button)

    def create_connections(self):
        '''Create your connections here'''
        self.button.clicked.connect(self.execute)

    def execute(self):
        print("TODO: Execute something here")
        pass

def main():
    if MAYA:
        widget = MyWidget(maya_qt5_main_window())
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        widget.show()
    else:
        # We are standalone, create a Qt application and window
        app = QtWidgets.QApplication(sys.argv)
        widget = MyWidget()
        widget.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()