
############################################################
#                                                          #
#          2023 Md Hasibul Amin. All rights reserved.      #
#                      ma77@email.sc.edu                   #
#                                                          #
############################################################

import math
import numpy as np
import csv
import random


def mapWB(layernum,rlow,rhigh,nodes,data_dir,weight_var):
    for i in range(layernum-1):
        j=i+1
        weight=np.genfromtxt(data_dir+'/'+'W'+str(j)+'.csv',delimiter=',')
        w_flat=np.reshape(weight,nodes[i]*nodes[i+1])
        weight_w=open('data/W'+str(j)+'.txt', "w")
        for k in range(len(w_flat)):
            x=float(w_flat[k])
            if (str(x)!='nan'):
                weight_w.write("%f\n"%(float(w_flat[k])))
        weight_w.close()
        
        bias=np.genfromtxt(data_dir+'/'+'B'+str(j)+'.csv',delimiter=',')
        b_flat=np.reshape(bias,nodes[i+1])
        bias_w=open('data/B'+str(j)+'.txt', "w")
        for k in range(len(b_flat)):
            x=float(b_flat[k])
            if (str(x)!='nan'):
                bias_w.write("%f\n"%(float(b_flat[k])))
        bias_w.close()
        
        f=open(data_dir+'/'+'W'+str(j)+'.txt',"r")
        wp=open(data_dir+'/'+'posweight'+str(j)+'.txt', "w")
        wn=open(data_dir+'/'+'negweight'+str(j)+'.txt', "w")
        for l in f:
            if (float(l)==1):
                wp.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
                wn.write("%f\n"%(rhigh+random.uniform(-1*weight_var*rhigh/100,weight_var*rhigh/100)))
            if (float(l)==-1):
                wp.write("%f\n"%(rhigh+random.uniform(-1*weight_var*rhigh/100,weight_var*rhigh/100)))
                wn.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
            if (float(l)==0):
                wp.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
                wn.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
        wp.close()
        wn.close()
        f.close()
        
        g=open(data_dir+'/'+'B'+str(j)+'.txt',"r")
        bp=open(data_dir+'/'+'posbias'+str(j)+'.txt', "w")
        bn=open(data_dir+'/'+'negbias'+str(j)+'.txt', "w")
        for l in g:
            if (float(l)==1):
                bp.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
                bn.write("%f\n"%(rhigh+random.uniform(-1*weight_var*rhigh/100,weight_var*rhigh/100)))
            if (float(l)==-1):
                bp.write("%f\n"%(rhigh+random.uniform(-1*weight_var*rhigh/100,weight_var*rhigh/100)))
                bn.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
            if (float(l)==0):
                bp.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
                bn.write("%f\n"%(rlow+random.uniform(-1*weight_var*rlow/100,weight_var*rlow/100)))
        bp.close()
        bn.close()
        g.close()
