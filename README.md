# IMAC-Sim
IMAC-Sim is a Python-based simulation framework, which creates the SPICE netlist of the In-Memory Analog Computing (IMAC) circuit based on various device- and circuit-level hyperparameters selected by the user, and automatically evaluates the accuracy, power consumption and latency of the developed circuit using a user-specified dataset. Follow the link for more information. https://arxiv.org/pdf/2210.17410.pdf
## Running the code
- First go to the directory _data_ and put the input test data, label data, pre-trained weights and biases into the directory. Sample model is provided.
- Go to the directory _spice_ and put the neuron subcircuit, differential amplifier subcircuit and transistor models into the directory. Sample model is provided.
- Open _testFC.py_ and modify the list of inputs as required.
- Run the IMAC using the command _python testFC.py_. 
