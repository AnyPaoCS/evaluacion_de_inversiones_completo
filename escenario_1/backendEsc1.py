import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import plotly.graph_objects as go
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit ,QTableView, QDialog 
from PyQt5.QtCore import QAbstractTableModel, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import norm
from escenario_1.ventanaesc1 import *
from programa import *
from escenario_1.backendConclusion import *

class  VentanaEscenario1(QtWidgets.QMainWindow, Ui_ventanaEsc1 ):
    def __init__(self):
        super().__init__()
        #QAbstractTableModel.__init__(self)
        self.setupUi(self)
        self.boton_simular.clicked.connect(self.click_simular)
        self.pushButton_conclusion.clicked.connect(self.click_conclusion)
        self.boton_home.clicked.connect(self.volver_home)
        self.pushButton_histoTIR.clicked.connect(self.click_histrogramaTIR)
        self.pushButton_distAcuTIR.clicked.connect(self.click_distAcumTIR)
        self.pushButton_distNInvIni.clicked.connect(self.click_distNInvInicial)
        self.pushButton_distNFlujoNeto.clicked.connect(self.click_disNFlujos)
        self.pushButton_tablaS.clicked.connect(self.click_tablaS)
        
    def click_simular(self):
        media_flujo = int(self.media_flujo.text())
        desviacionE_flujo = int(self.desviacionE_flujo.text())
        media_inv = int(self.media_inv.text())
        desviacionE_inv = int(self.desviacionE_inv.text())
        global corridas
        corridas = int(self.lineEdit_Ncorridas.text())
        global trema
        trema = int(self.lineEdit_TREMA.text())

        global main 
        main= Inversion(media_flujo,desviacionE_flujo,media_inv,desviacionE_inv,corridas)
        global obj_inv
        obj_inv = Normal(media_inv,desviacionE_inv)
        global obj_flujosNetos
        obj_flujosNetos = Normal(media_flujo,desviacionE_flujo)
        global text_conclusion , text_conclusion2
        text_conclusion,text_conclusion2 = main.evaluar()
        self.mostrar_popup()
    def mostrar_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Mensaje")
        msg.setText("Se cargaron los datos correctamente")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
    def click_conclusion(self):
        try:
            
            self.ventanaEsc1_conclusion = VentanaConclusion()
            self.ventanaEsc1_conclusion.mostrar_conclusion(text_conclusion,text_conclusion2)
            self.ventanaEsc1_conclusion.pase_de_reportes(main,obj_inv,obj_flujosNetos)
            self.ventanaEsc1_conclusion.exec_()
        except Exception as inst:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No se puede mostrar la conclusion sin datos simulados")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            print(type(inst))
    
    def click_histrogramaTIR(self):
        try:
            main.graficar_histrogramaTIR()
            plt.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados para el Histograma TIR")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        
    def click_distAcumTIR(self):
        try:
            main.graficar_distAcumuladaTIR()
            plt.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados para la Distribucion Acumulada")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        
    def click_distNInvInicial(self):
        try:
            obj_inv.grafica_distnormal_Inv()
            plt.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados para la Inversion Inicial")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        
    def click_disNFlujos(self):
        try:
            obj_flujosNetos.grafica_distnormal_Flujo()
            plt.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados para los Flujos Netos")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        
    def click_tablaS(self):
        try:
            self.model = pandasModel(tabla)
            self.view = QTableView()
            self.view.setModel(self.model)
            corridas_str = str(corridas)
            print(corridas_str)
            titulo = "Tabla: Resultado de simular "+ corridas_str + " corridas"
            print(titulo)
            self.view.setWindowTitle(titulo)
            self.view.resize(700, 600)
            self.view.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados para la tabla")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
      
    def volver_home(self):
       self.close()

         
class Distribucion:
    def __init__(self):
        self.res =0
        

