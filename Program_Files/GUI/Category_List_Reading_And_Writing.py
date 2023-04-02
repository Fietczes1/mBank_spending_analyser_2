import random

from PyQt5.QtGui import QColor


class Category:
     def __init__(self, name, value):
         self.name = name
         self.value = float(value)
         self.colour = QColor(0, 0, 0)

     #This function shoud, show swhat colour shoudld have specified category
     def colour_drawing(self):
         self.colour = QColor(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
     #TODO add Color For Colouring the selected Item

     #That's method what's is responisble for showing object during
     def __repr__(self):
         return f"Category(name='{self.name}', value={self.value})"

def Catergory_List_Txt_to_Tuple(filename):

    Category_list = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            Category_list.append(Category(line.rstrip(), 0.0)) #method rstrip probably take from right side of text new line character# and this is declaration of

    return Category_list
