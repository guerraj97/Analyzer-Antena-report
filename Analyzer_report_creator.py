#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 11:23:11 2021

Version 0.0.0 - Inicio del archivo.
Version 0.1.0 - Pruebas para la generacion de un documento PDF y agregar imagenes.
30/05/2021 Version 0.2.0 - Cambios en la GUI para pedir valores iniciales para calculos.
06/06/2021 Version 0.3.0 - Arreglos a la GUI para el inicio de los calculos y generacion del reporte PDF
                           Se agrega un checkbox para calcular la envolvente o no. Ademas, un textbox para
                           colocar la ruta de los datos que se van a utilizar. Bloqueo de interfaz inicial 
                           mediante el boton de INICIO.
24/08/2021 Version 0.3.1 - Se agregan identificadores a la GUI para nombrar archivos y figuras. Solamente 
                           se agregan los textboxes, aun no esta implementado para su funcionamiento.
                           Pendiente: que estas variables y textos sirvan para identificar archivos.

@author: joseguerra
"""


n = 35 #para el boton1 de capturar
n2 = 300 #para el boton3 del codigo
n3 = 35

from Analyzer import analyzer_generator #libreria swarm para la deteccion de la pose de agentes

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QApplication, QWidget, QPushButton,QLineEdit, QCheckBox, QVBoxLayout
import sys
from PySide2.QtGui import QImage, QPixmap



filename = '/Users/joseguerra/Desktop/Libro1.csv'




class Window(QWidget):
    #global q
    #new_thread = 0
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Reportes - RSI (2021)")
        self.parametros_iniciales()
        
        self.setGeometry(370,210,650,600)
        #self.setIcon()
        self.image_frame = QLabel()
        self.createCheckBox()
        
        self.capturar_button()

        self.Calculos_EL()
        self.biniciar_calculos.setEnabled(False)
        
        self.parametros_iniciales()
        
        #cajas de texto para datos conocidos
        self.texto_degree_EL.setEnabled(False)
        self.texto_degree_AZ.setEnabled(False)
        self.EL_PEAK.setEnabled(False)
        self.filename_.setEnabled(False)
        self.texto_antena_gain.setEnabled(False)
        
        self.diametro_antena.setEnabled(False)
        self.pad_id.setEnabled(False)
        self.banda_.setEnabled(False)
        

        
        #Muestra el titulo de la imagen en la GUI
        self.label_img_text = QLabel(self)
        self.label_img_text.move(80,250)
        self.label_img_text.setText("IDENTIFICADORES")
        self.label_img_text.setFixedWidth(125)
        self.label_img_text.show()
        
        #Para mostrar la imagen en la GUI
        self.label_img = QLabel(self)
        #self.label_img.setText()
        self.label_img.setGeometry(320, 220,450, 300)
        self.label_img.move(70,220)
        self.label_img.show()
        #self.mostrar_imagen.addWidget(self.image_frame)
        #self.setLayout(self.mostrar_imagen)
        
        #Etiquetas para ordenar la GUI
        
        #Para mostrar etiqueta de calibracion
        self.label_calib = QLabel(self)
        self.label_calib.move(n+60,50-20)
        self.label_calib.setText("Calibracion*")
        self.label_calib.setFixedWidth(125)
        self.label_calib.show()
        
        #Para mostrar etiqueta de generar codigo/marcador/identificador
        self.label_code = QLabel(self)
        self.label_code.move(n+280,50-20)
        self.label_code.setText("Ruta del archivo de datos")
        self.label_code.setFixedWidth(200)
        self.label_code.show()
        
        #Para mostrar etiqueta de obtencion de pose
        self.label_Pose = QLabel(self)
        self.label_Pose.move(n3+10,105)
        self.label_Pose.setText("Parametros iniciales para los calculos**")
        self.label_Pose.setFixedWidth(265)
        self.label_Pose.show()
        
        #Para mostrar etiqueta de notas
        self.label_note1 = QLabel(self)
        self.label_note1.move(n3-5,540)
        self.label_note1.setText("NOTA 1(*): Calibrar hasta ver las 4 esquinas del tablero (Presionar Reiniciar Calibracion)")
        self.label_note1.setFixedWidth(600)
        self.label_note1.show()
        
        #Para mostrar etiqueta de notas
        self.label_note2 = QLabel(self)
        self.label_note2.move(n3-5,560)
        self.label_note2.setText("NOTA 2(**): Mejores resultados se obtienen con ilumacion directa sobre la mesa")
        self.label_note2.setFixedWidth(600)
        self.label_note2.show()


    def capturar_button(self):
        self.bcapturar = QPushButton("INICIO", self)
        self.bcapturar.move(n,50)
        self.bcapturar.clicked.connect(self.capturar)
        
    
    def Calculos_EL(self):
        self.biniciar_calculos = QPushButton("Iniciar Calculos", self)
        self.biniciar_calculos.move(n3,120)

        self.biniciar_calculos.clicked.connect(self.pose)
        
        
    def pose(self):
        self.file_name = self.filename_.text()
        print(self.file_name)
        
        analyzer = analyzer_generator(self.file_name)
        EL_angle_txt = self.texto_degree_EL.text()
        EL_angle = float(EL_angle_txt)

        Antena_gain_txt = self.texto_antena_gain.text()
        if self.envelope == 0:
            Antena_gain_txt = 0
        _antena_gain = float(Antena_gain_txt)        
        
        AZ_angle_txt = self.texto_degree_AZ.text()
        AZ_angle = float(AZ_angle_txt)
        
        EL_PEAK_txt = self.EL_PEAK.text()
        _EL_PEAK = float(EL_PEAK_txt)
        
        AZ = analyzer.data_calculation_AZ(AZ_angle, _antena_gain, _EL_PEAK, self.envelope,_chart_title_ = "AZChart",_filename_ = "AZ_Chart")
        EL = analyzer.data_calculation_EL(EL_angle, _antena_gain, self.envelope,_chart_title_ = "ELChart",_filename_ = "EL_Chart")
        analyzer.gain_calculation()
        
        analyzer.report_generator("AZ_Chart.png", "EL_Chart.png",AZ,EL)
        
        # analyzer.data_calculation_AZ(-1.16,0,30.5,0,_chart_title_,_filename_)
        # analyzer.data_calculation_EL(-1,0,0,_chart_title_,_filename2_)
        # analyzer.gain_calculation()
        
        
        # EL = analyzer.data_calculation_EL(-12, antena_gain, 1, _chart_title_, _filename_)
        # AZ = analyzer.data_calculation_AZ(-13.15,antena_gain,30.5,1,_chart_title2_,_filename2_)
        
        # EL, fig = analyzer.data_calculation_EL(EL_angle, _antena_gain,self.envelope)
        # AZ = analyzer.data_calculation_AZ(AZ_angle, _antena_gain, _EL_PEAK,self.envelope)
        # analyzer.report_generator("AZChart.png", "ELChart.png",AZ,EL)
        #self.set_label_image(fig, "prueba")
    
        
    def parametros_iniciales(self):
        
        #para agregar las cajas de los datos 
        
        self.texto_degree_EL = QLineEdit(self,placeholderText="Degree EL")
        self.texto_degree_AZ = QLineEdit(self,placeholderText="Degree AZ")
        self.EL_PEAK = QLineEdit(self,placeholderText="EL PEAK")
        self.texto_antena_gain = QLineEdit(self,placeholderText="Antena Gain2")
        
        self.diametro_antena = QLineEdit(self,placeholderText="DIAMETRO ANTENA")
        self.pad_id = QLineEdit(self,placeholderText="PAD-ID")
        self.banda_ = QLineEdit(self,placeholderText="BAND")
        
        self.filename_ = QLineEdit(self,placeholderText="FILE NAME")
        
        self.filename_.setFixedWidth(400)
        self.filename_.move(n+200,50)
        
        self.EL_PEAK.setFixedWidth(125)
        self.EL_PEAK.move(n3+135,183)
        
        #para ajustar la posicion en la GUI
        self.texto_degree_EL.setFixedWidth(125)
        self.texto_degree_EL.move(n3+135,123)
   
        self.texto_degree_AZ.setFixedWidth(125)
        self.texto_degree_AZ.move(n3+135,153)
        
        self.texto_antena_gain.setFixedWidth(125)
        self.texto_antena_gain.move(n3+275,123)
        
        #PARA IDENTIFICACION DE LOS ARCHIVOS 
        #self.diametro_antena.setEnabled(False)
        self.diametro_antena.move(n3+60, 270)
        self.diametro_antena.setFixedWidth(155)
        #self.pad_id.setEnabled(False)
        self.pad_id.move(n3+60, 300)
        #self.banda_.setEnabled(False)
        self.banda_.move(n3+60, 335)
        
        
    def set_label_image(self, snap, text):
        self.image = snap
        height, width, channels = self.image.shape
        bytesPerLine = channels * width
        self.image_show = QImage(self.image.data, width, height,bytesPerLine, QImage.Format_RGB888)
        self.image = QPixmap.fromImage(self.image_show)
        self.pixmap_resized = self.image.scaled(self.label_img.width(), self.label_img.height(), Qt.KeepAspectRatio)
        self.label_img.setPixmap(self.pixmap_resized)
        self.label_img_text.setText(text)
        
        
    def capturar(self):
        self.biniciar_calculos.setEnabled(True)
        
        self.EL_PEAK.setEnabled(True)
        self.texto_antena_gain.setEnabled(True)
        
        self.texto_degree_EL.setEnabled(True)
        self.texto_degree_AZ.setEnabled(True)
        self.filename_.setEnabled(True)
        
        self.diametro_antena.setEnabled(True)
        self.pad_id.setEnabled(True)
        self.banda_.setEnabled(True)
        

    def createCheckBox(self):
        
        self.label = QLabel("", self)
        self.label.move(n3+100, 208)
        self.label.setFixedWidth(200)
        
        check = QCheckBox("envolvente", self)
        check.stateChanged.connect(self.checkBoxChange)
        check.move(n3+5,205)
        
        vbox = QVBoxLayout()

        
        check.toggle()
        vbox.addWidget(check)
        vbox.addWidget(self.label)
        
        #self.setLayout(vbox)
 
 
 
    def checkBoxChange(self, state):
        if state == Qt.Checked:
            self.envelope = 1
            self.label.setText("ACTIVADO")
            self.texto_antena_gain.setEnabled(True)
 
        else:
            self.envelope = 0
            self.label.setText("DESACTIVADO")
            self.texto_antena_gain.setEnabled(False)
        
        

            
myapp = QApplication.instance()
if myapp is None: 
    myapp = QApplication(sys.argv)
#myapp = QApplication(sys.argv)
window = Window()
window.show() 

sys.exit(myapp.exec_())

myapp.quit()

