import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import plotly.graph_objects as go
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit ,QTableView, QDialog, QMessageBox
#from PyQt5.Qtcore import QAbstractTableModel , Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import norm
from programa import *
from escenario_2.conclusion import *
from escenario_2.Reportes2 import *
from escenario_2.convertidor2 import *
class  VentanaConclusion(QtWidgets.QDialog, Ui_Conclusion ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_descargarReporte.clicked.connect(self.click_DescargarInformeFinal)
        self.pushButton_descargarGraficos.clicked.connect(self.click_graficos)
        self.pushButton_descargarTabla.clicked.connect(self.click_tabla)
        self.obj_reportes=Reportes2()
        self.obj_convertidor=Convertidor2()
        self.pushButton_atras.clicked.connect(self.atras)
        self.conclusion = ""
        self.conclusion2 = ""
    def click_graficos(self):
        self.obj_reportes.reporteGraficosDescarga()
    def click_tabla(self):
        self.obj_convertidor.tablaPdfDescarga()
    def click_DescargarInformeFinal(self):
        print("Entro al boton")
        self.obj_reportes.crearCaratula()
        self.obj_convertidor.tablaPdf()
        self.obj_reportes.reporteGraficos(self.conclusion2)
        self.obj_reportes.reporteFinal()
       
    
    def mostrar_conclusion(self, conclusion,conclusion2):
        self.conclusion = conclusion
        self.conclusion2 = conclusion2
        self.textBrowser.setText(conclusion)
    def pase_de_reportes(self,main,obj_inv,obj_res,obj_inf,obj_flujos):
        main.graficar_histrogramaVPN()
        plt.close()
        obj_inv.grafica_distTriangular_Inv()
        plt.close()
        obj_res.grafica_distTriangular_Res()
        plt.close()
        obj_inf.grafica_distTriangular_Inf()
        plt.close()
        obj_flujos.grafica_distUniforme()
        plt.close()
        print('imprime reporte final')
        
    def atras(self):
        
        self.close()
    
    
if __name__ == "__main__":

    app= QtWidgets.QApplication([])
    ventana_conclusion = VentanaConclusion()
    ventana_conclusion.show()
    
    app.exec_()