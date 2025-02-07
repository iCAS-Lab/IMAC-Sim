.SUBCKT DAC in0 in1 in2 out vdd 0

M2 in2 vdd out 0 nmos W=45n L=45n  
M3 in1 vdd out 0 nmos W=90n L=45n  
M4 in0 vdd out 0 nmos W=180n L=45n  
r2 out 0 1k

.ENDS DAC
