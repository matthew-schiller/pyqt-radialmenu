try:
    from Qt import QtWidgets, QtCore
    print('radial_menu: Using Qt.py')
except:
    from PySide2 import QtWidgets, QtCore
    print('radial_menu: Using PySide2')
import sys
from functools import partial
from grm.radialmenu import RadialMenu, RadialMenuItem


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


def test():
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
        #window.targetList.customContextMenuRequested.connect(menu.popup)
        window.setParent(active_window)
        window.show()
        sys.exit(app.exec_())


test()

