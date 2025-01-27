
############################################################
#                                                          #
#          2023 Md Hasibul Amin. All rights reserved.      #
#                      ma77@email.sc.edu                   #
#                                                          #
############################################################
import re
import os
import time
import math
import random
import mapIMAC
import mapWB
import numpy as np
import csv

start = time.time()

#list of inputs start
data_dir='data' #The directory where data files are located
spice_dir='spice' #The directory where spice files are located
dataset_file='test_data.csv' #Name of the dataset file
label_file='test_labels.csv' #Name of the label file
weight_var=0.0 #percentage variation in the resistance of the synapses
testnum=4 #Number of input test cases to run
testnum_per_batch=2 #Number of test cases in a single batch, testnum should be divisible by this number
firstimage=0 #start the test inputs from this image
vdd=0.8 #The positive supply voltage
vss=-0.8 #The negative supply voltage
tsampling=1 #The sampling time in nanosecond
nodes=[400,120,84,10] #Network Topology, an array which defines the DNN model size
xbar=[32,32] #The crossbar size
gain=[30,30,10] #Array for the differential amplifier gains of all hidden layers
tech_node=9e-9 #The technology node e.g. 9nm, 45nm etc.
metal=3*tech_node #Width of the metal line for parasitic calculation
T=22e-9 #Metal thickness
H=20e-9 #Inter metal layer spacing
L=15*tech_node #length of the bitcell
W=12*tech_node #width of the bitcell
D=5*tech_node #distance between I+ and I- lines
eps = 20*8.854e-12 #permittivity of oxide
rho = 1.9e-8 #resistivity of metal
rlow=5e3 #Low resistance level of the memristive device
rhigh=15e3 #High resistance level of the memristive device
#list of inputs end

hpar=[math.ceil(x/xbar[0]) for x in nodes] #Calculating the horizontal partitioning array for all hidden layers
hpar.pop() #The last value in the array is removed for hpar
vpar=[math.ceil(x/xbar[1]) for x in nodes] #Calculating the vertical partitioning array for all hidden layers
vpar.pop(0) #The first value in the array is removed for vpar

print('Rlow=%f'%rlow)
print('Rhigh=%f'%rhigh)
print('Horizontal partitions = '+str(hpar))
print('Vertical partitions = '+str(vpar))

#function to update the device resistances in the neuron.sp file, which includes the spice file for activation function
def update_neuron (rlow,rhigh):
    ff=open(spice_dir+'/'+'neuron.sp', "r+")
    i=0
    data= ff.readlines()
    for line in data:
        i+=1
        if 'Rlow' in line:
            data[i-1]='Rlow in2 input ' + str(rlow) +'\n'
        if 'Rhigh' in line:
            data[i-1]='Rhigh input out ' + str(rhigh) +'\n'

    ff.seek(0)
    ff.truncate()
    ff.writelines(data)
    ff.close()

#function to update the gain for the differential amplifiers
def update_diff (gain, LayerNUM):
    name=spice_dir+'/'+'diff{}.sp'.format(LayerNUM)
    ff=open(name, "r+")
    i=0
    data= ff.readlines()
    for line in data:
        i+=1
        if 'Gain' in line:
            data[i-1]='*Differential Amplifier with Gain=' + str(gain) +'\n'
        if 'R3' in line:
            data[i-1]='R3 n1 out ' + str(gain) +'k\n'
        if 'R4' in line:
            data[i-1]='R4 n2 0 ' + str(gain) +'k\n'
    ff.seek(0)
    ff.truncate()
    ff.writelines(data)
    ff.close()


#function to extract the measured average voltage or power from time1 to time2 in the output text file genrated by SPICE
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

#function to extract the measured voltage at a specific time in the output text file genrated by SPICE
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
dataset_flat = dataset.flatten()
dataset_bin = np.sign(dataset_flat)

data_w = open(data_dir+'/'+'testinput.txt', "w")
for i in range(len(dataset_bin)):
    data_w.write("%f\n"%(float(dataset_bin[i])))	
data_w.close()

#label preprocessing
label = np.genfromtxt(data_dir+'/'+'test_labels.csv',delimiter=',')
label_flat = label.flatten()
label_w = open(data_dir+'/'+'testlabel.txt', "w")
for i in range(len(label_flat)):
    label_w.write("%f\n"%(float(label_flat[i])))	
label_w.close()

