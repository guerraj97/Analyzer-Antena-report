#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 11:23:11 2021

Version 0.0.0 - Inicio del archivo.
Version 0.0.1 - Pruebas para la generacion de un documento PDF y agregar imagenes.
30/05/2021 Version 0.0.2 - Cambios en la GUI para pedir valores iniciales para calculos.

@author: joseguerra
"""

# from reportlab.pdfgen.canvas import Canvas
# from reportlab.lib.units import inch, cm
# from reportlab.lib.pagesizes import LETTER

# import matplotlib.pyplot as plt

# fig = plt.figure(figsize=(4, 3))
# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')

# fig.savefig("prueba")

# canvas = Canvas("font-example.pdf", pagesize=LETTER)
# canvas.setFont("Times-Roman", 18)
# canvas.drawString(1 * inch, 10 * inch, "Times New Roman (18 pt)")
# canvas.save()

# image_on_canvas.py

n = 35 #para el boton1 de capturar
n2 = 300 #para el boton3 del codigo
n3 = 35

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QApplication, QWidget, QPushButton,QLineEdit
import sys
from PySide2.QtGui import QImage, QPixmap


# def add_image(image_path):
#     img = utils.ImageReader(image_path)
#     img_width, img_height = img.getSize()
#     aspect = img_height / float(img_width)

#     my_canvas = canvas.Canvas("canvas_image.pdf",
#                               pagesize=letter)
#     my_canvas.saveState()
#     #my_canvas.rotate(45)
#     my_canvas.drawImage(image_path, 150, 10,
#                         width=100, height=(100 * aspect))
#     my_canvas.restoreState()
#     my_canvas.save()

# if __name__ == '__main__':
#     image_path = 'prueba.png'
#     add_image(image_path)


class Window(QWidget):
    #global q
    #new_thread = 0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Reportes - RSI (2021)")
        self.setGeometry(370,210,650,600)
        #self.setIcon()
        self.image_frame = QLabel()
        self.capturar_button()
        self.Reiniciar_calibracion()
        #self.detener_procesamiento_button()
        self.Num_ID()
        self.ingresar_codigo()
        self.codigo_button()
        self.new_thread = 0
        self.Toma_pose()
        self.biniciar_calculos.setEnabled(False)
        self.size_codigo.setEnabled(False)
        
        self.parametros_iniciales()
        
        #cajas de texto para datos conocidos
        self.texto_degree_start.setEnabled(False)
        self.texto_degree_stop.setEnabled(False)
        
        #self.detener.setEnabled(False)
        #self.mostrar_imagen = QLabel()
        
        #Muestra el titulo de la imagen en la GUI
        self.label_img_text = QLabel(self)
        self.label_img_text.move(220,220)
        self.label_img_text.setText("Visualizar Imagen")
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
        self.label_code.setText("Generacion Identificador")
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
        self.bcapturar = QPushButton("Calibrar", self)
        self.bcapturar.move(n,50)
        self.bcapturar.clicked.connect(self.capturar)
    
    def Reiniciar_calibracion(self):
        self.bre_calib = QPushButton("Reiniciar calibracion", self)
        self.bre_calib.move(n+90,50)
        self.bre_calib.clicked.connect(self.Calibracion_reinit)
    
        
    def codigo_button(self):
        self.btn3 = QPushButton("Generar Codigo", self)
        self.btn3.move(n2,50)
        self.btn3.clicked.connect(self.codigo)
        
    
    def Toma_pose(self):
        self.biniciar_calculos = QPushButton("Iniciar Calculos", self)
        self.biniciar_calculos.move(n3,120)
        #self.Init_pose()
        self.biniciar_calculos.clicked.connect(self.pose)
        
    def detener_procesamiento_button(self):
        self.detener = QPushButton("Detener Procesamiento", self)
        self.detener.move(n3,150)
        self.detener.clicked.connect(self.detener_procesamiento)
    
    def Calibracion_reinit(self):
        self.bcapturar.setEnabled(True)
        self.biniciar_calculos.setEnabled(False)
        self.size_codigo.setEnabled(False)
        
        
    def pose(self):
        global gray_blur_img, canny_img, snapshot_robot, resized, Final_Crop_rotated
        text = self.size_codigo.text()
        if text == '':
            text = '3'
        numCod = int(text)
        #read_lock.acquire()
        #start_time = time.time()
        #foto = camara.get_frame("SINGLE")
        #snapshot_robot,MyWiHe = vector_robot.calibrar_imagen(foto)
        #q.put(snapshot_robot)
        #read_lock.release()
        self.set_label_image(snapshot_robot,"Robots a identificar")
        #cv.imshow("CapturaPoseRobot", snapshot_robot)
        
        #cv.waitKey(0)
        #time.sleep(1)
  
        """   
        if resized == [] or Final_Crop_rotated ==[]:
            pass
        else:
            #gray_blur_img
            cv.imshow("gray_blur_img",gray_blur_img)
            cv.imshow("resized",resized)
            cv.imshow("Final_Crop_rotated", Final_Crop_rotated)
            cv.imshow("canny_img",canny_img)
            cv.waitKey(0)
        """
        #cv.waitKey(100)
        #cv.imshow("canny_img", canny_img)
        #cv.waitKey(0)
        #cv.imshow("Imagen blur", gray_blur_img)
        #cv.waitKey(0)
        
        #procesar.join()
        #obtener_pose.join()
        #actualizar = threading.Thread(target = read_2)
        
        """
        #Version sin hilos
        #Snapshot = cv.imread("opencv_CalibSnapshot_0.png")
        RecCod, gray_blur_img, canny_img = getRobot_Code(snapshot_robot, MyGlobalCannyInf, MyGlobalCannySup, numCod)
        parameters = getRobot_fromSnapshot(RecCod,gray_blur_img,numCod)
        
        size = len(parameters)
        for i in range (0, size):
            temp_param = parameters[i]
            if vector_robot.update_robot_byID(temp_param[0], temp_param[1], temp_param[2]):
                pass
            else:
                vector = vector_robot.agregar_robot(Robot(temp_param[0],temp_param[1],temp_param[2]))
        print("Este es el vector retornado: ",vector[0].id_robot)
        print("Este es el vector retornado: ",vector[1].id_robot)
        """
    
    def Num_ID(self):
        self.lineEdit = QLineEdit(self,placeholderText="Ingrese número")
        self.lineEdit.setFixedWidth(120)
        self.lineEdit.move(n2+140,55)
        #vbox = QVBoxLayout(self)
        #vbox.addWidget(self.lineEdit)
    
    def ingresar_codigo(self):
        self.size_codigo = QLineEdit(self,placeholderText="Tamaño del código")
        self.size_codigo.setFixedWidth(125)
        self.size_codigo.move(n3+120,303)
        #vbox = QVBoxLayout(self)
        #vbox.addWidget(self.lineEdit)
        
    def parametros_iniciales(self):
        
        #para agregar las cajas de los datos 
        
        self.texto_degree_start = QLineEdit(self,placeholderText="Degree start")
        self.texto_degree_stop = QLineEdit(self,placeholderText="Degree stop")

        
        #para ajustar la posicion en la GUI
        self.texto_degree_start.setFixedWidth(125)
        self.texto_degree_start.move(n3+135,123)
        
        self.texto_degree_stop.setFixedWidth(125)
        self.texto_degree_stop.move(n3+135,153)
        

        
    # def detener_procesamiento(self):
    #     global flag_detener
    #     flag_detener = True
    #     self.procesar.join()
    #     self.obtener_pose.join()
    #     self.vector_update.join()
    #     self.new_thread = 0
    #     flag_detener = False
    #     self.detener.setEnabled(False)
        
    def codigo(self):
        text = self.lineEdit.text()
        if text == '':
            text = '0'
        num = int(text)
        #camara.Generar_codigo(num)
        
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
        #foto = camara.get_frame()
        #CaliSnapshot = camara.Calibrar(foto,Calib_param,Treshold)
        #self.set_label_image(CaliSnapshot, "Imagen Calibrada")
        #self.label_img.show()
        #self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888).rgbSwapped()
        #self.image_frame.setPixmap(QPixmap.fromImage(self.image))

        #cv.imshow("Output Image", CaliSnapshot)
        #cv.waitKey(2000)
        #camara.destroy_window()
        self.biniciar_calculos.setEnabled(True)
        self.size_codigo.setEnabled(True)
        self.bcapturar.setEnabled(False)
        

            
myapp = QApplication.instance()
if myapp is None: 
    myapp = QApplication(sys.argv)
#myapp = QApplication(sys.argv)
window = Window()
window.show() 

sys.exit(myapp.exec_())

myapp.quit()