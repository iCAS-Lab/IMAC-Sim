
############################################################
#                                                          #
#          2023 Md Hasibul Amin. All rights reserved.      #
#                      ma77@email.sc.edu                   #
#                                                          #
############################################################

import random
import numpy as np
def mapLayer(layer1,layer2, LayerNUM,hpar,vpar,metal,T,H,L,W,D,eps,rho,weight_var,data_dir,spice_dir):  
    f=open(spice_dir+'/'+'layer'+str(LayerNUM)+".sp", "w")
    g=open(data_dir+'/'+'posweight'+str(LayerNUM)+".txt", "r")
    n=1;
    m=1;
    cell = layer1+1
    f.write(".SUBCKT layer"+ str(LayerNUM)+" vdd vss 0 ")

    for i in range(layer1):
        i2=i+1
        f.write("in%d "%i2)
	
    for i in range(layer2):
        i2=i+1
        f.write("out%d "%i2)
    i=1
    f.write("\n\n**********Non-Negative Weighted Array****************\n")
    for l in g:
        if (float(l)!=0):
            if (m < layer2+1):
                f.write("Rwpos%d_%d in%d_%d sp%d_%d %f\n"% (n,m,n,m,n,m,float(l)))
                m+=1;
            else:
                n+=1;
                m=1;
                if (n == int(cell*i/hpar+min((cell%hpar)/i,1)+1)):
                    i+=1
                f.write("Rwpos%d_%d in%d_%d sp%d_%d %f\n"% (n,m,n,m,n,m,float(l)))
                m+=1;
        else:
            m+=1;
    f.write("\n\n**********Negative Weighted Array****************\n\n")
    n=1;
    m=1;
    i=1;
    g.close()
    h=open(data_dir+'/'+'negweight'+str(LayerNUM)+".txt", "r")
    for l in h:
        if (float(l)!=0):
            if (m < layer2+1):
                f.write("Rwneg%d_%d in%d_%d sn%d_%d %f\n"% (n,m,n,m,n,m,float(l)))
                m+=1;
            else:
                n+=1;
                m=1;
                if (n == int(cell*i/hpar+min((cell%hpar)/i,1)+1)):
                    i+=1
                f.write("Rwneg%d_%d in%d_%d sn%d_%d %f\n"% (n,m,n,m,n,m,float(l)))
                m+=1;
        else:
            m+=1;
			

    h.close()
    f.write("\n\n**********Positive Biases****************\n\n")
    m=1;
    a=open(data_dir+'/'+'posbias'+str(LayerNUM)+".txt", "r")
    for l in a:
        if (float(l)!=0):
            f.write("Rbpos%d vd%d sp%d_%d %f\n"% (m,m,layer1+1,m,float(l)))
            m+=1;
        else:
            m+=1;
    a.close()


    f.write("\n\n**********Negative Biases****************\n\n")
    m=1;
    b=open(data_dir+'/'+'negbias'+str(LayerNUM)+".txt", "r")
    for l in b:
        if (float(l)!=0):
            f.write("Rbneg%d vd%d sn%d_%d %f\n"% (m,m,layer1+1,m,float(l)))
            m+=1;
        else:
            m+=1;
    b.close()


    f.write("\n\n**********Parasitic Resistances for input Lines****************\n\n")
    l0 = 39e-9
    d = metal
    p=0.25
    R=0.3
    alpha = l0*R/(d*(1-R))
    dsur_scatt = 0.75*(1-p)*l0/metal
    dgrain_scatt = pow((1-3*alpha/2+3*pow(alpha,2)-3*pow(alpha,3)*np.log(1+1/alpha)),-1)
    rho_new = rho * (dsur_scatt + dgrain_scatt)
    parasitic_res = rho_new*L/(metal*T)
    for i in range(cell):
        p=1
        for j in range(layer2):
            if (i == layer1):
                if (j == 0):
                    f.write("Rbias%d vdd vd%d %f\n"% (j+1,j+1,parasitic_res))
                elif (j == int(layer2*p/vpar+min((layer2%vpar)/p,1))):
                    f.write("Rbias%d vdd vd%d %f\n"% (j+1,j+1,parasitic_res))
                    p+=1
                else:
                    f.write("Rbias%d vd%d vd%d %f\n"% (j+1,j,j+1,parasitic_res))
            else:
                if (j == 0):
                    f.write("Rin%d_%d in%d in%d_%d %f\n"% (i+1,j+1,i+1,i+1,j+1,parasitic_res))
                elif (j == int(layer2*p/vpar+min((layer2%vpar)/p,1))):
                    f.write("Rin%d_%d in%d in%d_%d %f\n"% (i+1,j+1,i+1,i+1,j+1,parasitic_res))
                    p+=1
                else:
                    f.write("Rin%d_%d in%d_%d in%d_%d %f\n"% (i+1,j+1,i+1,j,i+1,j+1,parasitic_res))

		
    '''
    f.write("\n\n**********Parasitic Capacitances for Input Lines****************\n\n")
    for i in range((layer1+2)/2):
        if (i==0):
        parasitic_cap = 0.5*(1.15*(metal/H)+2.8*(pow((T/H),0.222)));
        for j in range(layer1+1):
            if (i!=j):
                Wij = W*abs(i-j)
                parasitic_cap = parasitic_cap + (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/Wij),1.34))
            else:
                parasitic_cap = parasitic_cap + (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/(W*i)),1.34)) - (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/(W*(layer1-i+1))),1.34))
            #f.write("R%d in%d in0%d 1k\n"% (i+1,i+1,i+1))
            parasitic_cap_final = eps*parasitic_cap*W*1e15
            for j in range(layer2):
                f.write("C%d_%d in%d_%d 0 %ff\n"% (i+1,j+1,i+1,j+1,parasitic_cap_final))
                if ((layer1+1)%2==0 or i!=(layer1)/2):
                    if (i==0):
                        #f.write("R%d vdd vdd0 1k\n"% (layer1+1-i))
                        f.write("Cbias%d vd%d 0 %ff\n"% (j+1,j+1,parasitic_cap_final))
                    else:
                        #f.write("R%d in%d in0%d 1k\n"% (layer1+1-i,layer1+1-i,layer1+1-i))
                        f.write("C%d_%d in%d_%d 0 %ff\n"% (layer1+1-i,j+1,layer1+1-i,j+1,parasitic_cap_final))
    '''

    f.write("\n\n**********Parasitic Resistances for sp1 and sn1 Lines****************\n\n")
    #rho = 1.9e-8
    parasitic_res = rho_new*L/(metal*T)
    p=1
    for i in range(cell):
        for j in range(layer2):
            if (i == int(cell*p/hpar+min((cell%hpar)/p,1)-1)):
                if (i == layer1):
                    f.write("Rsp%d_%d sp%d_%d sp%d_p%d %f\n"% (i+1,j+1,i+1,j+1,j+1,p,parasitic_res))
                    f.write("Rsn%d_%d sn%d_%d sn%d_p%d %f\n"% (i+1,j+1,i+1,j+1,j+1,p,parasitic_res))
                else:
                    f.write("Rsp%d_%d sp%d_%d sp%d_p%d %f\n"% (i+1,j+1,i+1,j+1,j+1,p,parasitic_res))
                    f.write("Rsn%d_%d sn%d_%d sn%d_p%d %f\n"% (i+1,j+1,i+1,j+1,j+1,p,parasitic_res))
                    if (j == layer2-1):
                        p+=1;
            else:
                f.write("Rsp%d_%d sp%d_%d sp%d_%d %f\n"% (i+1,j+1,i+1,j+1,i+2,j+1,parasitic_res))
                f.write("Rsn%d_%d sn%d_%d sn%d_%d %f\n"% (i+1,j+1,i+1,j+1,i+2,j+1,parasitic_res))

    '''
    f.write("\n\n**********Parasitic Capacitances for sp1 and sn1 Lines****************\n\n")
    #D = 36*lambda_tech
    parasitic_cap = 0.5*(1.15*(metal/H)+2.8*(pow((T/H),0.222)))
    parasitic_cap = parasitic_cap + (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/D),1.34))
    parasitic_cap_final = eps*parasitic_cap*W*1e15
    p=1
    for i in range(cell):
        for j in range(layer2):
            if (i== cell*p/hpar+min((cell%hpar)/p,1)-1):
                if (i == layer1):
                    f.write("Csp%d_%d sp%d_p%d 0 %ff\n"% (i+1,j+1,j+1,p,parasitic_cap_final))
                    f.write("Csn%d_%d sn%d_p%d 0 %ff\n"% (i+1,j+1,j+1,p,parasitic_cap_final))
                else:
                    f.write("Csp%d_%d sp%d_p%d 0 %ff\n"% (i+1,j+1,j+1,p,parasitic_cap_final))
                    f.write("Csn%d_%d sn%d_p%d 0 %ff\n"% (i+1,j+1,j+1,p,parasitic_cap_final))
                    if (j == layer2-1):
                        p+=1
                        f.write("\n**********Partition %d****************\n"%p)
            else:
                f.write("Csp%d_%d sp%d_%d 0 %ff\n"% (i+1,j+1,i+2,j+1,parasitic_cap_final))
                f.write("Csn%d_%d sn%d_%d 0 %ff\n"% (i+1,j+1,i+2,j+1,parasitic_cap_final))
    '''



    f.write("\n\n**********Weight Differntial Op-AMPS and Connecting Resistors****************\n\n")
    for ii in range(hpar):
        for jj in range(layer2):
            f.write("XDIFFw%d_p%d sp%d_p%d sn%d_p%d xin%d_%d diff%d\n"% (jj+1,ii+1,jj+1,ii+1,jj+1,ii+1,jj+1,ii+1,LayerNUM))
            f.write("Rconn%d_p%d xin%d_%d xin%d 1m\n"% (jj+1,ii+1,jj+1,ii+1,jj+1))


    f.write("\n\n**********neurons****************\n\n")	
    for i in range(layer2):
        j=i+1;
        f.write("Xsig%d xin%d out%d vdd 0 neuron\n"% (j,j,j))
		
    m=1;
    
    
    f.write(".ENDS layer"+ str(LayerNUM))
    f.close()
