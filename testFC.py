############################################################
#                                                          #
#                    2022 Md Hasibul Amin                  #
#                    ma77@email.sc.edu                     #
#                                                          #
############################################################
import re
import os
import time
import math
import random
import mapFC
import mapWB
import numpy as np
import csv

start = time.time()

# list of inputs start
data_dir='data'
spice_dir='spice'
dataset_file='test_data.csv'
label_file='test_labels.csv'
noise=0.000   #maximum noise amplitude in Volt
weight_var=0.0 #variation in the resistance of the synapses in Kohms
testnum=1
testnum_per_batch=1
firstimage=0 #start the test inputs from this image /500
Vdd=0.8
nodes=[400,120,84,10] #Network Topology, which should be similar to what is defined in MATLAB
hpar=[13,4,3]
vpar=[4,3,1]
gain=[30,30,10]
tech_node=9e-9
metal=3*tech_node #Metal width
T=22e-9 #Metal thickness
H=20e-9 #Inter metal layer spacing
L=12*tech_node #length of the bitcell
W=15*tech_node #width of the bitcell
D=5*tech_node #distance between sp and sn lines
eps = 20*8.854e-12 #permittivity of oxide
rho = 1.9e-8 #resistivity of metal
# list of inputs end

# device properties start
# lMTJ=50e-9
# wMTJ=30e-9
# RA=1e-11
# TMR=200
# AreaMTJ=(math.pi)*lMTJ*wMTJ/4
# rp=RA/AreaMTJ
rp=5e3
print(rp)
# rap=(1+(TMR/100.0))*rp
rap=15e3
print(rap)
# device properties end

# function to change the input voltage in the neuron.sp file, which includes the probabilistic activation function
def update_neuron (rp,rap):
    ff=open(spice_dir+'/'+'neuron.sp', "r+")
    i=0
    data= ff.readlines()
    for line in data:
        i+=1
        if 'Rlow' in line:
            data[i-1]='Rlow in2 input ' + str(rp) +'\n'
        if 'Rhigh' in line:
            data[i-1]='Rhigh input out ' + str(rap) +'\n'

    ff.seek(0)
    ff.truncate()
    ff.writelines(data)
    ff.close()


def update_diff (gain, LayerNUM):
    name=spice_dir+'/'+'diff{}.sp'.format(LayerNUM)
    ff=open(name, "r+")
    i=0
    data= ff.readlines()
    for line in data:
        i+=1
        if 'R3' in line:
            data[i-1]='R3 n1 out ' + str(gain) +'k\n'
        if 'R4' in line:
            data[i-1]='R4 n2 0 ' + str(gain) +'k\n'
    ff.seek(0)
    ff.truncate()
    ff.writelines(data)
    ff.close()


#function to find the measured average voltage or power in the output text file genrated by SPICE(Specifically for MEAUSURE FROM-TO)
def findavg (line):
    i=0
    m=0
    while (m == 0):
        i+=1;
        if (line[i]=='='):
            s1=i+1;
        if (line[i]=='f'):
            s2=i-1;
            m=1;
        if (line[i]=='\n'):
            s2=i;
            m=1;
    volt=line[s1:s2]
    volt=volt.replace(" ","")
    volt=volt.replace("m","e-3")
    volt=volt.replace("u","e-6")
    volt=volt.replace("n","e-9")
    volt=volt.replace("p","e-12")
    volt=volt.replace("f","e-15")
    volt=volt.replace("k","e3")
    volt=volt.replace("x","e6")
    volt=volt.replace("g","e9")
    volt=volt.replace("t","e12")
    return volt

#function to find the measured voltage in the output2 text file genrated by SPICE (Specifically for MEASURE AT)
def findat (line):
    i=0
    m=0
    while (m == 0):
        i+=1;
        if (line[i]=='='):
            s1=i+1;
        if (line[i]=='w'):
            s2=i-1;
            m=1;
        if (line[i]=='\n'):
            s2=i;
            m=1;
    volt=line[s1:s2]
    volt=volt.replace(" ","")
    volt=volt.replace("m","e-3")
    volt=volt.replace("u","e-6")
    volt=volt.replace("n","e-9")
    volt=volt.replace("p","e-12")
    volt=volt.replace("f","e-15")
    volt=volt.replace("a","e-18")
    volt=volt.replace("k","e3")
    volt=volt.replace("x","e6")
    volt=volt.replace("g","e9")
    volt=volt.replace("t","e12")
    return volt

#dataset preprocessing
dataset = np.genfromtxt(data_dir+'/'+dataset_file,delimiter=',')
dataset_reshaped = np.reshape (dataset,4000000)
dataset_signed = np.sign(dataset_reshaped)

dataset_write = open(data_dir+'/'+'testinput.txt', "w")
for i in range(len(dataset_signed)):
    dataset_write.write("%f\n"%(float(dataset_signed[i])))	
