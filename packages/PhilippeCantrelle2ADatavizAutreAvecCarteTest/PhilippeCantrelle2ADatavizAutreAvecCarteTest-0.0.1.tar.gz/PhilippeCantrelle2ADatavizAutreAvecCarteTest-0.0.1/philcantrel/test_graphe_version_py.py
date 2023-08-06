#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#version fichier py

import pandas as pd

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

import unittest
import numpy as np
from module_carte import *

class Test(unittest.TestCase):
    
    """On teste plot_geo_time_value"""
    
    def test_plot_geo_time_value(self):

    # on regarde les valeurs renvoyees par test_plot_geo_time_value 
    # pour i et j, si elles ne valent pas 1 et 1 il y a un probleme

        (a,b) = plot_geo_time_value(x=df['LLX'],y=df['LLY'], df = pd.read_csv("df_metro.csv", sep=",", encoding = 'latin-1'),lim_metropole = [-5, 10, 41, 52],filename = 'yourfilename.pdf')
        liste = [a,b]
        self.assertEqual(liste,[1,1])
            
if __name__ == '__main__':
    unittest.main()

