#mapIMAC module connects the hidden layers and sets the configurations in the SPICE netlist

import random
import mapLayer
def mapIMAC(nodes,length,hpar,vpar,nlevels,vrange,metal,T,H,L,W,D,eps,rho,weight_var,testnum,data_dir,spice_dir,vdd,vss,tsampling):
    f=open(spice_dir+'/'+'classifier.sp', "w")
    f.write("*Fully-connected Classifier\n")
    f.write(".lib './models' ptm14hp\n")    #the transistor library can be changed here (The current format does not use transistor for the weighted array)
    for x in range(len(nodes)-1):		
        f.write('.include diff'+str(x+1)+'.sp\n')
    f.write(".include 'neuron.sp'\n")
    f.write(".option post\n")
    f.write(".op\n")
    f.write(".PARAM VddVal=%f\n"%vdd)
    f.write(".PARAM VssVal=%f\n"%vss)
    f.write(".PARAM tsampling=%fn\n"%tsampling)
    #f.write(".PARAM vrange=%f\n"%vrange)
    #f.write(".PARAM nlevels=%d\n"%nlevels)
    for i in range(len(nodes)-1):
        f.write(".include 'layer"+ str(i+1)+".sp'\n")
    for i in range(len(nodes)-1):
        mapLayer.mapLayer(nodes[i],nodes[i+1],i+1,hpar[i],vpar[i],nlevels[i],vrange,metal,T,H,L,W,D,eps,rho,weight_var,data_dir,spice_dir)
        f.write("Xlayer"+ str(i+1)+" vdd vss 0 ")
        for i2 in range(nodes[i]):
            if (i==0):
                f.write("in%d "%i2)
            else:
                f.write("out%d_%d "%(i,i2))
        for i3 in range(nodes[i+1]):
            if (i==len(nodes)-2):
                f.write("output%d "%i3)
            else:
                f.write("out%d_%d "%(i+1,i3))
        f.write("layer"+ str(i+1)+"\n\n\n")


    f.write("\n\n**********Input Test****************\n\n")
    c=open(data_dir+'/'+'data_sim.txt', "r")
    input_str = c.readlines()[0].split()
    input_num = [float(num) for num in input_str]
    for line in range(nodes[0]):
        f.write("v%d in%d 0 PWL( 0n 0 "%(line,line))
        for image in range(testnum):
            f.write("%fn %f %fn %f "%(image*tsampling+0.1,input_num[line+image*nodes[0]],(image+1)*tsampling,input_num[line+image*nodes[0]]))
        f.write(")\n")
    c.close()

	
    f.write("\n\n\nvss vss 0 DC VssVal\n")
    f.write("\n\n\nvdd vdd 0 DC VddVal\n")
    f.write(".TRAN 0.1n %d*tsampling\n"%(testnum))

    for i in range(testnum):
        f.write(".MEASURE TRAN pwr%d AVG POWER FROM=%d*tsampling+0.1n TO=%d*tsampling\n"%(i,i,i+1))

    for i in range(testnum):
        for j in range(nodes[len(nodes)-1]):
            f.write(".MEAS TRAN VOUT%d_%d FIND v(output%d) AT=%d*tsampling\n"%(j,i,j,i+1))
    f.write(".end")
    f.close() 
			
			
