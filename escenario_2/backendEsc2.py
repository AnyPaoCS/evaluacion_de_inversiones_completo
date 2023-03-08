import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import plotly.graph_objects as go
from pylab import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit ,QTableView, QDialog, QMessageBox
from PyQt5.QtCore import QAbstractTableModel, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import norm
from escenario_2.ventanaesc2 import *
from programa import *
from escenario_2.backendConclusion2 import *
class  VentanaEscenario2(QtWidgets.QMainWindow, Ui_Escenario2 ):
    def __init__(self):
        super().__init__()
        #QAbstractTableModel.__init__(self)
        self.setupUi(self)
        self.pushButton_home.clicked.connect(self.volver_home)

        self.pushButton_simular.clicked.connect(self.click_simular)
        self.pushButton_coclusion.clicked.connect(self.click_conclusion)
        self.pushButton_vpn.clicked.connect(self.click_histrogramaVPN)
        self.pushButton_inv.clicked.connect(self.click_inversionInicial)
        self.pushButton_res.clicked.connect(self.click_valorRescate)
        self.pushButton_inf.clicked.connect(self.click_tasaInflacion)
        self.pushButton_neto.clicked.connect(self.click_flujoNeto)
        self.pushButton_tabla.clicked.connect(self.click_tablaS)
        self.pushButton_tabla2.clicked.connect(self.click_tablaS2)
     

        
    def click_simular(self):
        #inversion inicial
        inv_min = int(self.lineEdit_min_inv.text())
        inv_esp = int(self.lineEdit_esp_inv.text())
        inv_max = int(self.lineEdit_max_inv.text())
        #Valor de rescate
        res_min = int(self.lineEdit_min_res.text())
        res_esp = int(self.lineEdit_esp_res.text())
        res_max = int(self.lineEdit_max_res.text())
        #Inflacion
        inf_min = int(self.lineEdit_min_inf.text())
        inf_esp = int(self.lineEdit_esp_inf.text())
        inf_max = int(self.lineEdit_max_inf.text())
        #corridas
        global corridas
        corridas = int(self.lineEdit_corridas.text())
        #flujo neto
        flujo1 = int(self.lineEdit_1_neto.text()) 
        flujo2 = int(self.lineEdit_2_neto.text()) 
        flujo3 = int(self.lineEdit_3_neto.text()) 
        flujo4 = int(self.lineEdit_4_neto.text()) 
        flujo5 = int(self.lineEdit_5_neto.text())
        #tasa de descuento
        global t_descuento
        t_descuento = int(self.lineEdit_tasadescuento.text())
        #llamada a las distribuciones triangulares
        global obj_inv
        obj_inv = Triangular(inv_min,inv_esp,inv_max)
        global obj_res
        obj_res = Triangular(res_min,res_esp,res_max)
        global obj_inf
        obj_inf = Triangular(inf_min,inf_esp,inf_max)
        #llamada a las distribucion uniforme
        global obj_flujos
        obj_flujos = Uniforme(flujo1,flujo2,flujo3,flujo4,flujo5)

        global main 
        main = Inversion()
        global text_conclusion , text_conclusion2
        text_conclusion, text_conclusion2 = main.evaluar()
        self.mostrar_popup()
    def click_conclusion(self):
        try:
            self.ventanaEsc2_conclusion = VentanaConclusion()
            self.ventanaEsc2_conclusion.mostrar_conclusion(text_conclusion , text_conclusion2)
            self.ventanaEsc2_conclusion.pase_de_reportes(main,obj_inv,obj_res,obj_inf,obj_flujos)
            self.ventanaEsc2_conclusion.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No se puede mostrar la conclusion sin datos simulados")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
    def mostrar_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Mensaje")
        msg.setText("Se cargaron los datos correctamente")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
    def click_histrogramaVPN(self):
        try:
            main.graficar_histrogramaVPN()
            plt.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados para el Histograma VPN")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
    def click_inversionInicial(self):
       try:
            obj_inv.grafica_distTriangular_Inv()
            fig2.show()
       except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados de Inversion Inicial")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
            print("error",e)
    def click_valorRescate(self):
        try:
            obj_res.grafica_distTriangular_Res()
            fig3.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados del Valor de Rescate")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        
    def click_tasaInflacion(self):
        try:
            obj_inf.grafica_distTriangular_Inf()
            fig4.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados de la Tasa de inflacion")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        
    def click_flujoNeto(self):
        try:
            obj_flujos.grafica_distUniforme()
            plt.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No existen datos simulados de los Flujos Netos")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
  

       
    def volver_home(self):
       #cerrar ventana 
       self.close()
    def click_tablaS(self):
        #ventana emergente con tabla de los datos DATAFRAME corridas
        try:
            
            
            self.model = pandasModel(flujo_grafica)
            self.view = QTableView()
            self.view.setModel(self.model)
            corridas_str = str(corridas)
            titulo = "Tabla: Resultado de simular "+ corridas_str + " corridas"
            self.view.setWindowTitle(titulo)
            self.view.resize(1000, 600)
            self.view.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No se puede mostrar la tabla sin datos simulados")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()
        
    def click_tablaS2(self):
        #ventana emergente con tabla de los datos DATAFRAME corridas
        try:
            flujo_data = dataCorridas.iloc[:,[1,2,3,4,5,8]]
            flujo_data['año_5']= flujo_data['año_5'] - flujo_data['valor_de_rescate']
            flujo_data = flujo_data.iloc[:,[0,1,2,3,4]]
            print(flujo_data)
            flujo_data = flujo_data * 100 / 40
            self.model = pandasModel(flujo_data)
            self.view = QTableView()
            self.view.setModel(self.model)
            titulo = "Tabla: Resultado flujo neto antes de impuestos"
            self.view.setWindowTitle(titulo)
            self.view.resize(1000, 600)
            self.view.show()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Mensaje")
            msg.setText("No se puede mostrar la tabla sin datos simulados")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

    
