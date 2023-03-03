# IMAC-Sim
IMAC-Sim is a Python-based simulation framework, which creates the SPICE netlist of the In-Memory Analog Computing (IMAC) circuit based on various device- and circuit-level hyperparameters selected by the user, and automatically evaluates the accuracy, power consumption and latency of the developed circuit using a user-specified dataset. The list of currently supported inputs are as follows.

- data_dir: The directory where data files are located
- spice_dir: The directory where spice files are located
- dataset_file: Name of the dataset file
- label_file: Name of the label file
- noise: maximum noise amplitude in Volt
- weight_var: variation in the resistance of the synapses in Kohms
- testnum: Number of input test cases to run
- testnum_per_batch: Number of test cases in a single batch
- firstimage: Starting point of the test inputs in the dataset file
- Vdd: The highest voltage
- nodes: Network Topology, an array which defines the DNN model size
- hpar: Array for the horizontal partitioning of all hidden layers
- vpar: Array for the vertical partitioning of all hidden layers
- gain: Array for the differential amplifier gains of all hidden layers
- tech_node: The technology node e.g. 9nm, 45nm etc.
- metal: Width of the metal line for parasitic calculation
- T: Metal thickness
- H: Inter metal layer spacing
- L: length of the bitcell
- W: width of the bitcell
- D: Distance between sp and sn lines
- eps: Permittivity of oxide
- rho: Resistivity of metal

Follow the link for more information. https://arxiv.org/pdf/2210.17410.pdf
## Running the code
- First go to the directory _data_ and put the input test data, label data, pre-trained weights and biases into the directory. Sample files are provided for a 400 X 120 X 84 X 10 DNN model.
- Go to the directory _spice_ and put the neuron subcircuit, differential amplifier subcircuit and transistor models into the directory. Sample model files are provided.
- Open _testFC.py_ and modify the list of inputs as required.
- Run the IMAC using the command _python testFC.py_. This will build the necessary IMAC subcircuits in the _spice_ directory, run the netlist on HSpice and print the accuracy and power consumption results of your input test cases batch-by-batch in the terminal.