dataset_write.close()

#label preprocessing
label = np.genfromtxt(data_dir+'/'+'test_labels.csv',delimiter=',')
label_reshaped = np.reshape (label,100000)
label_write = open(data_dir+'/'+'testlabel.txt', "w")
for i in range(len(label_reshaped)):
    label_write.write("%f\n"%(float(label_reshaped[i])))	
label_write.close()


f=open(data_dir+'/'+'testinput.txt', "r")   # testinput.text is the output of the MATLAB code, which includes the test images in the MNIST Dataset
f2=open(data_dir+'/'+'testlabel.txt', "r")  # testlabel.text is the output of the MATLAB code, which includes the labels of the test images in the MNIST Dataset
in_data=f.readlines()
label=f2.readlines()
length=len(nodes)
#update_neuron(rp,rap)
for i in range(len(nodes)-1):
    update_diff(gain[i],i+1)
mapWB.mapWB(length,rp,rap,nodes,data_dir)
batch=testnum//testnum_per_batch
image_num=0
testimage=firstimage
err=[]
powr_list=[]
pwr_list=[]
for ii in range(batch):
    out_list=[]
    out2_list=[]
    label_list=[]
    input_data=in_data[int(testimage*nodes[0]):int((testimage+testnum_per_batch)*nodes[0])]
    label_data=label[int(testimage*nodes[len(nodes)-1]):int((testimage+testnum_per_batch)*nodes[len(nodes)-1])]
    for item in label_data:
        label_list.append(float(item))
        g=open(data_dir+'/'+'singletestinput2.txt', "w")
        for j2 in range(int(testnum_per_batch*nodes[0])):	
            g.write("%f "%(float(input_data[j2])*Vdd))	
    g.close()
    mapFC.mapFC(nodes,length,hpar,vpar,metal,T,H,L,W,D,eps,rho,weight_var,testnum_per_batch,data_dir,spice_dir)
    os.system('hspice '+spice_dir+'/classifier.sp >'+spice_dir+'/output.txt')
    #os.system('hspice -i '+spice_dir+'/classifier.sp -o '+spice_dir+'/output.txt')
    h=open(spice_dir+'/'+'output.txt', "r")
    for l in h:
        if 'vout' in l:
            z=findat(l)
            out_list.append(z)
        if 'pwr' in l:
            z2=findavg(l)
            pwr_list.append(z2)
        if 'powr' in l:
            z3=findavg(l)
            powr_list.append(z3)
    for i in range(len(out_list)):
        out_list[i]=float(out_list[i])
    for i1 in range (testnum_per_batch):
        print(i1+image_num+1)
        print(label_list[nodes[len(nodes)-1]*i1:nodes[len(nodes)-1]*(i1+1)])
        err.append(int(0))
        list_max=max(out_list[nodes[len(nodes)-1]*i1:nodes[len(nodes)-1]*(i1+1)])
        print(out_list[nodes[len(nodes)-1]*i1:nodes[len(nodes)-1]*(i1+1)])
        print(list_max)
        for i2 in range (nodes[len(nodes)-1]):
            if (out_list[nodes[len(nodes)-1]*i1+i2]==list_max):    # the neuron generating maximum output value represents the corrosponding class
                out_list[nodes[len(nodes)-1]*i1+i2]=1.0
            else:
                out_list[nodes[len(nodes)-1]*i1+i2]=0.0
            if (err[i1+image_num]==0):
                if (out_list[nodes[len(nodes)-1]*i1+i2] != label_list[nodes[len(nodes)-1]*i1+i2]):
                    err[i1+image_num]=1
        print(out_list[nodes[len(nodes)-1]*i1:nodes[len(nodes)-1]*(i1+1)])
        print("Power consumption = %f"%float(powr_list[i1+image_num]))
        print("sum error= %d"%(sum(err)))
    image_num = image_num + testnum_per_batch
    testimage = testimage + testnum_per_batch


print("sum error= %d"%(sum(err)))
f1=open("error.txt", "w")
f1.write("Number of wrong recognitions in %d input image(s) = %d\n"% ((ii+1), sum(err)))
f1.close()
f.close()
f2.close()

print("error rate = %f"%(sum(err)/float(testnum)))   #calculate error rate
print("average vdd power = %f"%(sum(float(x) for x in pwr_list)/float(testnum)))   #calculate average power consumption
print("average total power = %f"%(sum(float(x) for x in powr_list)/float(testnum)))   #calculate average power consumption



#measure the run time
end = time.time()
second=math.floor(end-start)
minute=math.floor(second/60)
hour=math.floor(minute/60)
tmin=minute-(60*hour)
tsec=second-(hour*3600)-(tmin*60)

print("Program Execution Time = %d hours %d minutes %d seconds"%(hour,tmin,tsec))



