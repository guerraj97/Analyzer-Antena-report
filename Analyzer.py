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


def add_image(image_path):
    img = utils.ImageReader(image_path)
    img_width, img_height = img.getSize()
    aspect = img_height / float(img_width)

    my_canvas = canvas.Canvas("canvas_image.pdf",
                              pagesize=letter)
    my_canvas.saveState()
    #my_canvas.rotate(45)
    my_canvas.drawImage(image_path, 150, 10,
                        width=100, height=(100 * aspect))
    my_canvas.restoreState()
    my_canvas.save()

def figure_generator(angle_step, difference, envelope,_filename):
           #genera el diagrama
        fig = plt.figure(figsize=(12,7))
        plt.plot(angle_step,difference)
        plt.plot(angle_step,envelope,"-r")
        plt.ylabel('some numbers')
        fig.savefig(_filename)
        
def report_template_table(angle,max_data,min_value,step_size):
        s = getSampleStyleSheet()
        # elements = []
        
        data = [

        ["Parameter", "Value"],
        ["Azimuth", "01"],
        ["Elevation", "01"],
        ["Antenna Gain (REAL)",""],
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
        self.df = pd.read_csv(filename, error_bad_lines=False,sep=';')
        
        self.max_index = self.df.shape[0]
        #self.max_data = self.df.max()
        
        self.EL_data = np.empty(self.max_index)
        self.AZ_data = np.empty(self.max_index)
        
        for i in range (0,self.max_index):
            self.EL_data[i] = self.df.EL[i]
            
        for i in range (0,self.max_index):
            self.AZ_data[i] = self.df.AZ[i]

            
        self.max_data = max(self.EL_data)
        #return self.maxnumber
    
    def data_calculation(self, _type_calculation,angle,antena_gain, EL_PEAK):
        
        #definicion de variables
        correction_angle = math.cos(EL_PEAK*(3.14159/180))
        
        #definicion de variables
        self.angle = angle #angle de barrido
        difference = np.empty(self.max_index) #creacion del array vacio, esto solo es para
                                              #un mejor manejo del tipo de datos

        #antena_gain = 53.697342562316 #ganancia de la antena
        
        for i in range (0,self.max_index):
            difference[i] = (self.df.EL[i] - self.max_data) #calcula la diferencia
        
        for i in range (0, len(difference)):
            if (difference[i] == 0):
                #print(i+1) 
                index_value = i #encuentra el indice de donde esta el valor.
                
        self.step_size = self.angle/(index_value) #calcula el step para el barrido
        angle_step = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                              #en -angle-
        angle_step[0] = self.angle #primer elemento es igual al angulo dado
        
        for i in range (1,self.max_index):
            angle_step[i] = angle_step[i-1] - self.step_size #calcula el barrido
                                       
        self.min_value = min(difference) #encuentra el valor minimo de la diferencia
        
        if _type_calculation == "AZ":
            correction_angle_new = np.empty(self.max_index) #array para el calculo del barrido de los grados empezando
                                      #en -angle-
            for i in range (0,self.max_index):
                correction_angle_new[i] = angle_step[i]*correction_angle
            
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
            figure_generator(angle_step,difference,envelope,"AZChart")
            
            AZ_data = report_template_table(self.angle, self.max_data, self.min_value, self.step_size)
        
        # print("este es el valor maximo", self.max_data)
        # print("Este es el step size",self.step_size)
        # print("esta es la diferencia minima",self.min_value)
        
        if _type_calculation == "EL":
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
            figure_generator(angle_step,difference,envelope,"ELChart")
            
            EL_data = report_template_table(self.angle, self.max_data, self.min_value, self.step_size)
        return AZ_data, EL_data

        
    def report_generator(self,_az_filename,_el_filename, AZ, EL):
        doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
        doc.pagesize = landscape(A4)
        s = getSampleStyleSheet()
        elements = []
        
        # data = [

        # ["Parameter", "Value"],
        # ["Azimuth", "01"],
        # ["Elevation", "01"],
        # ["Antenna Gain (REAL)",""],
        # ["Start of Pattern", str(self.angle)],
        # ["Stop of Pattern", str(-self.angle)],
        # ["MAX", str(self.max_data)],
        # ["MIN", str(self.min_value)],
        # ["Step Size", str(self.step_size)],
        # ]
   
        paragraph_1 = Paragraph("PREELIMINAR TEMPLATE REPORT", s['Heading1'])
        elements.append(paragraph_1)
        # elements.append(Image(_el_filename))
        
        # #TODO: Get this line right instead of just copying it from the docs
        # style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
        #                        ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
        #                        ('VALIGN',(0,0),(0,-1),'TOP'),
        #                        ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
        #                        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
        #                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
        #                        ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
        #                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        #                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        #                        ])
        
        # #Configure style and word wrap
        
        # s = s["BodyText"]
        # s.wordWrap = 'CJK'
        # data2 = [[Paragraph(cell, s) for cell in row] for row in data]
        # t=Table(data2)
        # t.setStyle(style)
        
        #Send the data and build the file
        elements.append(Image(_az_filename))
        elements.append(AZ)
        elements.append(Image(_el_filename))
        elements.append(EL)

                
        doc.build(elements)
    
class report_generator():
    def __init__(self,cam_num = 0, WIDTH = 960, HEIGHT = 720):
        pass
        
antena_gain = 53.697342562316
EL_PEAK = 30.50

analyzer = analyzer_generator(filename)
AZ, EL = analyzer.data_calculation("EL", -12, antena_gain, EL_PEAK)
analyzer.report_generator("AZChart.png", "ELChart.png")
