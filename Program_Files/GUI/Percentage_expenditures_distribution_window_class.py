
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QVBoxLayout




class Percentage_Distribution_of_Expenditures(QWidget):
    def __init__(self, Main_Window_Data):
        super().__init__()
        print("CLASS Open_Percentage_Distribution_Windows runned")
        self.setFixedWidth(1000)
        self.setFixedHeight(600)
        self.List_of_Bars = Main_Window_Data.Category_list #Category_List have to be
        # connect the sender window to the communicator
        Main_Window_Data.progress_bar_communicator.progress_bar_updated.connect(self.GiveMeSign)
        print(type(self.List_of_Bars[0]))



        self.initUI()

    def initUI(self):

        Height_of_single_progressbar = 25
        self.label = QLabel(self)
        self.label.setText("Percentage distribution of expenditure")

        #TODO this varaibel is to replace by intem from Mian_Window Object staright from reference


        self.list_of_QProgressBar = []
        self.list_of_Labels_as_QLabel = []
        vbox = QVBoxLayout()

        for i in range(len(self.List_of_Bars)):
            self.list_of_QProgressBar.append(QProgressBar(self))
            #print(self.List_of_Bars[i].name)
            self.list_of_Labels_as_QLabel.append(QLabel())
            self.list_of_Labels_as_QLabel[i].setText(self.List_of_Bars[i].name)
            vbox.addWidget(self.list_of_Labels_as_QLabel[i])
            self.list_of_QProgressBar[i].setGeometry(0, 0 + (Height_of_single_progressbar + 5 ) * i, 300, Height_of_single_progressbar)
            self.list_of_QProgressBar[i].setMinimum(0)
            self.list_of_QProgressBar[i].setMaximum(100)
            vbox.addWidget(self.list_of_QProgressBar[i])
        self.setLayout(vbox)
    
    """
    This method is called in momnet when receive signal from Main Winodow that some value is changed. 
    """
    def GiveMeSign(self):
        Biggest_value_Value = 0.0
        for i in range(len(self.List_of_Bars)):
            Biggest_value_Value = self.List_of_Bars[i].value if self.List_of_Bars[i].value > Biggest_value_Value else Biggest_value_Value
        for i in range(len(self.List_of_Bars)):
            self.list_of_QProgressBar[i].setValue(int(self.List_of_Bars[i].value/Biggest_value_Value*100))
        #print("HELLO YOUR SIGNAL IS WORKING !!!")