#!/usr/bin/env python
from polygongen import Polygons
import numpy as np                                                               
import os
import sys                                                                       
                                                                                 
def check_dist(filename, folder, eps = 0.0001):                                                         
    # takes .xyz file and calculates distances between residues                      
    # returns 1 if they are close do 1, otherwise returns 0         
    f     = np.loadtxt(folder +'/'+ filename)[:,1:]                                             
    vec   = f[1:,:]-f[:-1,:]                                                       
    dists = np.square(vec).sum(axis=1)                                           
    res   = np.logical_and(np.all(1-eps < dists), np.all(dists < 1+eps))           
    return int(res)                                                              
                                                                                 
if __name__ == '__main__':
    print('Testing polygongen') 
    res = 0
    # basic use: generate 3 lassos with looplength = 10 and taillength = 5
    Polygons(10, 5, 3)

    # output is in folder 'l010_t005', files 'lasso00000.xyz' to 'lasso00002.xyz'
    folder      = 'l010_t005'
    file_prefix = 'lasso'
    for filename in os.listdir(folder):
        if filename.startswith(file_prefix):
            res = res + check_dist(filename, folder)
    
    # formats can be changed
    Polygons(10, 5, 3, folder_prefix='test_', file_prefix='a_', out_fmt=(2,1,1)) 

    # output is in folder 'l10_t5', files 'a_0.xyz' to 'a_2.xyz'
    folder      = 'test_l10_t5'
    file_prefix = 'a'
    for filename in os.listdir(folder):
        if filename.startswith(file_prefix):
            res = res + check_dist(filename, folder)
    try: 
        assert res == 6
        print('Polygongen test passed :)')
    except: 
        print('Polygongen test failed :(')
            