class Distribucion:
    def __init__(self):
        self.res =0
        
#Clase distribucion triangular
class Triangular(Distribucion):
    def __init__(self, minimo, esperado,maximo):
        Distribucion.__init__(self)
        self.minimo = minimo
        self.esperado = esperado
        self.maximo = maximo
    #resultado para inversion inicial y de rescate
    def generar_resultado(self):
        res = np.around(np.random.triangular(self.minimo, self.esperado, self.maximo, 1), 0) # Meter datos Estimacion pesimista - probable - optimista
        res = res.astype(int)
        return res
    #resultado para inflacion
    def generar_resInf(self):
        #INFLACION
        inflacion = 100 - (np.around(np.random.triangular(100 - self.minimo, 100 - self.esperado, 100 - self.maximo, 1), 0)) #Meter datos Estimacion pesimista - probable - optimista
        return inflacion
    def grafica_distTriangular_Inv(self):
        global fig2
        fig2 = plt.figure(2)
        ax1 = fig2.add_subplot(211)
        ax2 = fig2.add_subplot(212)
        matplotlib.style.use('seaborn')
        fig2.suptitle('Distribución Triangular')
        x = np.array([self.minimo, self.esperado ,self.maximo])
        y = np.array([0, 2/(self.maximo - self.minimo) ,0])
        str_minimo = 'a = ' + str(x[0]) + ', ' + str(y[0])
        str_esperado = 'c = ' + str(x[1]) + ', ' + str(y[1])
        str_maximo = 'b = ' + str(x[2]) + ', ' + str(y[2])
        ax1.plot(x[0],y[0],'r.', ms = 15, label = str_minimo)
        ax1.plot(x[1],y[1],'b.', ms = 15, label = str_esperado)
        ax1.plot(x[2],y[2],'g.', ms = 15, label = str_maximo)
        fig2.legend(title = 'Distribución triangular')
        ax1.triplot(x,y)
        ax1.text((self.maximo-self.minimo)/2  + self.minimo, y[1]/3, 'La gráfica esta dada por una distribución triangular, mostrando \n los datos del histograma en la parte inferior la misma \n figura generada por los datos de dicha distribución \n'+ str(str_minimo) +',  '+str(str_esperado) +',  '+ str(str_maximo),
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')

        #grafico con solucion 1
        flujo_data = dataCorridas.iloc[:,[8]]
        array = flujo_data.to_numpy()
        ax2.hist(array, bins = 50, orientation='vertical')
        print("mostrar grafica distri")
        plt.savefig("./escenario_2/imagen2.jpg")
     
    def grafica_distTriangular_Res(self):
        global fig3
        fig3 = plt.figure(3)
        ax1 = fig3.add_subplot(211)
        ax2 = fig3.add_subplot(212)
        matplotlib.style.use('seaborn')
        fig3.suptitle('Distribución Triangular')
        x = np.array([self.minimo, self.esperado ,self.maximo])
        y = np.array([0, 2/(self.maximo - self.minimo) ,0])
        str_minimo = 'a = ' + str(x[0]) + ', ' + str(y[0])
        str_esperado = 'c = ' + str(x[1]) + ', ' + str(y[1])
        str_maximo = 'b = ' + str(x[2]) + ', ' + str(y[2])
        ax1.plot(x[0],y[0],'r.', ms = 15, label = str_minimo)
        ax1.plot(x[1],y[1],'b.', ms = 15, label = str_esperado)
        ax1.plot(x[2],y[2],'g.', ms = 15, label = str_maximo)
        fig3.legend(title = 'Distribución triangular')
        ax1.triplot(x,y)
        ax1.text((self.maximo-self.minimo)/2  + self.minimo, y[1]/3, 'La gráfica esta dada por una distribución triangular, mostrando \n los datos del histograma en la parte inferior la misma \n figura generada por los datos de dicha distribución \n'+ str(str_minimo) +',  '+str(str_esperado) +',  '+ str(str_maximo),
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')
        flujo_data = dataCorridas.iloc[:,[8]]
        array = flujo_data.to_numpy()
        ax2.hist(array, bins = 50, orientation='vertical')
        print("mostrar grafica distri")
        plt.savefig("./escenario_2/imagen3.jpg")
    def grafica_distTriangular_Inf(self):
        global fig4
        fig4 = plt.figure(4)
        ax1 = fig4.add_subplot(211)
        ax2 = fig4.add_subplot(212)
        matplotlib.style.use('seaborn')
        fig4.suptitle('Distribución Triangular')
        x = np.array([self.maximo, self.esperado ,self.minimo])
        y = np.array([0, 2/(self.minimo - self.maximo) ,0])
        str_minimo = 'a = ' + str(x[0]) + ', ' + str(y[0])
        str_esperado = 'c = ' + str(x[1]) + ', ' + str(y[1])
        str_maximo = 'b = ' + str(x[2]) + ', ' + str(y[2])
        ax1.plot(x[0],y[0],'r.', ms = 15, label = str_minimo)
        ax1.plot(x[1],y[1],'b.', ms = 15, label = str_esperado)
        ax1.plot(x[2],y[2],'g.', ms = 15, label = str_maximo)
        fig4.legend(title = 'Distribución triangular')
        ax1.triplot(x,y)
        ax1.text((self.maximo-self.minimo)/2  + self.minimo, y[1]/3, 'La gráfica esta dada por una distribución triangular, mostrando \n los datos del histograma en la parte inferior la misma \n figura generada por los datos de dicha distribución \n'+ str(str_minimo) +',  '+str(str_esperado) +',  '+ str(str_maximo),
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')
        flujo_data = dataCorridas.iloc[:,[8]]
        array = flujo_data.to_numpy()
        ax2.hist(array, bins = 50, orientation='vertical')
        
        
        print("mostrar grafica distri")
        plt.savefig("./escenario_2/imagen4.jpg")
    
class Uniforme(Distribucion):
    def __init__(self, flujo1, flujo2,flujo3,flujo4,flujo5):
        Distribucion.__init__(self)
        self.flujo1 = flujo1
        self.flujo2 = flujo2
        self.flujo3 = flujo3
        self.flujo4 = flujo4
        self.flujo5 = flujo5
    def generar_resultado(self):
        #INDICES
        indices = np.random.uniform(0,1,5) * 5
        indices = indices.astype(int)
        #FLUJO
        flujo = [self.flujo1, self.flujo2, self.flujo3, self.flujo4, self.flujo5] #Meter los valores que tendra nuestro flujo
        #NUEVO FLUJO SEGUN INDICES (ARREGLO NUEVO)
        flujoNuevo = np.take(flujo,(indices))
        return flujoNuevo
    def grafica_distUniforme(self):
        #datos
        flujo_data = dataCorridas.iloc[:,[1,2,3,4,5,8]]
        array = np.concatenate( (flujo_data['año_1'].to_numpy(), flujo_data['año_2'].to_numpy(), flujo_data['año_3'].to_numpy(), flujo_data['año_4'].to_numpy(), (flujo_data['año_5'].to_numpy()-flujo_data['valor_de_rescate'].to_numpy())), axis = None)
        #grafico con solucion 1
        plt.figure(5)
        plt.hist(array, bins = 5, orientation='vertical')
        plt.title('Histograma Flujo Neto')
        plt.xlabel('valores del Flujo Neto')
        plt.ylabel('Total repeticiones')
        plt.text(40000, 50, 'La gráfica muestra la evolución del flujo \n neto dado por una distribución uniforme',
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')

        plt.savefig("./escenario_2/imagen5.jpg")
class Inversion():

    def __init__(self):
        pass
    
    def evaluar(self):
        global dataCorridas 
        dataCorridas = self.construir_dataFrame()
        global flujo_grafica
        flujo_grafica = dataCorridas.iloc[:,[0,1,2,3,4,5,6,7]]
        flujo_grafica.to_excel(r'./escenario_2/export_dataframe.xlsx', index = False)
        
        conclusion,conclusion2 = self.probabilidad()
        return conclusion, conclusion2
    def calcular_VPN(self, descuento, arregloFinal):
        return np.npv(descuento,arregloFinal)
    def arreglo(self):
        inv = obj_inv.generar_resultado()
        flujo = obj_flujos.generar_resultado()
        rescate = obj_res.generar_resultado()
        inflacion = obj_inf.generar_resInf()/100
        descuento = np.around(t_descuento/100 + inflacion+(t_descuento/100 * inflacion), 8)
        flujo[4] = np.take(flujo,4) + rescate
        arregloFinal = np.concatenate((inv,flujo),axis=0)
        vpn =  self.calcular_VPN(descuento,arregloFinal)
        res = np.concatenate((arregloFinal, vpn, inflacion, rescate, descuento), axis = None)
        return res    
    def construir_dataFrame(self):
        #construye un dataframe de tamaño n difinido por --> range(n)
        data = pd.DataFrame(columns=  ['inv_ini', 'año_1', 'año_2', 'año_3', 'año_4', 'año_5', 'VPN', 'inflacion', 'valor_de_rescate', 'tasa_de_descuento'], index = range(corridas))
        for i in data.index :
            data.iloc[i] = self.arreglo()
        
        return data
    def graficar_histrogramaVPN(self):
      # HISTOGRAMA VPN , cambie el nombre corridas por datacorridas
        vpn_data = dataCorridas['VPN']
        np_vpn_data = vpn_data.to_numpy()
        plt.figure(1)
        plt.hist(np_vpn_data, bins = 20, orientation='vertical')
        plt.title('Histograma VPN')
        plt.xlabel('valores del VPN')
        plt.ylabel('Total repeticiones')
        string_corridas= str(corridas)
        plt.text(0, 60, 'La gráfica muestra el comportamiento del VPN \n tras simular ' + string_corridas + ' veces ' ,
        bbox={'facecolor': 'white', 'alpha': 2, 'pad': 5}, ha='center')
        plt.savefig("./escenario_2/imagen1.jpg")
    def probabilidad(self):
        p_vpn = dataCorridas['VPN'].to_numpy()
        may_01 = p_vpn[p_vpn > 0.1]
        print(may_01)
        porcentaje = len(may_01) * 100 / corridas
        str_procentaje = str(porcentaje)
        print(porcentaje)
        if porcentaje >= 90:
            res = 'Los parametros indican que la inversión puede ser aceptada, cumpliendo con los criterios de aceptación Prob[VPN > 0.1] > 90 %. Siendo esta probabilidad = '+ str_procentaje + '%'
            res2 = 'Los parametros indican que la inversión puede ser aceptada, cumpliendo \n con los criterios de aceptación Prob[VPN > 0.1] > 90 %. \n Siendo esta probabilidad = '+ str_procentaje + '%'
        else:
            res = 'Los parametros indican que la inversión debe ser rechazada, NO cumpliendo con los criterios de aceptación Prob[VPN > 0.1] > 90 %. Siendo esta probabilidad = '+ str_procentaje + '%'
            res2 = 'Los parametros indican que la inversión debe ser rechazada, NO cumpliendo \n con los criterios de aceptación Prob[VPN > 0.1] > 90 %.\n Siendo esta probabilidad = '+ str_procentaje + '%'
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
    ventana_esc2 = VentanaEscenario2()
    ventana_esc2.show()
    
    app.exec_()