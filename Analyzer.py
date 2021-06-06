#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 30 18:31:55 2021

Version 0.0.0 - Inicio del archivo.
30/05/2021 Version 0.0.1 - Creacion de las primeras clases para los calculos de los reportes.
                           Encuentra los maximos en los datos y los minimos en la diferencia, esto 
                           # sirve para poder realizar los calculos para el ploteo.
05/06/2021 Version 0.0.2 - Encuentra el minimo y maximo necesario para ciertos calculos. Grafica la figura 
                           con datos de elevacion y su respectiva grafica envolvente. Version preeliminar
                           de un documento PDF con una tabla que resume los datos y muestra la grafica
                           generada. 
05/06/2021 Version 0.0.3 - Generacion completa de un archivo PDF con graficas y tablas para AZ y EL.

@author: joseguerra
"""


#Librerias para la creacion de un reporte PDF

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import utils
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

filename = '/Users/joseguerra/Desktop/Libro1.csv'


def figure_generator(angle_step, difference, envelope,_filename, chart_title):
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
        
        plt.plot(angle_step,envelope,"-r") #ploteo de la envolvente
        plt.ylabel('some numbers')#axis name
        fig.savefig(_filename) #guarda la figura para su uso posterior en el reporte PDF
        
def report_template_table(angle,max_data,min_value,step_size,antena_gain):
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
            Step calculado para el barrido
        antena_gain : TYPE Float
            Ganancia de la antena
    
        Returns
        -------
        t : TYPE tableStyle
            Contiene una estructura de datos con toda la informacion para la generacion de la tabla 
            en el documento PDF
    
        '''
        s = getSampleStyleSheet()

        
        data = [

        ["Parameter", "Value"],
        ["Azimuth", "01"],
        ["Elevation", "01"],
        ["Antenna Gain (REAL)",str(antena_gain)],
        ["Start of Pattern", str(angle)],
        ["Stop of Pattern", str(-angle)],
        ["MAX", str(max_data)],
        ["MIN", str(min_value)],
        ["Step Size", str(step_size)],
        ]
   
        #paragraph_1 = Paragraph("PREELIMINAR TEMPLATE REPORT", s['Heading1'])
        # elements.append(paragraph_1)
        # elements.append(Image(_filename))
        
        #TODO: Get this line right instead of just copying it from the docs
        style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                               ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                               ('VALIGN',(0,0),(0,-1),'TOP'),
                               ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                               ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                               ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                               ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ])
        
        #Configure style and word wrap
        
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, s) for cell in row] for row in data]
        t=Table(data2)
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
        self.df = pd.read_csv(filename, error_bad_lines=False,sep=';')
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

       
    def data_calculation_AZ(self,angle,antena_gain, EL_PEAK):
        '''
        Funcion que calcula todo lo referente para la grafica de AZ

        Parameters
        ----------
        angle : TYPE Float
            Angulo de inicio para el barrido
        antena_gain : TYPE Float
            Ganancia de la antea
        EL_PEAK : TYPE FLoat
            Elevation PEAK

        Returns
        -------
        AZ_data : TYPE tableStyle
            Estructura de datos que contiene la informacion para generar la tabla en el PDF

        '''
        max_data = max(self.AZ_data) #Busca el maximo
        
        #definicion de variables
        difference = np.empty(self.max_index) #creacion del array vacio, esto solo es para
                                              #un mejor manejo del tipo de datos
        
        #definicion de variables
        correction_angle = math.cos(EL_PEAK*(3.14159/180)) #correccion al angulo de AZ
        
        
        for i in range (0,self.max_index):
            difference[i] = (self.df.AZ[i] - max_data) #calcula la diferencia
        
        for i in range (0, len(difference)):
            if (difference[i] == 0):
                index_value = i #encuentra el indice de donde esta el valor.
                
        step_size = angle/(index_value) #calcula el step para el barrido
        angle_step = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                              #en -angle-
        angle_step[0] = angle #primer elemento es igual al angulo dado
        
        for i in range (1,self.max_index):
            angle_step[i] = angle_step[i-1] - step_size #calcula el barrido
                                       
        min_value = min(difference) #encuentra el valor minimo de la diferencia
        
        correction_angle_new = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                  #en -angle-, pero en este caso, este array es para la correccion del angulo.
                                  
        for i in range (0,self.max_index):
            correction_angle_new[i] = angle_step[i]*correction_angle #calcula el nuevo angulo (correccion)
        
        #calculo de la envolvente
        envelope = np.empty(self.max_index)
        
        for i in range(0,self.max_index):
            if angle_step[i] <=-1 or angle_step[i]>=1:
                calc = -antena_gain+(32-25*math.log10(np.abs(correction_angle_new[i])))
                envelope[i] = calc
            else:
                envelope[i] = np.NaN
        overshoot = 0

        for i in range(0,self.max_index):
            if difference[i] > envelope[i]:
                overshoot+=1
        figure_generator(angle_step,difference,envelope,"AZChart","Azimuth Pattern for 9.0m Antenna # 4 C-Band")
        
        AZ_data = report_template_table(angle, max_data, min_value, step_size,antena_gain)
        

        return AZ_data    
    
    def data_calculation_EL(self,angle,antena_gain):
        '''
        Funcion que calcula todo lo referente para la grafica de EL

        Parameters
        ----------
        angle : TYPE Float
            Angulo de inicio para el barrido
        antena_gain : TYPE Float
            Ganancia de la antea

        Returns
        -------
        EL_data : TYPE tableStyle
            Estructura de datos que contiene la informacion para generar la tabla en el PDF

        '''
        max_data = max(self.EL_data)
        difference = np.empty(self.max_index) #creacion del array vacio, esto solo es para
                                              #un mejor manejo del tipo de datos

        #antena_gain = 53.697342562316 #ganancia de la antena
        
        for i in range (0,self.max_index):
            difference[i] = (self.df.EL[i] - max_data) #calcula la diferencia
        
        for i in range (0, len(difference)):
            if (difference[i] == 0):
                #print(i+1) 
                index_value = i #encuentra el indice de donde esta el valor.
                
        step_size = angle/(index_value) #calcula el step para el barrido
        angle_step = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                              #en -angle-
        angle_step[0] = angle #primer elemento es igual al angulo dado
        
        for i in range (1,self.max_index):
            angle_step[i] = angle_step[i-1] - step_size #calcula el barrido
                                       
        min_value = min(difference) #encuentra el valor minimo de la diferencia
    
        #calculo de la envolvente
        envelope = np.empty(self.max_index)
        
        for i in range(0,self.max_index):
            if angle_step[i] <=-1 or angle_step[i]>=1:
                calc = -antena_gain+(32-25*math.log10(np.abs(angle_step[i])))
                envelope[i] = calc
            else:
                envelope[i] = np.NaN
                
        overshoot = 0

        for i in range(0,self.max_index):
            if difference[i] > envelope[i]:
                overshoot+=1
        figure_generator(angle_step,difference,envelope,"ELChart","Elevation Pattern for 9.0m Antenna # 4 C-Band")
        
        EL_data = report_template_table(angle, max_data, min_value, step_size,antena_gain)
        return EL_data

        
    def report_generator(self,_az_filename,_el_filename, AZ, EL):
        '''
        

        Parameters
        ----------
        _az_filename : TYPE
            DESCRIPTION.
        _el_filename : TYPE
            DESCRIPTION.
        AZ : TYPE
            DESCRIPTION.
        EL : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
        doc.pagesize = landscape(A4)
        s = getSampleStyleSheet()
        elements = []
        
   
        paragraph_1 = Paragraph("PREELIMINAR TEMPLATE REPORT", s['Heading1'])
        elements.append(paragraph_1)

        
        #Send the data and build the file
        elements.append(Image(_az_filename))
        elements.append(AZ)
        elements.append(Image(_el_filename))
        elements.append(EL)

                
        doc.build(elements)

        
antena_gain = 53.697342562316
EL_PEAK = 30.50

analyzer = analyzer_generator(filename)
EL = analyzer.data_calculation_EL(-12, antena_gain)
AZ = analyzer.data_calculation_AZ(-13.93, antena_gain, EL_PEAK)
analyzer.report_generator("AZChart.png", "ELChart.png",AZ,EL)
