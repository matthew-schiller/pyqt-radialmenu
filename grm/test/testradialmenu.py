try:
    from Qt import QtWidgets, QtCore, QtGui
    print('radial_menu: Using Qt.py')
except:
    from PySide2 import QtWidgets, QtCore, QtGui
    print('radial_menu: Using PySide2')
import sys
from functools import partial
from grm.radialmenu import RadialMenu, RadialMenuAction, RadialMenuItem


class TestWindow(QtWidgets.QMainWindow):
    """
    QMainWindow class for testing radial menus when added
    to widgets

    Exec this file to run test
    """

    def __init__(self):
        super(TestWindow, self).__init__()

        ########################################################
        # Build a list widget
        ########################################################
        self.setWindowTitle('Test Radial Menu')
        self.resize(700, 500)

        self.centralWidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        self.label = QtWidgets.QLabel()
        self.label.setText('Click in widget below')
        self.verticalLayout.addWidget(self.label)

        self.targetList = QtWidgets.QListWidget(self.centralWidget)
        self.targetList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        for item_name in ['A', 'B', 'C', 'D']:
            item = QtWidgets.QListWidgetItem(self.targetList)
            item.setText('Test Item {}'.format(item_name))

        self.verticalLayout.addWidget(self.targetList)
        self.setCentralWidget(self.centralWidget)


def build_menu():
    """
    Builds an example menu with items populated.
    :return: Radial Menu Object
    """
    items = {'N': 'North',
             'S': 'South',
             'E': 'East',
             # 'W': 'West',
             'NE': 'NorthEast',
             'NW': 'NorthWest',
             'SE': 'SouthEast',
             'SW': 'SouthWest'}

    radial_menu = RadialMenu()
    item_widgets = list()
    for pos in items:
        item = RadialMenuItem(position=pos)
        item.setText(items[pos])
        radial_menu.add_item(item)
        item_widgets.append(item)
        item.connect(partial(temp_print, pos, item))

    # Make some items checkable
    item_widgets[0].setCheckable(True)
    item_widgets[1].setCheckable(True)

    # Build menu
    item = RadialMenuItem(position='W')
    item.setText('WESTSIDE!')
    radial_menu.add_item(item)

    # Test column menu
    item = RadialMenuItem(position=None)
    item.setText('I am in a column')
    radial_menu.add_item(item)

    column_widgets = list()
    for itemText in ['itemA', 'itemB', 'itemC', 'itemD', 'itemF']:
        item = RadialMenuItem(position=None)
        item.setText(itemText)
        item.connect(partial(temp_print, itemText, item))
        radial_menu.add_item(item)
        column_widgets.append(item)
    column_widgets[3].setCheckable(True)

    return radial_menu


def temp_print(print_stuff, widget):
    print(print_stuff)
    if widget.checkBox:
        widget.checkBox.setChecked(not(widget.checkBox.checkState()))


def testMousePress():
    active_window = QtWidgets.QApplication.activeWindow()
    if active_window:
        window = TestWindow()
        menu = build_menu()
        window.setParent(active_window)

        menu.left_click_connect(window.targetList)

        window.setWindowFlags(QtCore.Qt.Window)

        window.show()
    if not active_window:
        app = QtWidgets.QApplication(sys.argv)
        window = TestWindow()
        menu = build_menu()

        menu.left_click_connect(window.targetList)

        window.setParent(active_window)
        window.show()
        sys.exit(app.exec_())

def testMouseFilter():
    active_window = QtWidgets.QApplication.activeWindow()
    if active_window:
        window = TestWindow()
        menu = build_menu()
        window.setParent(active_window)

        menu.start()

        window.setWindowFlags(QtCore.Qt.Window)

        window.show()
    if not active_window:
        app = QtWidgets.QApplication(sys.argv)
        window = TestWindow()
        menu = build_menu()

        menu.start()

        window.setParent(active_window)
        window.show()
        sys.exit(app.exec_())

def testActions():
    active_window = QtWidgets.QApplication.activeWindow()
    if active_window:
        window = TestWindow()
        menu = build_menu()
        window.setParent(active_window)

        window.targetList.customContextMenuRequested.connect(menu.popup)

        window.setWindowFlags(QtCore.Qt.Window)

        window.show()
    if not active_window:
        app = QtWidgets.QApplication(sys.argv)
        window = TestWindow()
        #menu = build_menu()
        menu = RadialMenuAction()
        a = menu.addAction('stuff')
        a = menu.addAction('okay')
        mn = menu.addMenu('sub')
        a = menu.addAction('okay2')
        a.setCheckable(True)
        a.setChecked(True)
        a = menu.addAction('                               ')
        mn.addAction('sub stuff')

        # menu.popup(QtGui.QCursor.pos())
        #window.targetList.customContextMenuRequested.connect(menu.popup)
        #window.targetList.mousePressEvent = partial(menu.popup(QtGui.QCursor.pos()))
        window.targetList.mousePressEvent = menu.pressMe

        window.setParent(active_window)
        window.show()
        sys.exit(app.exec_())

def testActionsRadial():
    active_window = QtWidgets.QApplication.activeWindow()
    if not active_window:
        app = QtWidgets.QApplication(sys.argv)
        window = TestWindow()

        # Radial
        items = {'N': 'North',
                 'S': 'South',
                 'E': 'East',
                 # 'W': 'West',
                 'NE': 'NorthEast',
                 'NW': 'NorthWest',
                 'SE': 'SouthEast',
                 'SW': 'SouthWest'}

        radial_menu = RadialMenu()
        item_widgets = list()
        for pos in items:
            item = RadialMenuItem(position=pos)
            item.setText(items[pos])
            radial_menu.add_item(item)
            item_widgets.append(item)
            item.connect(partial(temp_print, pos, item))

        # Column
        column_menu = RadialMenuAction()
        column_menu.setParent(radial_menu)
        a = column_menu.addAction('stuff')
        a = column_menu.addAction('okay')
        mn = column_menu.addMenu('sub')
        a = column_menu.addAction('okay2')
        a.setCheckable(True)
        a.setChecked(True)
        a = column_menu.addAction('                               ')
        mn.addAction('sub stuff')


        pos = QtGui.QCursor.pos()
        column_menu.popup(pos)
        column_menu.menu_rect = QtCore.QRect(pos.x()-150, pos.y()+20, column_menu.width(), column_menu.height()-40)
        column_menu.setGeometry(column_menu.menu_rect)

        # menu.popup(QtGui.QCursor.pos())
        #window.targetList.customContextMenuRequested.connect(menu.popup)
        #window.targetList.mousePressEvent = partial(menu.popup(QtGui.QCursor.pos()))
        #window.targetList.mousePressEvent = column_menu.pressMe

        radial_menu.left_click_connect(window.targetList)

        window.setParent(active_window)
        window.show()
        sys.exit(app.exec_())

#testMouseFilter()