data_r=open(data_dir+'/'+'testinput.txt', "r")   # testinput.txt includes the test images from the MNIST Dataset
label_r=open(data_dir+'/'+'testlabel.txt', "r")  # testlabel.txt includes the labels of the test images in the MNIST Dataset
data_all=data_r.readlines() #data_all contains all test images
label_all=label_r.readlines() #label_all contains all labels
length=len(nodes) #length contains the number of layers in DNN model
#update_neuron(rlow,rhigh) #updates the resistances in the neuron
for i in range(len(nodes)-1):
    update_diff(gain[i],i+1) #updates the differential amplifier gains
mapWB.mapWB(length,rlow,rhigh,nodes,data_dir,weight_var) #calling mapWB which sets the corresponding resistance value for weights and biases
batch=testnum//testnum_per_batch #calculates the number of batch for the simulation
image_num=0 #number of image in the simulation
testimage=firstimage
err=[] #the array containing error information for each test case
pwr_list=[] #the array containing power information for each test case

for i in range(batch):
    out_list=[]
    label_list=[]
    data_sim=data_all[int(testimage*nodes[0]):int((testimage+testnum_per_batch)*nodes[0])]
    label_sim=label_all[int(testimage*nodes[len(nodes)-1]):int((testimage+testnum_per_batch)*nodes[len(nodes)-1])]
    for value in label_sim:
        label_list.append(float(value))
    sim_w=open(data_dir+'/'+'data_sim.txt', "w")
    for j in range(int(testnum_per_batch*nodes[0])):	
        sim_w.write("%f "%(float(data_sim[j])*vdd))	
    sim_w.close()
    mapIMAC.mapIMAC(nodes,length,hpar,vpar,metal,T,H,L,W,D,eps,rho,weight_var,testnum_per_batch,data_dir,spice_dir,vdd,vss,tsampling)
    os.chdir(spice_dir)
    os.system('hspice classifier.sp > output.txt')
    os.chdir('..')
    out_r=open(spice_dir+'/'+'output.txt', "r")
    for line in out_r:
        if 'vout' in line:
            vval=findat(line)
            out_list.append(float(vval))
        if 'pwr' in line:
            pval=findavg(line)
            pwr_list.append(pval)
    out_r.close()
        
    for j in range (testnum_per_batch):
        print(j+image_num+1)
        print(f'Actual label: {label_list[nodes[len(nodes)-1]*j:nodes[len(nodes)-1]*(j+1)]}')
        err.append(int(0))
        list_max=max(out_list[nodes[len(nodes)-1]*j:nodes[len(nodes)-1]*(j+1)])
        print(f'Output voltages: {out_list[nodes[len(nodes)-1]*j:nodes[len(nodes)-1]*(j+1)]}')
        #print(list_max)
        for k in range (nodes[len(nodes)-1]):
            if (out_list[nodes[len(nodes)-1]*j+k]==list_max):    # the neuron generating maximum output value represents the corrosponding class
                out_list[nodes[len(nodes)-1]*j+k]=1.0
            else:
                out_list[nodes[len(nodes)-1]*j+k]=0.0
            if (err[j+image_num]==0):
                if (out_list[nodes[len(nodes)-1]*j+k] != label_list[nodes[len(nodes)-1]*j+k]):
                    err[j+image_num]=1
        print(f'Predicted label: {out_list[nodes[len(nodes)-1]*j:nodes[len(nodes)-1]*(j+1)]}')
        if err[j+image_num]==1:
            print("Wrong prediction!")
        else:
            print("Correct prediction")
        print("Power consumption = %f"%float(pwr_list[j+image_num]))
        print("sum error= %d"%(sum(err)))
    image_num = image_num + testnum_per_batch
    testimage = testimage + testnum_per_batch

print("Task completed!")
print("Total error= %d"%(sum(err)))
err_w=open("error.txt", "w")
err_w.write("Number of wrong recognitions in %d input image(s) = %d\n"% (image_num, sum(err)))
err_w.close()
data_r.close()
label_r.close()

print("error rate = %f"%(sum(err)/float(testnum)))   #calculate error rate
print("accuracy = %f%%"%(100-(sum(err)/float(testnum))*100))   #calculate accuracy
print("average total power = %f"%(sum(float(x) for x in pwr_list)/float(testnum)))   #calculate average power consumption



#measure the run time
end = time.time()
second=math.floor(end-start)
minute=math.floor(second/60)
hour=math.floor(minute/60)
tmin=minute-(60*hour)
tsec=second-(hour*3600)-(tmin*60)

print("Program Execution Time = %d hours %d minutes %d seconds"%(hour,tmin,tsec))