class Normal(Distribucion):
    def __init__(self, media, desviacion_e,cantidad_valor =0):
        Distribucion.__init__(self)
        self.media = media
        self.desviacion_e = desviacion_e
        self.cantidad_valor = cantidad_valor


    def generar_resultado(self):
        res = np.random.normal(self.media, self.desviacion_e,self.cantidad_valor)
        return res
    
    def grafica_distnormal_Inv(self):
        x_1 = np.linspace(norm(self.media, self.desviacion_e).ppf(0.01),
                  norm(self.media, self.desviacion_e).ppf(0.99), 1000)
        FDP_normal = norm(self.media, self.desviacion_e).pdf(x_1) # FDP
        print("FDP: " ,type(FDP_normal))
        plt.figure(4)
        plt.plot(x_1, FDP_normal, label='FDP nomal')
        plt.title('Función de Densidad de Probabilidad')
        plt.ylabel('probabilidad')
        plt.xlabel('valores')
        plt.text(self.media, np.mean(FDP_normal.tolist()), 'La gráfica muestra el comportamiento de \n la distribución normal para la inversion inicial' ,
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')
        print('show: graficas' , plt)
        plt.savefig("./escenario_1/imagen4.jpg")
    def grafica_distnormal_Flujo(self):
        normal = norm(self.media, self.desviacion_e)
        x = np.linspace(normal.ppf(0.01),
                        normal.ppf(0.99), 1000)
        fp = normal.pdf(x) # Función de Probabilidad
        plt.figure(3)
        plt.plot(x, fp)
        plt.title('Distribución Normal')
        plt.ylabel('probabilidad')
        plt.xlabel('valores')
        plt.text(self.media,  np.mean(fp.tolist()), 'La gráfica muestra el comportamiento de \n la distribución normal para el flujo neto ' ,
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')
        plt.savefig("./escenario_1/imagen3.jpg")
class Inversion():

    def __init__(self,media_flujo,desviacionE_flujo,media_inv,desviacionE_inv,corridas):
        self.tir = 0
        self.media_flujo =media_flujo
        self.desviacionE_flujo = desviacionE_flujo
        self.media_inv = media_inv
        self.desviacionE_inv = desviacionE_inv
        self.corridas = corridas
        self.data = pd.DataFrame()
    def evaluar(self):
        global tabla 
        tabla= self.construir_dataFrame()
        conclusion, conclusion2 = self.probabilidad()
        return conclusion,conclusion2
    def calcular_tir(self):
        objt_inv= Normal(self.media_inv,self.desviacionE_inv,1)
        objt_flujos = Normal(self.media_flujo,self.desviacionE_flujo,5)
        inversion =objt_inv.generar_resultado()
        flujos_netos = objt_flujos.generar_resultado()
        aux_tir = np.rint(np.insert(flujos_netos,0,-inversion))
        tir = round((np.irr(aux_tir)*100), 3)
        corrida = np.append(aux_tir, tir, axis=None)
        return corrida
    def construir_dataFrame(self):
        data = pd.DataFrame(columns=['inversión_inicial', 'ingresos_año1', 'ingresos_año2','ingresos_año3', 'ingresos_año4','ingresos_año5', 'TIR'], index=range(self.corridas))
        #row = Inversion()
        for i in data.index :
            data.iloc[i] = self.calcular_tir()
        print("funciona!!!")
        print(data)
        data.sort_values(by=['TIR'], inplace=True)
        data.to_excel(r'./escenario_1/export_dataframe.xlsx', index = False)
        return data
   
    def graficar_histrogramaTIR(self):
        #datos
        #tabla.sort_values(by=['TIR'], inplace=True)
        tir_data = tabla['TIR']
        array = tir_data.to_numpy()
        fragmentos = np.around(np.linspace(array[0], array[-1], 21), 3 )
        bins = fragmentos.tolist()
        #grafico con solucion 1
        plt.figure(1)
        plt.hist(array, bins = bins, orientation='vertical')
        plt.title('Histograma TIR')
        plt.xlabel('valores del TIR')
        plt.ylabel('Total repeticiones')
        string_corridas= str(corridas)
        plt.text(array[-1]-array[0]*2, (corridas/ 10), 'La gráfica muestra el comportamiento de TIR \n tras simular ' + string_corridas + ' veces ' ,
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')
        plt.savefig("./escenario_1/imagen1.jpg")
    def graficar_distAcumuladaTIR(self):
        tabla.sort_values(by=['TIR'], inplace=True)
        tir_data = tabla['TIR']
        array = tir_data.to_numpy()
        tir_acu = pd.DataFrame(columns= ['limite inf','limite sup', 'fracción', 'fracción acumulada'], index= range(20))
        freq = (array[-1] - array[0])/20               # Amplitud de los intervalos
        inf = array.min()        # Limite inferior del primer intervalo
        dif = (array.min() - array.max()) % freq or freq
        sup = array.max() + dif  # Limite superior del último intervalo

        intervals = pd.interval_range(
            start=inf,
            end=sup,
            freq=freq,
            closed="left"
            )
        tir_acu = pd.DataFrame(index= intervals)

        tir_acu["fracción"] = round((pd.cut(array, bins= intervals).value_counts())/(self.corridas),3)
        tir_acu["fracción acumulada"] = tir_acu["fracción"].cumsum()
        a = np.arange(tir_acu.shape[0])
        plt.figure(2)
        plt.plot(tir_acu.index.mid, tir_acu['fracción acumulada'])
        plt.title('Frecuencia acumulada TIR')
        plt.xlabel('valores del TIR')
        plt.ylabel('Frecuencia acumulada')
        string_corridas= str(corridas)
        plt.text(array[-1]-array[0]*2, 0.5, 'La gráfica muestra el comportamiento de \nla distribución acumulada de la TIR \n tras simular  ' + string_corridas + ' veces ' ,
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')
        plt.savefig("./escenario_1/imagen2.jpg")

    def probabilidad(self):
        p_tir = tabla['TIR'].to_numpy()
        may_trema = p_tir[p_tir > trema]
        print(may_trema)
        porcentaje = len(may_trema) * 100 / corridas
        str_procentaje = str(porcentaje)
        print(porcentaje)
        if porcentaje >= 90:
            res = 'Los parametros indican que la inversión puede ser aceptada,  cumpliendo con los criterios de aceptación Prob [TIR > TREMA] > 90%. Siendo esta probabilidad = ' + str_procentaje + '%'
            res2 = 'Los parametros indican que la inversión puede ser aceptada\n,  cumpliendo con los criterios de aceptación Prob [TIR > TREMA] > 90%. \nSiendo esta probabilidad = ' + str_procentaje + '%'
        else:

            res = 'Los parametros indican que la inversión debe ser rechazada, NO cumpliendo con los criterios de aceptación Prob [TIR > TREMA] > 90%. Siendo esta probabilidad = ' + str_procentaje + '%'
            res2 = 'Los parametros indican que la inversión debe ser rechazada\n, NO cumpliendo con los criterios de aceptación Prob [TIR > TREMA] > 90%.\n Siendo esta probabilidad = ' + str_procentaje + '%'
        return res,res2

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

       
if __name__ == "__main__":

    app= QtWidgets.QApplication([])
    ventana_esc1= VentanaEscenario1()
    ventana_esc1.show()
    
    app.exec_()
    