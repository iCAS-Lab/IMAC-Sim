
############################################################
#                                                          #
#          2023 Md Hasibul Amin. All rights reserved.      #
#                      ma77@email.sc.edu                   #
#                                                          #
############################################################

import random
import numpy as np

def mapLayer(layer1,layer2, LayerNUM,hpar,vpar,metal,T,H,L,W,D,eps,rho,weight_var,data_dir,spice_dir): 

    # updating the resistivity for specific technology node
    l0 = 39e-9 # Mean free path of electrons in Cu
    d = metal # average grain size, equal to wire width
    p=0.25 # specular scattering fraction
    R=0.3 # probability for electron to reflect at the grain boundary
    alpha = l0*R/(d*(1-R)) # parameter for MS model
    dsur_scatt = 0.75*(1-p)*l0/metal # surface scattering
    dgrain_scatt = pow((1-3*alpha/2+3*pow(alpha,2)-3*pow(alpha,3)*np.log(1+1/alpha)),-1) # grain boundary scattering
    rho_new = rho * (dsur_scatt + dgrain_scatt) # new resistivity
    
    layer_w=open(spice_dir+'/'+'layer'+str(LayerNUM)+".sp", "w") # open the layer subcircuit file for writing
    layer1_wb = layer1+1 # number of bitcell in a row including weights and bias
    
    layer_w.write(".SUBCKT layer"+ str(LayerNUM)+" vdd vss 0 ")

    for i in range(layer1):
        layer_w.write("in%d "%(i+1))
	
    for i in range(layer2):
        layer_w.write("out%d "%(i+1))

    # writing the circuit for positive line weights
    layer_w.write("\n\n**********Positive Weighted Array**********\n")
    posw_r=open(data_dir+'/'+'posweight'+str(LayerNUM)+".txt", "r") # read the positive line conductances
    n_hpar=1 # horizontal partition number
    c=1 # column number
    r=1 # row number
    for line in posw_r:
        if (float(line)!=0):
            if (r < layer2+1):
                layer_w.write("Rwpos%d_%d in%d_%d sp%d_%d %f\n"% (c,r,c,r,c,r,float(line)))
                r+=1;
            else:
                c+=1;
                r=1;
                if (c == int(layer1_wb*n_hpar/hpar+min((layer1_wb%hpar)/n_hpar,1)+1)):
                    n_hpar+=1
                layer_w.write("Rwpos%d_%d in%d_%d sp%d_%d %f\n"% (c,r,c,r,c,r,float(line)))
                r+=1;
        else:
            r+=1;
    posw_r.close()
    
    
    # writing the circuit for negative line weights
    layer_w.write("\n\n**********Negative Weighted Array**********\n\n")
    negw_r=open(data_dir+'/'+'negweight'+str(LayerNUM)+".txt", "r")
    n_hpar=1 # horizontal partition number
    c=1 # column number
    r=1 # row number
    for line in negw_r:
        if (float(line)!=0):
            if (r < layer2+1):
                layer_w.write("Rwneg%d_%d in%d_%d sn%d_%d %f\n"% (c,r,c,r,c,r,float(line)))
                r+=1;
            else:
                c+=1;
                r=1;
                if (c == int(layer1_wb*n_hpar/hpar+min((layer1_wb%hpar)/n_hpar,1)+1)):
                    n_hpar+=1
                layer_w.write("Rwneg%d_%d in%d_%d sn%d_%d %f\n"% (c,r,c,r,c,r,float(line)))
                r+=1;
        else:
            r+=1;	
    negw_r.close()
    
    
    # writing the circuit for positive line biases
    layer_w.write("\n\n**********Positive Biases**********\n\n")
    posb_r=open(data_dir+'/'+'posbias'+str(LayerNUM)+".txt", "r")
    r=1;
    for line in posb_r:
        if (float(line)!=0):
            layer_w.write("Rbpos%d vd%d sp%d_%d %f\n"% (r,r,layer1_wb,r,float(line)))
            r+=1;
        else:
            r+=1;
    posb_r.close()
    
    
    # writing the circuit for negative line biases
    layer_w.write("\n\n**********Negative Biases**********\n\n")
    negb_r=open(data_dir+'/'+'negbias'+str(LayerNUM)+".txt", "r")
    r=1;
    for line in negb_r:
        if (float(line)!=0):
            layer_w.write("Rbneg%d vd%d sn%d_%d %f\n"% (r,r,layer1_wb,r,float(line)))
            r+=1;
        else:
            r+=1;
    negb_r.close()
    
    
    # writing the circuit for vertical line parasitic resistances
    layer_w.write("\n\n**********Parasitic Resistances for Vertical Lines**********\n\n")
    parasitic_res = rho_new*W/(metal*T)
    for i in range(layer1_wb):
        n_vpar=1 # vertical partition number
        c=i+1 # column number
        for j in range(layer2):
            r=j+1 # row number
            if (i == layer1): # only for the bias line
                if (j == 0):
                    layer_w.write("Rbias%d vdd vd%d %f\n"% (r,r,parasitic_res))
                elif (j == int(layer2*n_vpar/vpar+min((layer2%vpar)/n_vpar,1))):
                    layer_w.write("Rbias%d vdd vd%d %f\n"% (r,r,parasitic_res))
                    n_vpar+=1
                else:
                    layer_w.write("Rbias%d vd%d vd%d %f\n"% (r,j,r,parasitic_res))
            
            else: # the input connected vertical lines
                if (j == 0):
                    layer_w.write("Rin%d_%d in%d in%d_%d %f\n"% (c,r,c,c,r,parasitic_res))
                elif (j == int(layer2*n_vpar/vpar+min((layer2%vpar)/n_vpar,1))):
                    layer_w.write("Rin%d_%d in%d in%d_%d %f\n"% (c,r,c,c,r,parasitic_res))
                    n_vpar+=1
                else:
                    layer_w.write("Rin%d_%d in%d_%d in%d_%d %f\n"% (c,r,c,j,c,r,parasitic_res))
    
    #uncomment the following for adding the vertical line parasitic capacitances (commented for saving simulation time)
    '''
    # writing the circuit for vertical line parasitic capacitances
    layer_w.write("\n\n**********Parasitic Capacitances for Vertical Lines**********\n\n")
    for i in range(int((layer1_wb+1)/2)):
        c=i+1 # column number
        if (i==0):
            parasitic_cap = 0.5*(1.15*(metal/H)+2.8*(pow((T/H),0.222)));
            #calculating the parasitic capacitance for the first and last line considering the effect of all other lines
            for j in range(layer1_wb):
                if (i!=j):
                    Wij = W*abs(i-j)
                    parasitic_cap = parasitic_cap + (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/Wij),1.34))
                    parasitic_cap_final = eps*parasitic_cap*W*1e15
            # writing the first and last line capacitances
            for j in range(layer2):
                r=j+1
                layer_w.write("C%d_%d in%d_%d 0 %ff\n"% (c,r,c,r,parasitic_cap_final))
                layer_w.write("Cbias%d vd%d 0 %ff\n"% (r,r,parasitic_cap_final))
        else:
            # updating the parasitic capacitance based on line position
            parasitic_cap = parasitic_cap + (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/(W*i)),1.34)) - (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/(W*(layer1-i+1))),1.34))
            parasitic_cap_final = eps*parasitic_cap*W*1e15
            # writing the line capacitances
            for j in range(layer2):
                r=j+1 # row number
                layer_w.write("C%d_%d in%d_%d 0 %ff\n"% (c,r,c,r,parasitic_cap_final))
                if ((layer1_wb%2)!=0 and i==int(layer1/2)):
                    continue
                layer_w.write("C%d_%d in%d_%d 0 %ff\n"% (layer1+1-i,r,layer1+1-i,r,parasitic_cap_final))
    '''
    
    
    # writing the circuit for horizontal line parasitic resistances
    layer_w.write("\n\n**********Parasitic Resistances for I+ and I- Lines****************\n\n")
    parasitic_res = rho_new*L/(metal*T)
    n_hpar=1 # horizontal partition number
    for i in range(layer1_wb):
        c=i+1 # column number
        for j in range(layer2):
            r=j+1 # row number
            if (i == int(layer1_wb*n_hpar/hpar+min((layer1_wb%hpar)/n_hpar,1)-1)):
                if (i == layer1):
                    layer_w.write("Rsp%d_%d sp%d_%d sp%d_p%d %f\n"% (c,r,c,r,r,n_hpar,parasitic_res))
                    layer_w.write("Rsn%d_%d sn%d_%d sn%d_p%d %f\n"% (c,r,c,r,r,n_hpar,parasitic_res))
                else:
                    layer_w.write("Rsp%d_%d sp%d_%d sp%d_p%d %f\n"% (c,r,c,r,r,n_hpar,parasitic_res))
                    layer_w.write("Rsn%d_%d sn%d_%d sn%d_p%d %f\n"% (c,r,c,r,r,n_hpar,parasitic_res))
                    if (j == layer2-1):
                        n_hpar+=1;
            else:
                layer_w.write("Rsp%d_%d sp%d_%d sp%d_%d %f\n"% (c,r,c,r,c+1,r,parasitic_res))
                layer_w.write("Rsn%d_%d sn%d_%d sn%d_%d %f\n"% (c,r,c,r,c+1,r,parasitic_res))

    
    #uncomment the following for adding the horizontal line parasitic capacitances (commented for saving simulation time)
    '''
    # writing the circuit for horizontal line parasitic capacitances
    layer_w.write("\n\n**********Parasitic Capacitances for I+ and I- Lines****************\n\n")
    parasitic_cap = 0.5*(1.15*(metal/H)+2.8*(pow((T/H),0.222)))
    parasitic_cap = parasitic_cap + (0.03*(metal/H)+0.83*(T/H)-0.07*(pow((T/H),0.222)))*(pow((H/D),1.34))
    parasitic_cap_final = eps*parasitic_cap*W*1e15
    n_hpar=1
    for i in range(layer1_wb):
        c=i+1 # column number
        for j in range(layer2):
            r=j+1 # row number
            if (i == int(layer1_wb*n_hpar/hpar+min((layer1_wb%hpar)/n_hpar,1)-1)):
                if (i == layer1):
                    layer_w.write("Csp%d_%d sp%d_p%d 0 %ff\n"% (c,r,r,n_hpar,parasitic_cap_final))
                    layer_w.write("Csn%d_%d sn%d_p%d 0 %ff\n"% (c,r,r,n_hpar,parasitic_cap_final))
                else:
                    layer_w.write("Csp%d_%d sp%d_p%d 0 %ff\n"% (c,r,r,n_hpar,parasitic_cap_final))
                    layer_w.write("Csn%d_%d sn%d_p%d 0 %ff\n"% (c,r,r,n_hpar,parasitic_cap_final))
                    if (j == layer2-1):
                        n_hpar+=1
            else:
                layer_w.write("Csp%d_%d sp%d_%d 0 %ff\n"% (c,r,c+1,r,parasitic_cap_final))
                layer_w.write("Csn%d_%d sn%d_%d 0 %ff\n"% (c,r,c+1,r,parasitic_cap_final))
    
    '''
    
    
    # writing the circuit for Op-AMPS and connecting resistors
    layer_w.write("\n\n**********Weight Differntial Op-AMPS and Connecting Resistors****************\n\n")
    for i in range(hpar):
        for j in range(layer2):
            layer_w.write("XDIFFw%d_p%d sp%d_p%d sn%d_p%d nin%d_%d diff%d\n"% (j+1,i+1,j+1,i+1,j+1,i+1,j+1,i+1,LayerNUM))
            layer_w.write("Rconn%d_p%d nin%d_%d nin%d 1m\n"% (j+1,i+1,j+1,i+1,j+1))
    
    
    
    # writing the circuit for neurons
    layer_w.write("\n\n**********neurons****************\n\n")	
    for i in range(layer2):
        layer_w.write("Xsig%d nin%d out%d vdd 0 neuron\n"% (i+1,i+1,i+1))
    
    
    layer_w.write(".ENDS layer"+ str(LayerNUM))
    layer_w.close()
