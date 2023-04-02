#TODO Add checking that file Exist
#TODO Add Colour's for different Categories and Adding new categories should add random colour
#TODO Saving file to some report type (Excell, PDF)
#TODO Refreshing table to show only not assigned item
#TODO detachs to other file section like (Layout, ... )

# Only needed for access to command line arguments
import sys
import os #for managing with path for category_list.txt

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QAction, QTableWidget, QVBoxLayout, QWidget, \
    QHBoxLayout, QTableWidgetItem, QFileDialog, QComboBox

#Depreceated in PyQt5
#from PyQt5.QtCore import QStringList, QString

#dot in this linkage mean that will use file from the same directory

from Program_Files.Data_Management.Pandas_table_management import *
from Category_List_Reading_And_Writing import *
from Percentage_expenditures_distribution_window_class import *


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.items_of_combobox = {} #its Dictionary storing value of each of specified spending group

        self.amount_of_money = 0 #temporary variable keeping value of maney selected in specified selection period

        self.setFixedWidth(1000)
        self.setFixedHeight(600)

        self.amount_to_add = -1

        self.click_amount = 0
        self.setWindowTitle("mBank Spended Monwy Alanyser")


        #I don't know why i use that
        self.setMouseTracking(True)

        #Adding Table
        self.Table = QTableWidget()
        self.Table.cellClicked.connect(self.Adding_values)


        # creating a push button
        self.button = QPushButton("CLICK", self)
        # adding action to a button
        self.button.clicked.connect(self.Button_is_clicked)
        self.first_action_subtraction = QAction("Subtract")
        # setting size of button
        self.button.resize(150, 50)

        #Button to load CSV
        self.button_Load_CSV = QPushButton("Load CSV data", self)
        # adding action to a button
        self.button_Load_CSV.clicked.connect(self.Fulfilling_table)
        self.first_action_subtraction = QAction("Subtract")

        #Button for Displaying Additional Windows with Data
        self.button_Values_display = QPushButton("Display Values", self)
        self.button_Values_display.clicked.connect(self.Open_Percentage_Distribution_Windows)

        self.combobox1 = QComboBox()





        # adding action to a button
        self.combobox1.currentIndexChanged.connect(self.Food_button_clicked)


        #LAYOUTS
        self.Horizontal_layout = QHBoxLayout()
        self.Horizontal_layout.addWidget(self.button)
        self.Horizontal_layout.addWidget(self.button_Load_CSV)
        self.Horizontal_layout.addWidget(self.button_Values_display)

        #https: // www.pythonguis.com / docs / qcombobox /

        #TODO Store item in file
        #self.combobox1.addItem('Food')
        #self.combobox1.addItem('Health')
        #self.combobox1.addItem('Car')
        #self.combobox1.addItem('Family')

        os.chdir("..")
        filename = str(f'{os.path.abspath(os.curdir)}' + "\\category_list.txt")
        self.Category_list = Catergory_List_Txt_to_Tuple(filename)

        for item in self.Category_list:
            print(item.name)
            self.combobox1.addItem(item.name)




        #TODO overwrite method of combobox AddItem to every time update self.items_of_combobox variable
        #Put to combobox_Constructor
        if len(self.items_of_combobox) != self.combobox1.count():
            print(self.combobox1.count())

            for i in range(self.combobox1.count()):
                self.items_of_combobox.update({self.combobox1.itemText(i):0})
                print(self.items_of_combobox)

        Vertical_Layout = QVBoxLayout()
        Vertical_Layout.addLayout(self.Horizontal_layout)
        Vertical_Layout.addWidget(self.combobox1)
        Vertical_Layout.addWidget(self.Table)

        widget = QWidget()
        widget.setLayout(Vertical_Layout)
        self.setCentralWidget(widget)
        #self.first_action_subtraction.toggled.connect(self.subtraction)

        #When you Press the QAction object listed in the context menu
        self.first_action_subtraction.triggered.connect(self.subtraction)

        #When you Go by mouse over the QAction object listed in the context menu
        #self.first_action_subtraction.hovered.connect(self.subtraction)

        #When you change something in properties of the QAction object
        #self.first_action_subtraction.changed.connect(self.subtraction)

        # CREATING SIGNAL
        # Communication between Windows
        # create signal and connect to slot
        # connect the sender window to the communicator
        self.progress_bar_communicator = ProgressBarCommunicator()
        #self.Category_list.valueChanged.connect(progress_bar_communicator.send_update_signal)


    def contextMenuEvent(self, e):
        self.context = QMenu(self)



        self.context.addAction(self.first_action_subtraction)
        self.context.addAction(QAction("Increment", self))
        self.context.addAction(QAction("test 3", self))
        self.context.exec(e.globalPos())


    def Button_is_clicked(self):
        self.click_amount += self.amount_to_add
        self.button.setText(str(self.click_amount))
        #print(self.button.clicked.par)

    def subtraction(self):
        self.amount_to_add *= -1
        print("Subtraction done")

    def Fulfilling_table(self):
        # Creating a DialogBox
        fileName = QFileDialog.getOpenFileName(self,
                                                    "Select Excell file",
                                                    "C:/Users/njvtwk/Downloads/lista_operacji_txt.csv",
                                                    "Excell Files (*.xmlx *.csv)")
        print(type(fileName))
        print(fileName[0])
        df = Load_data(fileName[0])
        #Adding column to Dataframe to mark already assigned rows
        df.insert(int(df.shape[1]), "Group of spending Labeled_mark", 0 ) #Initially fulfilled by NaN values
        #df = Load_data() #It's Basic version

        #Adding Table name





        # Row count
        self.Table.setRowCount(int(df.shape[0]))

        # Column count
        self.Table.setColumnCount(int(df.shape[1]))

        #Setting the Column names as in DataFrame
        print("Dataframe.columns type is")
        print(df.columns.tolist())

        self.Table.setHorizontalHeaderLabels(df.columns.tolist())

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                #print(df.iloc[i][j])
                self.Table.setItem(i , j, QTableWidgetItem(str(df.iloc[i, j])))



    def Adding_values(self):
        #print(self.amount_of_money)
        current_row = self.Table.currentRow()
        current_column = self.Table.currentColumn()

        cell_value = self.Table.item(current_row, current_column).text()

        #print(cell_value)
        #TODO we need to retun value of column where is Kwota
        print([i for i in range(self.Table.columnCount()) if self.Table.horizontalHeaderItem(i).text()])
        #print([i for i in range(self.Table.columnCount()) if self.Table.horizontalHeaderItem(i).text()].index('Kwota'))

        #Adding Horizontal table Value Was Crucial
        print(self.Table.horizontalHeaderItem(current_column).text())

        if self.Table.horizontalHeaderItem(current_column).text() == 'Kwota':
            print(self.Table.horizontalHeaderItem(current_column).text())
            self.Table.item(current_row, current_column).setBackground(QColor(255, 0, 0))

            self.Category_list[self.combobox1.currentIndex()].value += float(cell_value)

        self.progress_bar_communicator.send_update_signal(self.Category_list)


    def Food_button_clicked(self):
        print(self.Category_list[self.combobox1.currentIndex()].name)
        print(self.Category_list[self.combobox1.currentIndex()].value)

    # function  describing how to open new function
    def Open_Percentage_Distribution_Windows(self):
        print("Open_Percentage_Distribution_Windows runned")
        self.Percentage_Sistribution_Window = Percentage_Distribution_of_Expenditures(self)
        self.Percentage_Sistribution_Window.show()



"""
        09.03.2023 - Conception changed to usage file, so operations will be on 

        self.amount = 0 #Amount of money collected during this round
        #Key = self.combobox1.itemText(self.combobox1.currentIndex())
        if len(self.items_of_combobox) > 0:
            Key = list(self.items_of_combobox.keys())[self.combobox1.currentIndex()]

            print("Key for dictionary is equal: " + Key)
            #print("Type of self.items_of_combobox(Key) from Key given above: " + type(self.items_of_combobox[Key]) + "An have value" + self.items_of_combobox[Key])
            self.amount_of_money = self.items_of_combobox[Key]
            print(self.amount_of_money)

    #def loading_data_to_cells(self):
"""

#Slot and class for communicating
class ProgressBarCommunicator(QObject):
    progress_bar_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def send_update_signal(self, some_list):
        self.progress_bar_updated.emit(some_list)


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)




# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.

