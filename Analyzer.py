#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 30 18:31:55 2021

Version 0.0.0 - Inicio del archivo.
30/05/2021 Version 0.1.0 - Creacion de las primeras clases para los calculos de los reportes.
                           Encuentra los maximos en los datos y los minimos en la diferencia, esto 
                           # sirve para poder realizar los calculos para el ploteo.
05/06/2021 Version 0.2.0 - Encuentra el minimo y maximo necesario para ciertos calculos. Grafica la figura 
                           con datos de elevacion y su respectiva grafica envolvente. Version preeliminar
                           de un documento PDF con una tabla que resume los datos y muestra la grafica
                           generada. 
05/06/2021 Version 0.3.0 - Generacion completa de un archivo PDF con graficas y tablas para AZ y EL.
06/06/2021 Version 0.3.1 - Mejoras menores al reporte PDF. Se arregal el calcular la envolvente mediante
                           una variable de control para que el usuario decida si quiere o no tener este dato.
13/06/2021 Version 0.4.0 - Se agrega el calculo de la ganacia.
13/06/2021 Version 0.4.1 - Mejoras a la busqueda de datos para calcular la ganancia. Se agregan nuevas variables
                           en las funciones de AZ y EL calculation, para nombrar las figuras y los titulos a gusto
                           del usuario. 
24/08/2021 Version 0.4.2 - Arreglos menores al codigo. Codigo de debugin comentado. 
                           Pendiente: Mejorar PDF.
                           
27/08/2021 Version 0.5.0 - Arreglos para la generacion de la tabla de datos. Ahora si se calcula la envolvente
                           se muestra una tabla diferente al calculo de la ganancia. Se agregan variables de control
                           para verificar la envolvente y otro tipo de identificadores segun lo necesitado.  

18/09/2021 Version 0.5.1 - Arreglos a la tabla de datos para una mejor visualizacion. 

29/11/2021 Version 0.5.2 - Arreglos al codigo para mostrar si paso la ganancia.  

