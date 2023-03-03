# IMAC-Sim
IMAC-Sim is a Python-based simulation framework, which creates the SPICE netlist of the In-Memory Analog Computing (IMAC) circuit based on various device- and circuit-level hyperparameters selected by the user, and automatically evaluates the accuracy, power consumption and latency of the developed circuit using a user-specified dataset. Follow the link for more information. https://arxiv.org/pdf/2210.17410.pdf
## Running the code
- First go to the directory _data_ and put the input test data, label data, pre-trained weights and biases into the directory. Sample files are provided for a 400 X 120 X 84 X 10 DNN model.
- Go to the directory _spice_ and put the neuron subcircuit, differential amplifier subcircuit and transistor models into the directory. Sample model files are provided.
- Open _testFC.py_ and modify the list of inputs as required.
- Run the IMAC using the command _python testFC.py_. This will build the necessary IMAC subcircuits in the _spice_ directory, run the netlist on HSpice and print the accuracy and power consumption results of your input test cases batch-by-batch in the terminal.
