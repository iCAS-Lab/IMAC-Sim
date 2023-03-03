.SUBCKT neuron in out vsup+ vsup-

X1 out input vsup- vsup- nfet nfin=10
X2 out input vsup+ vsup+ pfet nfin=10
Rlow in2 input 8488.26363157
vin in in2 -0.4
Rhigh input out 25464.7908947

.ENDS neuron
