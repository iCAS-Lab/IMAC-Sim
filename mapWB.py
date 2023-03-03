import math
import numpy as np
import csv



def mapWB(layernum,rp,rap,nodes,data_dir):
    for i in range(layernum-1):
        j=i+1
        with open(data_dir+'/'+'W'+str(j)+'.txt', 'r') as r, open(data_dir+'/'+'W_nocomma'+str(j)+'.txt', 'w') as w:
            for num, line in enumerate(r):
                if num >= 0:
                    newline = line[:-2] + "\n" if "\n" in line else line[:-1]
                else:
                    newline = line
                w.write(newline)
        a=np.genfromtxt(data_dir+'/'+'W_nocomma'+str(j)+'.txt',delimiter=',')
        b=np.reshape (a,nodes[i]*nodes[i+1])
        g=open('data/W'+str(j)+'.txt', "w")
        for jj in range(len(b)):
            x=float(b[jj])
            if (str(x)!='nan'):
                g.write("%f\n"%(float(b[jj])))	
        g.close()
        f=open(data_dir+'/'+'W'+str(j)+'.txt',"r")
        wp=open(data_dir+'/'+'posweight'+str(j)+'.txt', "w")
        wn=open(data_dir+'/'+'negweight'+str(j)+'.txt', "w")
        for l in f:
            if (float(l)==1):
                wp.write("%f\n"%rp)
                wn.write("%f\n"%rap)
            if (float(l)==-1):
                wp.write("%f\n"%rap)
                wn.write("%f\n"%rp)
            if (float(l)==0):
                wp.write("%f\n"%rp)
                wn.write("%f\n"%rp)

            
        f.close()
        g=open(data_dir+'/'+'B'+str(j)+'.txt',"r")
        bp=open(data_dir+'/'+'posbias'+str(j)+'.txt', "w")
        bn=open(data_dir+'/'+'negbias'+str(j)+'.txt', "w")
        for l in g:
            if (float(l)==1):
                bp.write("%f\n"%rp)
                bn.write("%f\n"%rap)
            if (float(l)==-1):
                bp.write("%f\n"%rap)
                bn.write("%f\n"%rp)
            if (float(l)==0):
                bp.write("%f\n"%rp)
                bn.write("%f\n"%rp)

        g.close()


