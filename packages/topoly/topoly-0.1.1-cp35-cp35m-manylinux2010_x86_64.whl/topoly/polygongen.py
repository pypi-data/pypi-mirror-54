#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 12:49:58 2018

@author: bartosz
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import argparse

class Polygons(object):
    def __init__(self, no_of_sides, len_of_tail, no_of_polygons, 
                  is_loop_closed = False, print_with_index = True, 
                  file_prefix = 'lasso', folder_prefix = '', out_fmt = (3,3,5)):
        """
        Program creates random equilateral closed polygons (loops) with 
        random walk tails (lassos).                  
                                                                  
        Algorithm for generating random equilateral polygons based on 
        J. Cantarella \"A fast direct sampling algorithm for equilateral closed 
        polygons\". If you use this program, please, cite his article.  

        Parameters:
        int no_of_sides    -- number of sides of your loop
        int len_of_tail    -- number of vertices of your lasso tail; passing 0 
                              value lets you create simple loop, with no tail
        int no_of_polygons -- number of desired polygons, take into account your
                              free RAM cause for speed program creates polygons
                              in parallel.
        bool is_loop_closed   -- create extra loop vertice with same coordinates
                                 as first loop vertice (may be usefull for 
                                 visualisation)
        bool print_with_index -- output .xyz file will have format (index x y z)
                                 instead of (x y z)
        str file_prefix     -- prefix for created .xyz files
        str folder_prefix   -- prefix for created folder with .xyz files
        int,int,int out_fmt -- change space for numbers in names of created 
                               folder/files
                               first number is equal to number of digits 
                               of <no_of_sides>
                               second is equal to number of digits of 
                               <len_of_tail>
                               third is equal to number of digits of 
                               <file_num>

        program creates folder with format: 
        <folder_prefix>l<no_of_sides>_t<len_of_tail>
        and insade saves files with format:
        <file_prefix><file_num>.xyz        
        """
        self.nos = no_of_sides
        self.nop = no_of_polygons
        self.lot = len_of_tail
        self.file_prefix = file_prefix
        self.fold_prefix = folder_prefix
        self.is_loop_closed   = is_loop_closed
        self.print_with_index = print_with_index
        self.loop_fmt, self.tail_fmt, self.polyg_fmt = out_fmt
 
        # diagonal lengths
        self.vec_d     = np.zeros([self.nos-1, self.nop], order='F')
        # dihedral angles
        self.vec_theta = np.zeros([self.nos-2, self.nop], order='F')
        self.loop_coors = np.zeros([3, self.nos, self.nop], order='F')
        self.tail_coors = np.zeros([3, self.lot, self.nop], order='F')
        self.lasso_coors = None

        self.passed = 0
        self.failed = 0

        self.gen_diagonals()
        self.calc_loop_vertices()

        if self.is_loop_closed == True:
            self.close_polygon()
        if self.lot > 0:
            self.gen_tail()
            self.join_loop_tail()
        if self.lot == 0:
            self.lasso_coors = self.loop_coors

        self.export_lasso_xyz()
        
        
    def join_loop_tail(self):
        self.lasso_coors = np.hstack([self.loop_coors, self.tail_coors])

    def close_polygon(self):
        self.loop_coors = np.concatenate((self.loop_coors[:,:,:],
                        self.loop_coors[:,0,:].reshape(3,1,self.nop)), axis = 1)
    
    def gen_diagonals(self):
        for p in range(self.nop):
            while 1:
                while 1:
                    s               = np.zeros(self.nos-1)
                    # s[0] = 0 for numeration consistency with Canterella_2016
                    s[1:self.nos-2] = np.random.uniform(-1,1,self.nos-3)
                    s[self.nos-2]   = -np.sum(s)
                    if np.greater(np.abs(s[self.nos-2]), 1):
                        self.failed += 1
                    else:
                        break
                d = np.ones(self.nos-1)      
                # d[0] = 1 for numeration consistency with Canterella_2016
                # (also d[n-2] = 1)
                for i in range(1,self.nos-2): 
                    d[i] = d[i-1] + s[i]
                if np.any(np.less(d[:-1] + d[1:], 1)):
                    self.failed += 1
                else:
                    self.passed += 1
                    break
            theta = np.random.uniform(0,2*np.pi,self.nos-3)
            self.vec_d[:,p] = d
            self.vec_theta[1:,p] = theta
            # theta[0] = 0 for numeration consistency with Canterella_2016

    def calc_loop_vertices(self): # d1 = [x1, x2, x3]
        p0 = np.zeros([3,self.nop])
        p1 = np.vstack([np.ones([self.nop]).reshape([1,self.nop]), 
                         np.zeros([2,self.nop])])
        self.loop_coors[:,0,:] = p0
        self.loop_coors[:,1,:] = p1
        for i in range(2, self.nos):
            d2_len = self.vec_d[i-1,:]
            d1_len = self.vec_d[i-2,:]
            d1     = self.loop_coors[:,i-1,:]
            theta  = self.vec_theta[i-2,:]
            
            alpha, betha = self.rotate(d1)
            x   = (np.square(d1_len) - 1 + np.square(d2_len)) / (2 * d1_len)
            rho = np.sqrt(np.square(d2_len) - np.square(x))
            y   = rho * np.cos(theta)
            z   = rho * np.sin(theta)
            self.loop_coors[:,i,:] = self.unrotate([x,y,z],alpha,betha)

    def rotate(self,v): 
        # rotate vector v = [x,y,z] -> w = [d,0,0] (d = length of v)
        x,y,z = v
        #       | 1     0           0      |      | cos(betha) -sin(betha) 0 |
        #   A = | 0 cos(alpha) -sin(alpha) |  B = | sin(betha)  cos(betha) 0 |
        #       | 0 sin(alpha)  cos(alpha) |      |     0           0      1 |
        alpha = np.arctan2(-z,y)
        #       |            x                |
        #  Av = | y cos(alpha) - z sin(alpha) |
        #       | y sin(alpha) + z cos(alpha) |
        # third component equal to zero gives condition on angle alpha that 
        #  rotates v to the XY plane
        betha = np.arctan2( +z*np.sin(alpha) - y*np.cos(alpha), x )
        #       | x cos(betha) - sin(betha)[y cos(alpha) - z sin(alpha)] |
        # BAv = | z sin(betha) + cos(betha)[y cos(alpha) - z sin(alpha)] |
        #       |                         0                              |
        # second component equal to zero gives condition on angle betha that 
        # rotates Av to the x-axis
        return alpha, betha

    def unrotate(self,w,alpha,betha): 
        # unrotates vector rotated by B(betha)A(alpha)
        w = np.array(w)
        alpha = np.array(alpha)
        betha = np.array(betha)
        # A(-alpha)B(-betha)
        try: zero = np.zeros(len(alpha))#; one = np.ones(len(alpha))
        except: zero = 0#; one = 1
        # TRANSPOSED, BUT DOESN'T LOOK LIKE (bracket order)
        # transposition handled by np.einsum
        AB = np.array([[         np.cos(betha),               np.sin(betha),             zero      ],
                       [ -np.cos(alpha)*np.sin(betha),  np.cos(alpha)*np.cos(betha), np.sin(alpha) ],
                       [  np.sin(alpha)*np.sin(betha), -np.sin(alpha)*np.cos(betha), np.cos(alpha) ]])
        return np.einsum('ijk,jk->ik',AB,w)

    def gen_tail(self):
        fi    = np.random.uniform(0,2*np.pi,[self.lot, self.nop])
        theta = np.random.uniform(0,np.pi,[self.lot, self.nop])
        x = np.cos(fi) * np.sin(theta)
        y = np.sin(fi) * np.sin(theta)
        z = np.cos(theta)
        i = 0
        self.tail_coors[0,i,:] = x[i,:] + self.loop_coors[0,-1,:]
        self.tail_coors[1,i,:] = y[i,:] + self.loop_coors[1,-1,:]
        self.tail_coors[2,i,:] = z[i,:] + self.loop_coors[2,-1,:]
        for i in range(1,self.lot):
            self.tail_coors[0,i,:] = x[i,:] + self.tail_coors[0,i-1,:]
            self.tail_coors[1,i,:] = y[i,:] + self.tail_coors[1,i-1,:]
            self.tail_coors[2,i,:] = z[i,:] + self.tail_coors[2,i-1,:]


    def export_lasso_xyz(self):
        if self.lot == 0:
            folder = '{}l{:0{:d}d}/'.format(self.fold_prefix, 
                                             self.nos, self.loop_fmt)
        folder = '{}l{:0{:d}d}_t{:0{:d}d}/'.format(self.fold_prefix, 
                              self.nos, self.loop_fmt, self.lot, self.tail_fmt)
        try: os.mkdir(folder)
        except: pass

        if self.print_with_index:
            for polyg in range(self.nop):
                with open(folder + '/{}{:0{:d}d}.xyz'.format(self.file_prefix, 
                                             polyg, self.polyg_fmt),'w') as f:        
                    for node in range(np.shape(self.lasso_coors)[1]):
                        f.write('{:2d} {:10f} {:10f} {:10f}\n'.format(node+1, 
                                 self.lasso_coors[0, node, polyg], 
                                 self.lasso_coors[1, node, polyg], 
                                 self.lasso_coors[2, node, polyg] ))
        else:
            for polyg in range(self.nop):
                with open(folder + '/{}{:0{:d}d}.xyz'.format(self.file_prefix, 
                                             polyg, self.polyg_fmt),'w') as f:
                    for node in range(np.shape(self.lasso_coors)[1]):
                        f.write('{:10f} {:10f} {:10f}\n'.format(
                                 self.lasso_coors[0, node, polyg], 
                                 self.lasso_coors[1, node, polyg], 
                                 self.lasso_coors[2, node, polyg]))


