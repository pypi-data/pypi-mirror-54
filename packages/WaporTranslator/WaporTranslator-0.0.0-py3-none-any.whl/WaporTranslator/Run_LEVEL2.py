# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 17:03:41 2019
"""

import sys
import json
import warnings

import WaporTranslator.LEVEL_2 as L2

def main(Start_year_analyses, End_year_analyses, output_folder, Radiation_Data):

    # run WaporTranslator intermediate parameters (all of LEVEL2)
    L2.Run_Intermediate_Parameters.main(Start_year_analyses, End_year_analyses, output_folder, Radiation_Data)
    
    return()

if __name__== "__main__":
    
    # Do not show warnings
    warnings.filterwarnings('ignore')    
    
    # open json file
    with open(sys.argv[1]) as f:
        datastore = f.read()
    obj = json.loads(datastore)  
    inputs = obj["Inputs"][0]
    
    # Set Variables
    Start_year_analyses = inputs["Start_year"]
    End_year_analyses = inputs["End_year"]
    output_folder = inputs["Output_folder"]  
    try:
        Radiation_Data = inputs["Radiation_Source"]   
    except:
        Radiation_Data = "KNMI"   
        
    # run code
    main(Start_year_analyses, End_year_analyses, output_folder, Radiation_Data)
