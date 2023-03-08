from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from PyPDF2 import PdfFileMerger
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit ,QTableView, QFileDialog,QWidget,QMessageBox
import os
class Reportes2(QWidget):
    
    def __init__(self):
        super().__init__()
       
    def crearCaratula(self):
        c = canvas.Canvas("./escenario_2/Report/Reportes/"+'Reporte1.pdf')
        c.setFont('Helvetica', 20)
        c.drawString(140,760,"Universidad Mayor de San Simón")
        c.setFont('Helvetica-Oblique', 20)
        c.drawString(140,740,"Facultad de Ciencias y Tecnología")
        c.setFont('Helvetica-Oblique', 40)
        c.drawString(90,450,"Reporte de la Simulacion")
        c.setFont('Helvetica-Oblique', 40)
        c.drawString(180,420,"de Inversiones")
        c.drawImage('./escenario_2/logo1.jpg', 30, 650, 100, 150)
        c.drawImage('./escenario_2/logo2.jpg', 460, 700, 100, 100)
        c.showPage()
        c.save()
    def reporteGraficosDescarga(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        try:
            fileName, _ = QFileDialog.getSaveFileName(self,"Guardar Graficos..","ReporteGraficos.pdf","All Files (*);;Text Files (*.pdf)", options=options)
        
            # abrimos el pdf 
            c = canvas.Canvas(fileName)
            #Fuente y el tamaño = ?
            c.setFont('Helvetica-Oblique', 50)
            # Dibujamos texto: (X,Y,Texto)
            c.drawString(225,450,"Graficos")
            c.showPage()
            c.setFont('Helvetica', 30)
            # Dibujamos texto: (X,Y,Texto)
            c.drawString(125,760,"Grafico del Histograma VPN")
            # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
            c.drawImage('./escenario_2/imagen1.jpg', 10, 175, 600, 500)
            c.showPage()
            #//
            c.setFont('Helvetica', 30)
            c.drawString(110,760,"Grafico de la Inversion Inicial")
            c.drawImage('./escenario_2/imagen2.jpg', 10, 175, 600, 500)
            c.showPage()
            #//
            c.setFont('Helvetica', 30)
            c.drawString(125,760,"Grafico del Valor de Rescate")
            c.drawImage('./escenario_2/imagen3.jpg', 10, 175, 600, 500)
            c.showPage()
            #//
            c.setFont('Helvetica', 30)
            c.drawString(150,760,"Grafico de la Inflacion")
            c.drawImage('./escenario_2/imagen4.jpg', 10, 175, 600, 500)
            c.showPage()
            #//
            c.setFont('Helvetica', 30)
            c.drawString(160,760,"Grafico del Flujo Neto")
            c.drawImage('./escenario_2/imagen5.jpg', 10, 175, 600, 500)
            c.showPage()
            c.save()
            self.mostrar_popup()
        except Exception as e:
            print("se cancelo ")
    def reporteGraficos(self,conclusion):
        # abrimos el pdf 
        c = canvas.Canvas("./escenario_2/Report/Reportes/"+'Reporte3.pdf')
        #Fuente y el tamaño = ?
        c.setFont('Helvetica-Oblique', 50)
        # Dibujamos texto: (X,Y,Texto)
        c.drawString(225,450,"Graficos")
        c.showPage()
        c.setFont('Helvetica', 30)
        # Dibujamos texto: (X,Y,Texto)
        c.drawString(125,760,"Grafico del Histograma VPN")
        # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
        c.drawImage('./escenario_2/imagen1.jpg', 10, 175, 600, 500)
        c.showPage()
        #//
        c.setFont('Helvetica', 30)
        c.drawString(110,760,"Grafico de la Inversion Inicial")
        c.drawImage('./escenario_2/imagen2.jpg', 10, 175, 600, 500)
        c.showPage()
        #//
        c.setFont('Helvetica', 30)
        c.drawString(125,760,"Grafico del Valor de Rescate")
        c.drawImage('./escenario_2/imagen3.jpg', 10, 175, 600, 500)
        c.showPage()
        #//
        c.setFont('Helvetica', 30)
        c.drawString(150,760,"Grafico de la Inflacion")
        c.drawImage('./escenario_2/imagen4.jpg', 10, 175, 600, 500)
        c.showPage()
        #//
        c.setFont('Helvetica', 30)
        c.drawString(160,760,"Grafico del Flujo Neto")
        c.drawImage('./escenario_2/imagen5.jpg', 10, 175, 600, 500)
        c.showPage()
        #Conclusion
        c.setFont('Helvetica-Oblique', 50)
        c.drawString(200,450,"Conclusion")
        c.showPage()
        #Mensaje
        #my_text = "Los resultados de esta simulacion para la inversion de este negocio da a concluir \nque el proyecto es rentable para llevarlo a cabo ya que se muestra en los graficos\nque se logra un valor de ingresos aceptables."
        my_text = conclusion
        textobject = c.beginText(2*cm, 29.7 * cm - 2 * cm)
        for line in my_text.splitlines(False):
            textobject.textLine(line.rstrip())
        c.drawText(textobject)
        c.save()
    def reporteFinal(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        try:
            fileName, _ = QFileDialog.getSaveFileName(self,"Guardar Reporte Final..","ReporteFinal.pdf","All Files (*);;Text Files (*.pdf)", options=options)
        
            loc = "./escenario_2/Report/Reportes/"
            pdfs = [loc+archivo for archivo in os.listdir(loc) if archivo.endswith(".pdf")]
            #nombre_archivo_salida = "ReporteFinal.pdf"
            fusionador = PdfFileMerger()
            for pdf in pdfs:
                fusionador.append(open(pdf, 'rb'))

            with open(fileName, 'wb') as salida:
                fusionador.write(salida)
            self.mostrar_popup()
        except Exception as e:
            print("se cancelo ")
    def mostrar_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Mensaje")
        msg.setText("Se creo el reporte correctamente")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()