#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 19:28:56 2022

@author: jguerra
"""

from Analyzer import analyzer_generator 

file_name = input("Ingrese la ruta del archivo de datos: ") #Acá el usuario ya sabe qué debe ingresar
analyzer = analyzer_generator(file_name)

EL_angle_txt = input("Ingrese el INICIO DEL PATRON PARA ELEVACION: ") #Acá el usuario ya sabe qué debe ingresar
EL_angle = float(EL_angle_txt)
AZ_angle_txt = input("Ingrese el INICIO DEL PATRON PARA AZIMUTH: ") 
AZ_angle = float(AZ_angle_txt)   

Az_position = input("Ingrese la posicion en AZIMUTH: ")
Az_position = float(Az_position)
EL_PEAK_txt = input("Ingrese el ELEVATION PEAK (POSICION): ") 
_EL_PEAK = float(EL_PEAK_txt)

Antena_gain_txt = input("Ingrese la GANANCIA de la antena: ") 
_antena_gain = float(Antena_gain_txt)







antena_diameter = input("Ingrese el DIAMETRO de la antena: ") 
PAD_ID = input("Coloque el ID del PAD: ") 
band_id = input("Coloque que tipo de banda es (C, L,Ku): ") 

PDF_name = input("Coloque el nombre del archivo PDF a generar: ")

PDF=PDF_name+".pdf"

envelope = input("¿Desea encontrar la envolvente? 0 para NO, 1 para SI: ") 
envelope = int(envelope)

AZ_chart_title = "Azimuth Pattern for " + antena_diameter + "m Antenna " + PAD_ID +" "+ band_id + "-band"
print(AZ_chart_title)

EL_chart_title = "Elevation Pattern for " + antena_diameter + "m Antenna " + PAD_ID +" "+ band_id + "-band"

filename_EL_gain = "EL_Chart_GAIN " + antena_diameter + "m Antenna " + PAD_ID 
filename_AZ_gain = "AZ_Chart_GAIN " + antena_diameter + "m Antenna " + PAD_ID 

filename_EL_env = "AZ_Chart_envelope " + antena_diameter + "m Antenna " + PAD_ID 
filename_AZ_env = "EL_Chart_envelope " + antena_diameter + "m Antenna " + PAD_ID 

if envelope == 0:
    AZ = analyzer.data_calculation_AZ(AZ_angle, _antena_gain, envelope,_EL_PEAK,Az_position,AZ_chart_title,filename_AZ_gain)
    EL = analyzer.data_calculation_EL(EL_angle, _antena_gain, envelope,_EL_PEAK,Az_position,EL_chart_title,filename_EL_gain)
    CALCULATED_GAIN = analyzer.gain_calculation()
    analyzer.report_generator(filename_AZ_gain+".png", filename_EL_gain+".png",AZ,EL,CALCULATED_GAIN,PDF,envelope,antena_diameter,PAD_ID,band_id)
else:
    AZ = analyzer.data_calculation_AZ(AZ_angle, _antena_gain, envelope,_EL_PEAK,Az_position,AZ_chart_title,_filename_ = filename_AZ_env)
    EL = analyzer.data_calculation_EL(EL_angle, _antena_gain, envelope,_EL_PEAK,Az_position,EL_chart_title,_filename_ = filename_EL_env)
    CALCULATED_GAIN = 0 #analyzer.gain_calculation()   
    analyzer.report_generator(filename_AZ_env+".png", filename_EL_env+".png",AZ,EL,CALCULATED_GAIN,PDF,envelope,antena_diameter,PAD_ID,band_id)
    
    
    
    
    
    