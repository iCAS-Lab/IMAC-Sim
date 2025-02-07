.subckt	drelu in0 in1 in2 out0 out1 out2 vdd 0
xmux0 out0 0 in0 in2 vdd 0 mux21
xmux1 out1 0 in1 in2 vdd 0 mux21
*xmux2 out2 0 in2 in2 vdd 0 mux21
rfill in2 out2 1m
.ends
