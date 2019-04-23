import sys
from functools import partial
from PySide2 import QtWidgets
from radialMenu import RadialMenu, RadialMenuItem


class TestRadialMenuWindow(QtWidgets.QMainWindow):
    """
    QMainWindow class for testing radial menus when added
    to widgets

    Exec this file to run test
    """

    def __init__(self):
        super(TestRadialMenuWindow, self).__init__()

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
        for item_name in ['A', 'B', 'C', 'D']:
            item = QtWidgets.QListWidgetItem(self.targetList)
            item.setText('Test Item {}'.format(item_name))

        self.verticalLayout.addWidget(self.targetList)
        self.setCentralWidget(self.centralWidget)

        ########################################################
        # Add Radial Menu
        ########################################################
        items = {'N': 'North',
                 'S': 'South',
                 'E': 'East',
                 # 'W': 'West',
                 'NE': 'NorthEast',
                 'NW': 'NorthWest',
                 'SE': 'SouthEast',
                 'SW': 'SouthWest'}

        self.radial_menu = RadialMenu()
        item_widgets = list()
        for pos in items:
            item = RadialMenuItem(position=pos)
            item.setText(items[pos])
            self.radial_menu.add_item(item)
            item_widgets.append(item)
            item.connect(partial(self.temp_print, pos, item))
        # Make some items checkable
        item_widgets[0].setCheckable(True)
        item_widgets[1].setCheckable(True)

        # Build menu
        item = RadialMenuItem(position='W')
        item.setText('WESTSIDE!')
        self.radial_menu.add_item(item)

        # Use right click
        # self.pieQMenu.rightClickConnect(ui.targetList)
        # Use left click
        self.radial_menu.left_click_connect(self.targetList)

        # Test column menu
        item = RadialMenuItem(position=None)
        item.setText('I am in a column')
        self.radial_menu.add_item(item)

        for itemText in ['itemA', 'itemB', 'itemC', 'itemD', 'itemF']:
            item = RadialMenuItem(position=None)
            item.setText(itemText)
            item.connect(partial(self.temp_print, itemText, item))
            self.radial_menu.add_item(item)

    @staticmethod
    def temp_print(print_stuff, widget):
        print(print_stuff)
        if widget.checkBox:
            widget.checkBox.setChecked(not(widget.checkBox.checkState()))


app = QtWidgets.QApplication(sys.argv)
window = TestRadialMenuWindow()
window.show()
sys.exit(app.exec_())