@author: joseguerra
"""


#Librerias para la creacion de un reporte PDF

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, PageBreak

from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import utils
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
#from PIL import Image

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from datetime import datetime, timedelta
  
  


CONST_DB_M_10 = -10
CONST_DB_M_10_UP = -9.9
CONST_DB_M_10_DOWN = -10.1

CONST_DB_M_3 = -3
CONST_DB_M_3_UP = -2.9
CONST_DB_M_3_DOWN = -3.1
HEIGHT_TITLE = 680
IMAGE_HEIGTH = HEIGHT_TITLE-120

filename = '/Users/joseguerra/Desktop/GAIN_2DEG_PAD_B.csv'
#filename = '/Users/joseguerra/Desktop/GAIN_2DEG_PAD_B.csv'
#filename = '/Users/joseguerra/Desktop/AZ_GAIN_2_DEG.csv' #DATOS ANTERIORES PARA EL PAD B


def figure_generator(angle_step, difference, envelope,_filename, chart_title,_envelope_state):
        '''
    

    Parameters
    ----------
    angle_step : TYPE float
        El step de la variacion del angulo del barrido para las pruebas.
    difference : TYPE Numpy Array
        Contiene la diferencia calculada para generacion del grafico
    envelope : TYPE Numpy Array
        Contiene los datos para la envolvente
    _filename : TYPE String
        Nombre del archivo a guardar. Por default lo guarda como un PNG
    chart_title : TYPE String
        Titulo del grafico, puede cambiar.

    Returns
    -------
    None.

    '''
        fig = plt.figure(figsize=(8,4)) #tama;o de la figura
        plt.plot(angle_step,difference) #ploteo de la data
        
        plt.title(chart_title)#agrega titulo
        
        if _envelope_state == 0:
            pass
        else:
            plt.plot(angle_step,envelope,"-r") #ploteo de la envolvente
            
        #plt.ylabel('some numbers')#axis name
        fig.savefig(_filename) #guarda la figura para su uso posterior en el reporte PDF
        print("save figure")
        return fig
        
def report_template_table(angle,max_data,min_value,step_size,antena_gain,EL_PEAK,AZ_pos,overshoot,envelope):
        '''
    

    Parameters
    ----------
    angle : TYPE Float
            Angulo de inicio para el barrido
    max_data : TYPE Float
            Maximo encontrado
    min_value : TYPE Float
            Minimo encontrado
    step_size : TYPE Float
            Step calculado para el barrido.
    antena_gain : TYPE Float
            Ganancia de la antena
    EL_PEAK : TYPE Float
            Posicion inicial de la antena o pico en elevacion
    AZ_pos : TYPE Float
            Posicion inicial en la antena o pico en Azimuth
    overshoot : TYPE Int
            Cantidad de valores que estan por arriba del envelope (solo mostrado si se pide la grafica de envolvente)
    envelope : TYPE Int
            1 o 0, para mostrar la tabla de envelope o solamente los datos para gain

    Returns
    -------
        t : TYPE tableStyle
            Contiene una estructura de datos con toda la informacion para la generacion de la tabla 
            en el documento PDF

    '''
        s = getSampleStyleSheet()

        if envelope == 0:
        
            data = [
    
            ["Parameter", "Value"],
            ["Azimuth", str(AZ_pos)+" Deg PEAK"],
            ["Elevation", str(EL_PEAK)+" Deg PEAK"],
            ["Antenna Gain (REAL)",str(antena_gain)+" dBi"],
            ["Start of Pattern", str(angle)+"° Deg"],
            ["Stop of Pattern", str(-angle)+"° Deg"],
            ["MAX", str(round(max_data,2))+" dBm"],
            ["MIN", str(round(min_value,2))+" dBm"],
            ["Step Size", str(round(step_size,4))+"° Deg"],
            ]
            
        else:
            data = [
    
            ["Parameter", "Value"],
            ["Azimuth", str(AZ_pos)+" Deg PEAK"],
            ["Elevation", str(EL_PEAK)+" Deg PEAK"],
            ["Antenna Gain (REAL)",str(antena_gain)+" dBi"],
            ["Start of Pattern", str(angle)+"° Deg"],
            ["Stop of Pattern", str(-angle)+"° Deg"],
            ["MAX", str(round(max_data,2))+" dBm"],
            ["MIN", str(round(min_value,2))+" dBm"],
            ["Step Size", str(round(step_size,4))+"° Deg"],
            ["Overshoot", str(overshoot)],
            ["Overshoot ratio", str(round(overshoot/1001*100,4))+"%"],
            ]
            
   
        #paragraph_1 = Paragraph("PREELIMINAR TEMPLATE REPORT", s['Heading1'])
        # elements.append(paragraph_1)
        # elements.append(Image(_filename))
        
        #TODO: Get this line right instead of just copying it from the docs
        style = TableStyle([('ALIGN',(0,0),(1,0),'CENTER'),
                               ('VALIGN',(0,0),(0,-1),'TOP'),
                               ('TEXTCOLOR',(0,0),(0,10),colors.blue),
                               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                               ('TEXTCOLOR',(0,0),(1,0),colors.green),
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ])
        
        #Configure style and word wrap
        
        t=Table(data)
        t.setStyle(style)
        return t
    
class analyzer_generator():

    
    def __init__(self,filename):
        '''
        

        Parameters
        ----------
        filename : TYPE String
            Nombre del archivo donde esta la informacion de AZ y EL

        Returns
        -------
        None.

        '''
        self.antena_gain_real = 0
        self.df = pd.read_csv(filename, error_bad_lines=False)
        #El archivo debe guardarse como un CSV (ver fomato adjunto en la informacion de este proyecto)
        #El separador es un ';' ya que, por como se guardan los datos, Python reconoce esto como el separador
        #de informacion. 
        
        self.max_index = self.df.shape[0] #Encuentra el indice maximo de los datos dentro del CSV

        
        self.EL_data = np.empty(self.max_index) #Array para los datos de elevacion (EL)
        self.AZ_data = np.empty(self.max_index) #Array para los datos de Azimuth (AZ)
        
        #Este paso es importante, pero puede modificarse. 
        #El objetivo principal de este paso es mover los datos de tipy dataframe a tipo Numpy Array.
        #Esto permite que los datos sean tomados como numeros y su manejo sea mas sencillo en algunos pasos,
        #especificamente, al momento de encontrar maximos y minimos. 
        for i in range (0,self.max_index):
            self.EL_data[i] = self.df.EL[i]
            
        for i in range (0,self.max_index):
            self.AZ_data[i] = self.df.AZ[i]

       
    def data_calculation_AZ(self,angle,antena_gain, _envelope,EL_PEAK,AZ_pos,_chart_title_ = "AZChart",_filename_ = "AZ_Chart"):
        '''
        Funcion que calcula todo lo referente para la grafica de AZ

        Parameters
        ----------
        angle : TYPE Float
            Angulo de inicio para el barrido
        antena_gain : TYPE Float
            Ganancia de la antea
        _envelope : TYPE Int
            1 o 0, para determinar si se calcula o no la envolvente en la grafica y se muestre la figura correcta
        EL_PEAK : TYPE FLoat
            Elevation PEAK, posicion en EL
        AZ_pos : TYPE Float
            Posicion en AZ
        _chart_title_ : TYPE String, optional
            DESCRIPTION. The default is "AZChart". Para nombrar el grafico de AZ
        _filename_ : TYPE String, optional
            DESCRIPTION. The default is "AZ_Chart". Para nombrar el archivo de la imagen de AZ

        Returns
        -------
        AZ_data : TYPE tableStyle
            Estructura de datos que contiene la informacion para generar la tabla en el PDF

        '''
        max_data = max(self.AZ_data) #Busca el maximo
        print(self.AZ_data)
        #definicion de variables
        self.difference_AZ = np.empty(self.max_index) #creacion del array vacio, esto solo es para
                                              #un mejor manejo del tipo de datos
        
        #definicion de variables
        correction_angle = math.cos(EL_PEAK*(3.14159/180)) #correccion al angulo de AZ
        correct_angle_AZ = round((angle/correction_angle),2)
        
        for i in range (0,self.max_index):
            self.difference_AZ[i] = (self.AZ_data[i] - max_data) #calcula la diferencia
        
        for i in range (0, len(self.difference_AZ)):
            if (self.difference_AZ[i] == 0):
                index_value = i #encuentra el indice de donde esta el valor.
                
        step_size = angle/(index_value-1) #calcula el step para el barrido
        self.angle_step_AZ = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                              #en -angle-
        self.angle_step_AZ[0] = angle #primer elemento es igual al angulo dado
        
        for i in range (1,self.max_index):
            self.angle_step_AZ[i] = self.angle_step_AZ[i-1] - step_size #calcula el barrido
                                       
        min_value = min(self.difference_AZ) #encuentra el valor minimo de la diferencia
        
        self.correction_angle_AZ = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                  #en -angle-, pero en este caso, este array es para la correccion del angulo.
                                  
        for i in range (0,self.max_index):
            self.correction_angle_AZ[i] = self.angle_step_AZ[i]*correction_angle #calcula el nuevo angulo (correccion)
        
        if _envelope == 0:
            figure_generator(self.angle_step_AZ,self.difference_AZ,np.NaN,_filename_,_chart_title_, 0)
            overshoot = 0
        else:
            #calculo de la envolvente
            envelope = np.empty(self.max_index)
            
            for i in range(0,self.max_index):
                if self.angle_step_AZ[i] <=-1 or self.angle_step_AZ[i]>=1:
                    calc = -antena_gain+(32-25*math.log10(np.abs(self.correction_angle_AZ[i])))
                    envelope[i] = calc
                else:
                    envelope[i] = np.NaN
                
            overshoot = 0
    
            for i in range(0,self.max_index):
                if self.difference_AZ[i] > envelope[i]:
                    overshoot+=1
            figure_generator(self.angle_step_AZ,self.difference_AZ,envelope,_filename_,_chart_title_, 1)
        
        AZ_data = report_template_table(round(correct_angle_AZ,2), max_data, min_value, step_size,antena_gain,EL_PEAK,AZ_pos,overshoot,_envelope)
        

        return AZ_data    
    
    def data_calculation_EL(self,angle,antena_gain, _envelope,EL_PEAK,AZ_pos,_chart_title_ = "ELChart",_filename_ = "EL_Chart"):
        '''
        Funcion que calcula todo lo referente para la grafica de EL

        Parameters
        ----------
        angle : TYPE Float
            Angulo de inicio para el barrido
        antena_gain : TYPE Float
            Ganancia de la antea
        _envelope : TYPE Int
            1 o 0, para determinar si se calcula o no la envolvente en la grafica y se muestre la figura correcta
        EL_PEAK : TYPE FLoat
            Elevation PEAK, posicion en EL
        AZ_pos : TYPE Float
            Posicion en AZ
        _chart_title_ : TYPE String, optional
            DESCRIPTION. The default is "ElChart". Para nombrar el grafico de EL
        _filename_ : TYPE String, optional
            DESCRIPTION. The default is "EL_Chart". Para nombrar el archivo de la imagen de EL

        Returns
        -------
        EL_data : TYPE tableStyle
            Estructura de datos que contiene la informacion para generar la tabla en el PDF

        '''

        max_data = max(self.EL_data)
        self.difference_EL = np.empty(self.max_index) #creacion del array vacio, esto solo es para
                                              #un mejor manejo del tipo de datos

        #antena_gain = 53.697342562316 #ganancia de la antena
        
        for i in range (0,self.max_index):
            self.difference_EL[i] = (self.df.EL[i] - max_data) #calcula la diferencia
        
        for i in range (0, len(self.difference_EL)):
            if (self.difference_EL[i] == 0):
                #print(i+1) 
                index_value = i #encuentra el indice de donde esta el valor.
                
        step_size = angle/(index_value) #calcula el step para el barrido

        self.angle_step_EL = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                              #en -angle-
        self.angle_step_EL[0] = angle #primer elemento es igual al angulo dado
        
        for i in range (1,self.max_index):
            self.angle_step_EL[i] = self.angle_step_EL[i-1] - step_size #calcula el barrido
                          
        min_value = min(self.difference_EL) #encuentra el valor minimo de la diferencia
    
        if _envelope == 0:
            el_chart = figure_generator(self.angle_step_EL,self.difference_EL,np.NaN,_filename_,_chart_title_, 0)
            overshoot = 0
        else:
            #calculo de la envolvente
            envelope = np.empty(self.max_index)
            
            for i in range(0,self.max_index):
                if self.angle_step_EL[i] <=-1 or self.angle_step_EL[i]>=1:
                    calc = (32-25*math.log10(np.abs(self.angle_step_EL[i])))-antena_gain
                    envelope[i] = calc
                else:
                    envelope[i] = np.NaN
                
            overshoot = 0
    
            for i in range(0,self.max_index):
                if self.difference_EL[i] > envelope[i]:
                    overshoot+=1
                    
            el_chart = figure_generator(self.angle_step_EL,self.difference_EL,envelope,_filename_,_chart_title_,1)
        self.antena_gain_real = antena_gain
        EL_data = report_template_table(angle, max_data, min_value, step_size,antena_gain,EL_PEAK,AZ_pos,overshoot,_envelope)
        return EL_data

        
    def report_generator(self,_az_filename,_el_filename, AZ, EL, CALCULATED_GAIN,PDF_NAME,envelope,antena_diameter,PAD_ID,band_id):
        '''
        Funcion que genera el archivo PDF utilizando la tabla de AZ y EL asi como las respectivas
        figuras generadas.

        Parameters
        ----------
        _az_filename : TYPE String
            DESCRIPTION. El nombre de la figura generada para AZ, puede ser de ganancia o envolvente
        _el_filename : TYPE String
            DESCRIPTION. El nombre de la figura generada para EL, puede ser de ganancia o envolvente
        AZ : TYPE tableStyle
            DESCRIPTION. Tabla con la informacion referente a los calculos de AZ
        EL : TYPE tableStyle
            DESCRIPTION. Tabla con la informacion referente a los calculos de EL
        CALCULATED_GAIN : TYPE Float
            DESCRIPTION. Ganancia calculada (si envelope = 0)
        PDF_NAME : TYPE String
            DESCRIPTION. Nombre del archivo PDF a generar
        envelope : TYPE Int
            DESCRIPTION. 1 o 0, para generar las tablas y textos correctos segun sea de ganancia o envolvente

        Returns
        -------
        None.

        '''
        doc = SimpleDocTemplate(PDF_NAME, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)

# GENERANDO EL CANVAS PARA "DIBUJAR" EL PDF
        c = canvas.Canvas(PDF_NAME)
        c.saveState()
        c.setFont("Helvetica", 14)
        styles = getSampleStyleSheet()
# FINALIZA EL START-UP DE LA CONFIGURACION DEL ARCHIVO PDF

# DIBUJANDO EL TITULO
        PAGE_WIDTH  = doc.width
        PAGE_HEIGHT = doc.height
        
        if envelope == 0:
            title_pdf_ = "Gain Report " + antena_diameter + "m Antenna " + PAD_ID +" "+ band_id + "-band"
        else:
            title_pdf_ = "Envelope " + antena_diameter + "m Antenna " + PAD_ID +" "+ band_id + "-band"
        
        p = Paragraph(title_pdf_,styles['Heading1'])
        w, h = p.wrap(doc.width, doc.bottomMargin)
        p.drawOn(c, doc.width/2-140, HEIGHT_TITLE)
#FINALIZA EL DIBUJO DEL TITULO

#DIBUJA EL LOGO DE CPI 
#header
        header = Image('cpilogo.jpg')
        header.drawHeight = 70
        header.drawWidth = 100
        header.hAlign = 'RIGHT'
        w , h = header.wrap(doc.width , doc.topMargin)
        header.drawOn(c , doc.leftMargin , 710)
#FINALIZA EL DIBUJO DE CPI    
   
#INICIA LOGO RSI
#header
        header = Image('rsilogo.png')
        header.drawHeight = 50
        header.drawWidth = 175
        header.hAlign = 'LEFT'
        w , h = header.wrap(doc.width , doc.topMargin)
        header.drawOn(c , doc._rightMargin-175 , 720)
#FINALIZA LOGO RSI

# Footer
        footer = Paragraph('FECHA Y HORA', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(c, doc.leftMargin, h)   


#DIBUJA LA GRAFICA AZ
#graph
        graph = Image(_az_filename)
        graph.drawHeight = 275
        graph.drawWidth = 395
        graph.hAlign = 'CENTER'
        #w , h = graph.wrap(doc.width , doc.topMargin)
        graph.drawOn(c , PAGE_WIDTH/2-140 ,PAGE_HEIGHT/2-10)
#FINALIZA DIBUJO DE GRAFICA

#DIBUJA LA TABLA 
        AZ.wrapOn(c, doc.width , doc.topMargin)
        AZ.drawOn(c, PAGE_WIDTH/2-70, PAGE_HEIGHT/2-200)
#FINALIZA DIBUJO 

        c.showPage()
        
 #------- ELEVATION ------------------       
#DIBUJA EL LOGO DE CPI 
#header
        header = Image('cpilogo.jpg')
        header.drawHeight = 70
        header.drawWidth = 100
        header.hAlign = 'RIGHT'
        w , h = header.wrap(doc.width , doc.topMargin)
        header.drawOn(c , doc.leftMargin , 700)
#FINALIZA EL DIBUJO DE CPI    

#INICIA LOGO RSI
#header
        header = Image('rsilogo.png')
        header.drawHeight = 50
        header.drawWidth = 175
        header.hAlign = 'LEFT'
        w , h = header.wrap(doc.width , doc.topMargin)
        header.drawOn(c , doc._rightMargin-175 , 720)
#FINALIZA LOGO RSI

# Footer
        footer = Paragraph('FECHA Y HORA', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(c, doc.leftMargin, h)   

#DIBUJA LA GRAFICA EL
#graph
        graph = Image(_el_filename)
        graph.drawHeight = 275
        graph.drawWidth = 395
        graph.hAlign = 'CENTER'
        #w , h = graph.wrap(doc.width , doc.topMargin)
        graph.drawOn(c , PAGE_WIDTH/2-140 ,PAGE_HEIGHT/2-10)
#FINALIZA DIBUJO DE GRAFICA

#DIBUJA LA TABLA 
        EL.wrapOn(c, doc.width , doc.topMargin)
        EL.drawOn(c, PAGE_WIDTH/2-70, PAGE_HEIGHT/2-200)
#FINALIZA DIBUJO 

#PARA MOSTRAR LA GANANCIA:
        if envelope == 0:
            text = "CALCULATED GAIN: " + str(round(CALCULATED_GAIN,2))
            para = Paragraph(text, styles["Heading3"])
            
            w, h = para.wrap(doc.width, doc.bottomMargin)
            para.drawOn(c, doc.width/2-50, PAGE_HEIGHT/2-240)
            
            if self.antena_gain_real < CALCULATED_GAIN or CALCULATED_GAIN == self.antena_gain_real:
                text_2 = "GAIN PASS "
                para2 = Paragraph(text_2, styles["Heading3"])
                w, h = para2.wrap(doc.width, doc.bottomMargin)
                para2.drawOn(c, doc.width/2-50, PAGE_HEIGHT/2-260)
#FINALIZA LA CREACION DEL REPORTE

        s = getSampleStyleSheet()
        elements = []
        p = ParagraphStyle('yourtitle',alignment = 1,parent=s['Heading1'])
        
   
        paragraph_1 = Paragraph("PREELIMINAR TEMPLATE REPORT", p)
        elements.append(paragraph_1)

        
        #Send the data and build the file
        elements.append(Image(_az_filename))
        elements.append(AZ)
        elements.append(PageBreak())
        elements.append(Image(_el_filename))
        elements.append(EL)
        if envelope == 0:
            text = "CALCULATED GAIN: " + str(round(CALCULATED_GAIN,2))
            para = Paragraph(text, s["Heading3"])
            elements.append(para)
            if self.antena_gain_real < CALCULATED_GAIN or CALCULATED_GAIN == self.antena_gain_real:
                text_2 = "GAIN PASS "
                para2 = Paragraph(text_2, s["Heading3"])
                elements.append(para2)
            
        #footer_content = Paragraph("This is a footer. It goes on every page.  ", s['Normal'])
        #canvas.saveState()
        #w, h = footer_content.wrap(doc.width, doc.bottomMargin)
        #elements.append(footer_content)
        #canvas.restoreState()

                
        doc.build(elements)
        c.save()
        
    def gain_calculation(self):
        '''
        Calcula la ganancia de la Antena

        Returns
        -------
        CALCULATED_GAIN : TYPE Float
            DESCRIPTION. Ganancia calculada

        '''
        db_10 = -10
        db_3 = -3
        #self.angle_step_EL
        #self.angle_step_AZ
        
        #self.correction_angle_AZ
        
        self.rf_new_AZ = np.empty(self.max_index)
        
        for i in range (0,len(self.correction_angle_AZ)):
            if self.correction_angle_AZ[i] > 0:
                self.rf_new_AZ[i] = -self.difference_AZ[i]
            else:
                self.rf_new_AZ[i] = self.difference_AZ[i]
                
        #para AZ
        index_negative_10dB = 0
        index_positive_10dB = 0
        index_negative_3dB = 0
        index_positive_3dB = 0
        
        diff_index_10n = 300
        diff_index_10p = 300
        diff_index_3n = 300
        diff_index_3p = 300
        for i in range (0, len(self.rf_new_AZ)):
            
            if abs(self.rf_new_AZ[i])%abs(CONST_DB_M_10) <1:
                if diff_index_10n > abs(self.rf_new_AZ[i]-CONST_DB_M_10) and self.rf_new_AZ[i] < 0:
                    index_negative_10dB = i
                    diff_index_10n = abs(self.rf_new_AZ[i]-CONST_DB_M_10)
                # if abs(self.rf_new_EL[i]-CONST_DB_M_10)<0.17 and self.rf_new_EL[i] < 0:
                #     index_negative_10dB = i
                    
            if abs(self.rf_new_AZ[i])%abs(CONST_DB_M_10) <1:
                if diff_index_10p > abs(self.rf_new_AZ[i]+CONST_DB_M_10):
                    index_positive_10dB = i
                    diff_index_10p = abs(self.rf_new_AZ[i]+CONST_DB_M_10)
                # if abs(self.rf_new_EL[i]+CONST_DB_M_10)<0.17:
                #     print("diferencia entre const y angulo",self.rf_new_EL[i]+CONST_DB_M_10)
                #     index_positive_10dB = i
                    
            if abs(self.rf_new_AZ[i])%abs(CONST_DB_M_3) <1:
                if diff_index_3n > abs(self.rf_new_AZ[i]-CONST_DB_M_3) and self.rf_new_AZ[i] < 0:
                    index_negative_3dB = i
                    diff_index_3n = abs(self.rf_new_AZ[i]-CONST_DB_M_3)
                # if abs(self.rf_new_EL[i]-CONST_DB_M_3)<0.17 and self.rf_new_EL[i] < 0:
                #     index_negative_3dB = i
                    
            if abs(self.rf_new_AZ[i])%abs(CONST_DB_M_3) <1:
                if diff_index_3p > abs(self.rf_new_AZ[i]+CONST_DB_M_3):
                    index_positive_3dB = i
                    diff_index_3p = abs(self.rf_new_AZ[i]+CONST_DB_M_3)
                # if abs(self.rf_new_EL[i]+CONST_DB_M_3)<0.17:
                #     index_positive_3dB = i
        
        # for i in range (0, len(self.rf_new_AZ)):
        #     if index_negative_10dB == 0:
        #         if abs(self.rf_new_AZ[i]-CONST_DB_M_10) <0.17:
        #             index_negative_10dB = i
        #             print("index_negative_10dB",index_negative_10dB)
        #             # if i > 0:
        #             #     if abs(self.rf_new_AZ[i-1]-CONST_DB_M_10) <0.06:
        #             #         index_negative_10dB = i-1
        #             #         print(index_negative_10dB)
                    
        #     if index_positive_10dB == 0:
        #         if abs(self.rf_new_AZ[i]+CONST_DB_M_10) <0.08:
        #             index_positive_10dB = i
        #             if i > 0:
        #                 if abs(self.rf_new_AZ[i-1]+CONST_DB_M_10) <0.06:
        #                     index_positive_10dB = i-1
                        
        #     if index_negative_3dB == 0:       
        #         if abs(self.rf_new_AZ[i]-CONST_DB_M_3) <0.08:
        #             index_negative_3dB = i
        #             if i > 0:
        #                 if abs(self.rf_new_AZ[i-1]-CONST_DB_M_3) <0.06:
        #                     index_negative_3dB = i-1
        #     if index_positive_3dB == 0:      
        #         if abs(self.rf_new_AZ[i]+CONST_DB_M_3) <0.08:
        #             index_positive_3dB = i
        #             if i>0:
        #                 if abs(self.rf_new_AZ[i-1]+CONST_DB_M_3) <0.06:
        #                     index_positive_3dB = i-1
                        
        for u in range (0,4):
            if u == 0:
               up_10n= index_negative_10dB + 1
               down_10n = index_negative_10dB - 1
               
               _10n_angle = self.rf_new_AZ[index_negative_10dB]
               #print(_10n_angle)
               _10n_angle_UP = self.rf_new_AZ[up_10n]
               #print(_10n_angle_UP)
               _10n_angle_DOWN = self.rf_new_AZ[down_10n]
               # print("imprimiendo la correccion")
               # print(self.correction_angle_AZ)
               _10n_step = self.correction_angle_AZ[index_negative_10dB]
               _10n_step_UP = self.correction_angle_AZ[up_10n]
               _10n_step_DOWN = self.correction_angle_AZ[down_10n]
               # print("imprimiendo los step")
               # print(_10n_step)
               # print(_10n_step_UP)
               # print(_10n_step_DOWN)
               # print("----------------------")
               #buscando el angulo para negativ
               
               
               if _10n_angle > db_10:
                   diff_10n = _10n_angle - db_10
               else:
                   diff_10n = -(_10n_angle - db_10)
                   
               if _10n_angle_UP > db_10:
                   diff_10n_UP = _10n_angle_UP - db_10
               else:
                   diff_10n_UP = -(_10n_angle_UP - db_10)
                   
               if _10n_angle_DOWN > db_10:
                   diff_10n_DOWN = _10n_angle_DOWN - db_10
               else:
                   diff_10n_DOWN = -(_10n_angle_DOWN - db_10)
                   
               # print("Imprimiendo las diferencias de 10")
               # print(diff_10n)
               # print(diff_10n_UP)
               # print(diff_10n_DOWN)
               # print("----------------------")
               #buscando el angulo para negativo    
               if diff_10n < diff_10n_UP and diff_10n < diff_10n_DOWN:
                   AZ_10_DOWN = round(_10n_step,3)
                   
               elif diff_10n > diff_10n_UP and diff_10n_DOWN > diff_10n_UP:
                   AZ_10_DOWN = round(_10n_step_UP,3)
                   
               elif diff_10n > diff_10n_DOWN and diff_10n_DOWN < diff_10n_UP:
                   AZ_10_DOWN = round(_10n_step_DOWN,3)
                
        
            if u == 1:
               up_3n = index_negative_3dB - 1
               down_3n = index_negative_3dB + 1
               
               _3n_angle = self.rf_new_AZ[index_negative_3dB]
               _3n_angle_UP = self.rf_new_AZ[up_3n]
               _3n_angle_DOWN = self.rf_new_AZ[down_3n]
               
               _3n_step = self.correction_angle_AZ[index_negative_3dB]
               _3n_step_UP = self.correction_angle_AZ[up_3n]
               _3n_step_DOWN = self.correction_angle_AZ[down_3n]
               
               if _3n_angle > db_3:
                   diff_3n = _3n_angle - db_3
               else:
                   diff_3n = -(_3n_angle - db_3)
                   
               if _3n_angle_UP > db_3:
                   diff_3n_UP = _3n_angle_UP - db_3
               else:
                   diff_3n_UP = -(_3n_angle_UP - db_3)
                   
               if _3n_angle_DOWN > db_3:
                   diff_3n_DOWN = _3n_angle_DOWN - db_3
               else:
                   diff_3n_DOWN = -(_3n_angle_DOWN - db_3)
                   
               # print("Imprimiendo las diferencias de 10")
               # print(diff_10n)
               # print(diff_10n_UP)
               # print(diff_10n_DOWN)
               # print("----------------------")
               #buscando el angulo para negativo    
               if diff_3n < diff_3n_UP and diff_3n < diff_3n_DOWN:
                   AZ_3_DOWN = round(_3n_step,3)
                   
               elif diff_3n > diff_3n_UP and diff_3n_DOWN > diff_3n_UP:
                   AZ_3_DOWN = round(_3n_step_UP,3)
                   
               elif diff_3n > diff_3n_DOWN and diff_3n_DOWN < diff_3n_UP:
                   AZ_3_DOWN = round(_3n_step_DOWN,3)
               
            if u == 2:
               up_3p = index_positive_3dB + 1
               down_3p = index_positive_3dB - 1
                   
               _3p_angle = self.rf_new_AZ[index_positive_3dB]
               _3p_angle_UP = self.rf_new_AZ[up_3p]
               _3p_angle_DOWN = self.rf_new_AZ[down_3p]
               
               _3p_step = self.correction_angle_AZ[index_positive_3dB]
               _3p_step_UP = self.correction_angle_AZ[up_3p]
               _3p_step_DOWN = self.correction_angle_AZ[down_3p]
               #print("angulo up 3" ,self.angle_step_EL[up_3p])
               
               if _3p_angle > -db_3:
                   diff_3p = _3p_angle + db_3
               else:
                   diff_3p = -(_3p_angle + db_3)
                   
               if _3p_angle_UP > -db_3:
                   diff_3p_UP = _3p_angle_UP - (-db_3)
               else:
                   diff_3p_UP = -(_3p_angle_UP - (-db_3))
                   
               if _3p_angle_DOWN > -db_3:
                   diff_3p_DOWN = _3p_angle_DOWN - (-db_3)
               else:
                   diff_3p_DOWN = -(_3p_angle_DOWN - (-db_3))
                   
                
               # print("Imprimiendo las diferencias")
               # print(diff_3p)
               # print(diff_3p_UP)
               # print(_3p_angle)
               # print(diff_3p_DOWN)
               # print("----------------------")
               #buscando el angulo para negativo    
               if diff_3p < diff_3p_UP and diff_3p< diff_3p_DOWN:
                   AZ_3_UP = round(_3p_step,3)
                   
               elif diff_3p > diff_3p_UP and diff_3p_DOWN > diff_3p_UP:
                   AZ_3_UP = round(_3p_step_UP,3)
                   
               elif diff_3p > diff_3p_DOWN and diff_3p_DOWN < diff_3p_UP:
                   AZ_3_UP = round(_3p_step_DOWN,3)
               
            if u == 3:
               up_10p = index_positive_10dB + 1
               down_10p = index_positive_10dB - 1
               
               
               _10p_angle = self.rf_new_AZ[index_positive_10dB]
               _10p_angle_UP = self.rf_new_AZ[up_10p]
               _10p_angle_DOWN = self.rf_new_AZ[down_10p]
               
               _10p_step = self.correction_angle_AZ[index_positive_10dB]
               _10p_step_UP = self.correction_angle_AZ[up_10p]
               _10p_step_DOWN = self.correction_angle_AZ[down_10p]
               
               if _10p_angle > -db_10:
                   diff_10p = _10p_angle + db_10
               else:
                   diff_10p = -(_10p_angle + db_10)
                   
               if _10p_angle_UP > -db_10:
                   diff_10p_UP = _10p_angle_UP + db_10
               else:
                   diff_10p_UP = -(_10p_angle_UP + db_10)
                   
               if _10p_angle_DOWN > -db_10:
                   diff_10p_DOWN = _10p_angle_DOWN + db_10
               else:
                   diff_10p_DOWN = -(_10p_angle_DOWN + db_10)
                   
               #buscando el angulo para negativo    
               if diff_10p < diff_10p_UP and diff_10p< diff_10p_DOWN:
                   AZ_10_UP = round(_10p_step,3)
                   
               elif diff_10p > diff_10p_UP and diff_10p_DOWN > diff_10p_UP:
                   AZ_10_UP = round(_10p_step_UP,3)
                   
               elif diff_10p > diff_10p_DOWN and diff_10p_DOWN < diff_10p_UP:
                   AZ_10_UP = round(_10p_step_DOWN,3)    
   ##---------------- PARA DEBUGING ------------------ ##                
        # print("PARA AZIMUTH")
        # print("Elevation 10dB DOWN",AZ_10_DOWN)   
        # print("Elevation 10dB UP",AZ_10_UP)     
        # print("Elevation 3dB UP",AZ_3_UP)
        # print("Elevation 3dB Down", AZ_3_DOWN)
        # print()
        # print("index_negative_10dB -10",index_negative_10dB) 
        # print("index_negative_3dB -3",index_negative_3dB) 
        # print("index_positive_3dB 3",index_positive_3dB) 
        # print("index_positive_10dB 10",index_positive_10dB)   
                
        #para EL
        index_negative_10dB = 0
        index_positive_10dB = 0
        index_negative_3dB = 0
        index_positive_3dB = 0
        
        diff_index_10n = 300
        diff_index_10p = 300
        diff_index_3n = 300
        diff_index_3p = 300
        #calculos iniciales para elevacion       
        self.rf_new_EL = np.empty(self.max_index)
        for i in range (0,len(self.angle_step_EL)):
            
            if self.angle_step_EL[i] > 0:
                self.rf_new_EL[i] =-self.difference_EL[i]
            else:
                self.rf_new_EL[i] = self.difference_EL[i]
              
        #para EL
        diff_index_10n = 300
        diff_index_10p = 300
        diff_index_3n = 300
        diff_index_3p = 300
        for i in range (0, len(self.rf_new_EL)):
            
            if abs(self.rf_new_EL[i])%abs(CONST_DB_M_10) <1:
                if diff_index_10n > abs(self.rf_new_EL[i]-CONST_DB_M_10) and self.rf_new_EL[i] < 0:
                    index_negative_10dB = i
                    diff_index_10n = abs(self.rf_new_EL[i]-CONST_DB_M_10)
                # if abs(self.rf_new_EL[i]-CONST_DB_M_10)<0.17 and self.rf_new_EL[i] < 0:
                #     index_negative_10dB = i
                    
            if abs(self.rf_new_EL[i])%abs(CONST_DB_M_10) <1:
                if diff_index_10p > abs(self.rf_new_EL[i]+CONST_DB_M_10):
                    index_positive_10dB = i
                    diff_index_10p = abs(self.rf_new_EL[i]+CONST_DB_M_10)
                # if abs(self.rf_new_EL[i]+CONST_DB_M_10)<0.17:
                #     print("diferencia entre const y angulo",self.rf_new_EL[i]+CONST_DB_M_10)
                #     index_positive_10dB = i
                    
            if abs(self.rf_new_EL[i])%abs(CONST_DB_M_3) <1:
                if diff_index_3n > abs(self.rf_new_EL[i]-CONST_DB_M_3) and self.rf_new_EL[i] < 0:
                    index_negative_3dB = i
                    diff_index_3n = abs(self.rf_new_EL[i]-CONST_DB_M_3)
                # if abs(self.rf_new_EL[i]-CONST_DB_M_3)<0.17 and self.rf_new_EL[i] < 0:
                #     index_negative_3dB = i
                    
            if abs(self.rf_new_EL[i])%abs(CONST_DB_M_3) <1:
                if diff_index_3p > abs(self.rf_new_EL[i]+CONST_DB_M_3):
                    index_positive_3dB = i
                    diff_index_3p = abs(self.rf_new_EL[i]+CONST_DB_M_3)
                # if abs(self.rf_new_EL[i]+CONST_DB_M_3)<0.17:
                #     index_positive_3dB = i
                        
        for u in range (0,4):
            if u == 0:
               up_10n= index_negative_10dB + 1
               down_10n = index_negative_10dB - 1
               
               _10n_angle = self.rf_new_EL[index_negative_10dB]
               #print(_10n_angle)
               _10n_angle_UP = self.rf_new_EL[up_10n]
               _10n_angle_DOWN = self.rf_new_EL[down_10n]
               
               _10n_step = self.angle_step_EL[index_negative_10dB]
               #print(_10n_step)
               _10n_step_UP = self.angle_step_EL[up_10n]
               _10n_step_DOWN = self.angle_step_EL[down_10n]
               
               if _10n_angle > db_10:
                   diff_10n = _10n_angle - db_10
               else:
                   diff_10n = -(_10n_angle - db_10)
                   
               if _10n_angle_UP > db_10:
                   diff_10n_UP = _10n_angle_UP - db_10
               else:
                   diff_10n_UP = -(_10n_angle_UP - db_10)
                   
               if _10n_angle_DOWN > db_10:
                   diff_10n_DOWN = _10n_angle_DOWN - db_10
               else:
                   diff_10n_DOWN = -(_10n_angle_DOWN - db_10)
                   
               # print("Imprimiendo las diferencias de 10")
               # print(diff_10n)
               # print(diff_10n_UP)
               # print(diff_10n_DOWN)
               # print("----------------------")
               #buscando el angulo para negativo    
               if diff_10n < diff_10n_UP and diff_10n < diff_10n_DOWN:
                   EL_10_DOWN = round(_10n_step,3)
                   
               elif diff_10n > diff_10n_UP and diff_10n_DOWN > diff_10n_UP:
                   EL_10_DOWN = round(_10n_step_UP,3)
                   
               elif diff_10n > diff_10n_DOWN and diff_10n_DOWN < diff_10n_UP:
                   EL_10_DOWN = round(_10n_step_DOWN,3)
                
        
            if u == 1:
               up_3n = index_negative_3dB - 1
               down_3n = index_negative_3dB + 1
               
               _3n_angle = self.rf_new_EL[index_negative_3dB]
               _3n_angle_UP = self.rf_new_EL[up_3n]
               _3n_angle_DOWN = self.rf_new_EL[down_3n]
               
               _3n_step = self.angle_step_EL[index_negative_3dB]
               _3n_step_UP = self.angle_step_EL[up_3n]
               _3n_step_DOWN = self.angle_step_EL[down_3n]
               
               if _3n_angle > db_3:
                   diff_3n = _3n_angle - db_3
               else:
                   diff_3n = -(_3n_angle - db_3)
                   
               if _3n_angle_UP > db_3:
                   diff_3n_UP = _3n_angle_UP - db_3
               else:
                   diff_3n_UP = -(_3n_angle_UP - db_3)
                   
               if _3n_angle_DOWN > db_3:
                   diff_3n_DOWN = _3n_angle_DOWN - db_3
               else:
                   diff_3n_DOWN = -(_3n_angle_DOWN - db_3)
                   
               # print("Imprimiendo las diferencias de 10")
               # print(diff_10n)
               # print(diff_10n_UP)
               # print(diff_10n_DOWN)
               # print("----------------------")
               #buscando el angulo para negativo    
               if diff_3n < diff_3n_UP and diff_3n < diff_3n_DOWN:
                   EL_3_DOWN = round(_3n_step,3)
                   
               elif diff_3n > diff_3n_UP and diff_3n_DOWN > diff_3n_UP:
                   EL_3_DOWN = round(_3n_step_UP,3)
                   
               elif diff_3n > diff_3n_DOWN and diff_3n_DOWN < diff_3n_UP:
                   EL_3_DOWN = round(_3n_step_DOWN,3)
               
            if u == 2:
               up_3p = index_positive_3dB + 1
               down_3p = index_positive_3dB - 1
                   
               _3p_angle = self.rf_new_EL[index_positive_3dB]
               _3p_angle_UP = self.rf_new_EL[up_3p]
               _3p_angle_DOWN = self.rf_new_EL[down_3p]
               
               _3p_step = self.angle_step_EL[index_positive_3dB]
               _3p_step_UP = self.angle_step_EL[up_3p]
               _3p_step_DOWN = self.angle_step_EL[down_3p]
               #print("angulo up 3" ,self.angle_step_EL[up_3p])
               
               if _3p_angle > -db_3:
                   diff_3p = _3p_angle + db_3
               else:
                   diff_3p = -(_3p_angle + db_3)
                   
               if _3p_angle_UP > -db_3:
                   diff_3p_UP = _3p_angle_UP - (-db_3)
               else:
                   diff_3p_UP = -(_3p_angle_UP - (-db_3))
                   
               if _3p_angle_DOWN > -db_3:
                   diff_3p_DOWN = _3p_angle_DOWN - (-db_3)
               else:
                   diff_3p_DOWN = -(_3p_angle_DOWN - (-db_3))
                   
                
               # print("Imprimiendo las diferencias")
               # print(diff_3p)
               # print(diff_3p_UP)
               # print(_3p_angle)
               # print(diff_3p_DOWN)
               # print("----------------------")
               #buscando el angulo para negativo    
               if diff_3p < diff_3p_UP and diff_3p< diff_3p_DOWN:
                   EL_3_UP = round(_3p_step,3)
                   
               elif diff_3p > diff_3p_UP and diff_3p_DOWN > diff_3p_UP:
                   EL_3_UP = round(_3p_step_UP,3)
                   
               elif diff_3p > diff_3p_DOWN and diff_3p_DOWN < diff_3p_UP:
                   EL_3_UP = round(_3p_step_DOWN,3)
               
            if u == 3:
               up_10p = index_positive_10dB + 1
               down_10p = index_positive_10dB - 1
               
               
               _10p_angle = self.rf_new_EL[index_positive_10dB]
               _10p_angle_UP = self.rf_new_EL[up_10p]
               _10p_angle_DOWN = self.rf_new_EL[down_10p]
               
               _10p_step = self.angle_step_EL[index_positive_10dB]
               _10p_step_UP = self.angle_step_EL[up_10p]
               _10p_step_DOWN = self.angle_step_EL[down_10p]
               
               if _10p_angle > -db_10:
                   diff_10p = _10p_angle + db_10
               else:
                   diff_10p = -(_10p_angle + db_10)
                   
               if _10p_angle_UP > -db_10:
                   diff_10p_UP = _10p_angle_UP + db_10
               else:
                   diff_10p_UP = -(_10p_angle_UP + db_10)
                   
               if _10p_angle_DOWN > -db_10:
                   diff_10p_DOWN = _10p_angle_DOWN + db_10
               else:
                   diff_10p_DOWN = -(_10p_angle_DOWN + db_10)
                   
               #buscando el angulo para negativo    
               if diff_10p < diff_10p_UP and diff_10p< diff_10p_DOWN:
                   EL_10_UP = round(_10p_step,3)
                   
               elif diff_10p > diff_10p_UP and diff_10p_DOWN > diff_10p_UP:
                   EL_10_UP = round(_10p_step_UP,3)
                   
               elif diff_10p > diff_10p_DOWN and diff_10p_DOWN < diff_10p_UP:
                   EL_10_UP = round(_10p_step_DOWN,3)
            
       
        ##---------- PARA DEBUGING ------------------ ##
        # print("PARA ELEVACION")
        # print("Elevation 10dB DOWN",EL_10_DOWN)   
        # print("Elevation 10dB UP",EL_10_UP)     
        # print("Elevation 3dB UP",EL_3_UP)
        # print("Elevation 3dB Down", EL_3_DOWN)
        # print()
        # print("index_negative_10dB -10",index_negative_10dB) 
        # print("index_negative_3dB -3",index_negative_3dB) 
        # print("index_positive_3dB 3",index_positive_3dB) 
        # print("index_positive_10dB 10",index_positive_10dB)    

        _3dB_AZ = round(-AZ_3_DOWN + AZ_3_UP,3)
        _3dB_EL = round(-EL_3_DOWN + EL_3_UP,3)
        
        _10dB_AZ = round(-AZ_10_DOWN + AZ_10_UP,3)
        _10dB_EL = round(-EL_10_DOWN + EL_10_UP,3)
        # print(_3dB_AZ)
        # print(_3dB_EL)
        ganancia_3db = 10*math.log10(31000/(_3dB_EL * _3dB_AZ))
        ganancia_10db = 10*math.log10(91000/(_10dB_EL * _10dB_AZ))
        print(ganancia_3db)
        print(ganancia_10db)
        
        GAIN = (ganancia_10db + ganancia_3db)/2
        print(GAIN)
        
        FEED_LOSS = 0.5
        RMS_LOSS = 0.02
        
        CALCULATED_GAIN = GAIN - FEED_LOSS - RMS_LOSS
        print("GANANCIA CALCULADA",CALCULATED_GAIN)
        return CALCULATED_GAIN
        
        #CONST_DB_M_10 = -10 #esta
        #CONST_DB_M_10_UP = -9.9
        #CONST_DB_M_10_DOWN = -10.1
        
        #CONST_DB_M_3 = -3 #esta
        #CONST_DB_M_3_UP = -2.9
        #CONST_DB_M_3_DOWN = -3.1
        
                
        
        

        
# antena_gain = 53.697342562316
# EL_PEAK = 30.50
# Using current time
# ini_time_for_now = datetime.now()
# _chart_title_ = "Azimuth Pattern for 9.0m Antenna # 4 C-Band"
# _chart_title2_ = "Elevation Pattern for 9.0m Antenna # 4 C-Band"
# _filename_ = "AZ_ENV_Chart_PadC.png"
# _filename2_ = "EL_EN_Chart_PadC.png"

# antena_gain = 53.6973
#analyzer = analyzer_generator(filename)
# analyzer.data_calculation_AZ(-1.16,0,30.5,0,_chart_title_,_filename_)
# analyzer.data_calculation_EL(-1,0,0,_chart_title_,_filename2_)
# analyzer.gain_calculation()
#analyzer.data_calculation_AZ(angle, antena_gain, EL_PEAK, _envelope,_chart_title_ = "AZChart",_filename_ = "AZ_Chart")
#analyzer.data_calculation_EL(angle, antena_gain, _envelope,_chart_title_ = "ELChart",_filename_ = "EL_Chart")
#analyzer.gain_calculation()
# EL = analyzer.data_calculation_EL(-12, antena_gain, 1, _chart_title_, _filename_)
# AZ = analyzer.data_calculation_AZ(-13.15,antena_gain,30.5,1,_chart_title2_,_filename2_)

# # Using current time
# end_time_for_now = datetime.now()

# delta = end_time_for_now - ini_time_for_now 
#print(delta)
# analyzer.report_generator(_filename_, _filename2_,AZ,EL)
