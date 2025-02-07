*3-bit flash ADC

*.INCLUDE '45nm_LP.pm'
.param ref = 1
.param negref = -1
Vref ref 0 DC=ref
Vnegref negref 0 DC=negref
*Vinclk clk 0 PULSE (0 1 0NS 5p 5p 0.5NS 1NS)
.param w48 = AGAUSS(48n,4.8n,3,1)
.param w96 = AGAUSS(96n,9.6n,3,1)

.subckt	nt not2 a vdd gnd
MP14 not2 a vdd vdd PMOS L=45n w=w96
MN1 not2 a gnd gnd NMOS L=45n w=w48
.ends


.subckt	mux21 out i1 i2 select vdd 0
xnot selectnot select vdd 0 nt
MP1 out select i1 vdd PMOS L=45n w=w96
MN1 out selectnot i1 0 NMOS L=45n w=w48
MP2 out selectnot i2 vdd PMOS L=45n w=w96
MN2 out select i2 0 NMOS L=45n w=w48
.ends

.subckt	opamp out outbar sens ref clk vdd 0
MP14 vdd clk vd vdd PMOS L=45n w=w96	
MP1 vd sens left1 vdd PMOS L=45n w=w96
MP2 left1 right2 left2 vdd PMOS L=45n w=w96
MP3 vd ref right1 vdd PMOS L=45n w=w96
MP4 right1 left2 right2 vdd PMOS L=45n w=w96
MN11 left1 clk 0 0 NMOS L=45n w=w48
MN12 left2 clk 0 0 NMOS L=45n w=w48
MN13 left2 right2 0 0 NMOS L=45n w=w48
MN14 right1 clk 0 0 NMOS L=45n w=w48
MN15 right2 clk 0 0 NMOS L=45n w=w48
MN16 right2 left2 0 0 NMOS L=45n w=w48
xnot1 out left2 vdd 0 nt
xnot2 outbar right2	vdd 0 nt
.ends

.subckt	or out in1 in2 in3 in4 vdd 0
xnt1 out t1 vdd 0 nt
Mp1 t4 in1 vdd vdd pmos L=45n w=386n
Mp2 t3 in2 t4 vdd pmos L=45n w=386n
Mp3 t2 in3 t3 vdd pmos L=45n w=386n
Mp4 t1 in4 t2 vdd pmos L=45n w=386n
MN1  t1 in1 0 0 NMOS L=45n w=48n
MN2  t1 in2 0 0 NMOS L=45n w=48n
MN3  t1 in3 0 0 NMOS L=45n w=48n
MN4  t1 in4 0 0 NMOS L=45n w=48n
.ends

.subckt	Enc o0 o1 o2 d0 d1 d2 d3 d4 d5 d6 d7 vdd 0

	xor1 o2 d4 d5 d6 d7 vdd 0 or
	xor2 o1 d2 d3 d6 d7 vdd 0 or
	xor3 o0 d1 d3 d5 d7 vdd 0 or

.ends

.param adc_res = 10k


.subckt	cstmcmp out in1 in2 in1n in2n vdd 0
*in2 msb

	MP1 t1	in2	vdd vdd PMOS L=45n w=192n
	MP2 out	in1n	t1 vdd PMOS L=45n w=192n


	MN1 out in2	0 0 NMOS L=45n w=w48
	
	MN2 out	in1n	t2 0 NMOS L=45n w=w96
	MN3 t2	in2n	0 0 NMOS L=45n w=w96
	
.ends 



.subckt	ADC o0 o1 o2 vin negref ref clk vdd 0

	r1 ref t1 adc_res
	r2 t1 t2 adc_res
	r3 t2 t3 adc_res
	r4 t3 t4 adc_res
	r5 t4 t5 adc_res
	r6 t5 t6 adc_res
	r7 t6 negref adc_res
	
	
	
	
	xcstmcmp1 d_6 d6 d7 d6n d7n vdd 0 cstmcmp
	xcstmcmp2 d_5 d5 d6 d5n d6n vdd 0 cstmcmp
	xcstmcmp3 d_4 d4 d5 d4n d5n vdd 0 cstmcmp
	xcstmcmp4 d_3 d3 d4 d3n d4n vdd 0 cstmcmp
	xcstmcmp5 d_2 d2 d3 d2n d3n vdd 0 cstmcmp
	xcstmcmp6 d_1 d1 d2 d1n d2n vdd 0 cstmcmp

	
	
	
	
	
	
	
	xopamp1 d7 d7n vin ref clk vdd 0 opamp
	xopamp2 d6 d6n vin t1 clk vdd 0 opamp
	xopamp3 d5 d5n vin t2 clk vdd 0 opamp
	xopamp4 d4 d4n vin t3 clk vdd 0 opamp
	xopamp5 d3 d3n vin t4 clk vdd 0 opamp
	xopamp6 d2 d2n vin t5 clk vdd 0 opamp
	xopamp7 d1 d1n vin t6 clk vdd 0 opamp
	
	
	xEnc o0 o1 o2 d0 d_1 d_2 d_3 d_4 d_5 d_6 d7 vdd 0 enc
	
.ends
