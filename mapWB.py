
############################################################
#                                                          #
#          2023 Md Hasibul Amin. All rights reserved.      #
#                      ma77@email.sc.edu                   #
#                                                          #
############################################################

import math
import numpy as np
import csv



def mapWB(layernum,rlow,rhigh,nodes,data_dir):
    for i in range(layernum-1):
        j=i+1
        weight=np.genfromtxt(data_dir+'/'+'W'+str(j)+'.csv',delimiter=',')
        w_flat=np.reshape(weight,nodes[i]*nodes[i+1])
        print(w_flat)
        weight_w=open('data/W'+str(j)+'.txt', "w")
        for k in range(len(w_flat)):
            x=float(w_flat[k])
            if (str(x)!='nan'):
                weight_w.write("%f\n"%(float(w_flat[k])))
        weight_w.close()
        
        f=open(data_dir+'/'+'W'+str(j)+'.txt',"r")
        wp=open(data_dir+'/'+'posweight'+str(j)+'.txt', "w")
        wn=open(data_dir+'/'+'negweight'+str(j)+'.txt', "w")
        for l in f:
            if (float(l)==1):
                wp.write("%f\n"%rlow)
                wn.write("%f\n"%rhigh)
            if (float(l)==-1):
                wp.write("%f\n"%rhigh)
                wn.write("%f\n"%rlow)
            if (float(l)==0):
                wp.write("%f\n"%rlow)
                wn.write("%f\n"%rlow)

            
        f.close()
        g=open(data_dir+'/'+'B'+str(j)+'.txt',"r")
        bp=open(data_dir+'/'+'posbias'+str(j)+'.txt', "w")
        bn=open(data_dir+'/'+'negbias'+str(j)+'.txt', "w")
        for l in g:
            if (float(l)==1):
                bp.write("%f\n"%rlow)
                bn.write("%f\n"%rhigh)
            if (float(l)==-1):
                bp.write("%f\n"%rhigh)
                bn.write("%f\n"%rlow)
            if (float(l)==0):
                bp.write("%f\n"%rlow)
                bn.write("%f\n"%rlow)

        g.close()
