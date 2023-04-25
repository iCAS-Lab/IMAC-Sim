# IMAC-Sim
IMAC-Sim is a Python-based simulation framework, which creates the SPICE netlist of the In-Memory Analog Computing (IMAC) circuit based on various device- and circuit-level hyperparameters selected by the user, and automatically evaluates the accuracy, power consumption and latency of the developed circuit using a user-specified dataset. The list of currently supported inputs are as follows.

- data_dir: The directory where data files are located
- spice_dir: The directory where spice files are located
- dataset_file: Name of the dataset file
- label_file: Name of the label file
- weight_var: percentage variation in the resistance of the synapses
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
- rlow: Low resistance level of the memristive device
- rhigh: High resistance level of the memristive device

Follow this paper for more information. Md Hasibul Amin, Mohammed E. Elbtity, and Ramtin Zand. 2023. IMAC-Sim: A Circuit-level Simulator For In-Memory Analog Computing Architectures (2023). https://arxiv.org/abs/2304.09252

## Running the code
- First go to the directory _data_ and put the input test data, label data, pre-trained weights and biases into the directory. Sample files are provided for a 400 X 120 X 84 X 10 DNN model.
- Go to the directory _spice_ and put the neuron subcircuit, differential amplifier subcircuit and transistor models into the directory. Sample model files are provided.
- Open _testIMAC.py_ and modify the list of inputs as required.
- Make sure you have HSpice installed and accessible in your machine through _hspice_ command in the terminal. The code initiates a HSpice run through an os.system call of the _hspice_ command.
- Run the IMAC using the command _python testIMAC.py_. This will build the necessary IMAC subcircuits in the _spice_ directory, run the netlist on HSpice and print the accuracy and power consumption results of your input test cases batch-by-batch in the terminal.


## More documentation

The following papers use IMAC-Sim.
- M. H. Amin, M. E. Elbtity and R. Zand, "Xbar-Partitioning: A Practical Way for Parasitics and Noise Tolerance in Analog IMC Circuits," in IEEE Journal on Emerging and Selected Topics in Circuits and Systems, vol. 12, no. 4, pp. 867-877, Dec. 2022, doi: 10.1109/JETCAS.2022.3222966.
- M. Elbtity, A. Singh, B. Reidy, X. Guo and R. Zand, "An In-Memory Analog Computing Co-Processor for Energy-Efficient CNN Inference on Mobile Devices," 2021 IEEE Computer Society Annual Symposium on VLSI (ISVLSI), Tampa, FL, USA, 2021, pp. 188-193, doi: 10.1109/ISVLSI51109.2021.00043.
- Md Hasibul Amin, Mohammed Elbtity, Mohammadreza Mohammadi, and Ramtin Zand. 2022. MRAM-based Analog Sigmoid Function for In-memory Computing. In Proceedings of the Great Lakes Symposium on VLSI 2022 (GLSVLSI '22). Association for Computing Machinery, New York, NY, USA, 319–323. https://doi.org/10.1145/3526241.3530376
- M. H. Amin, M. Elbtity and R. Zand, "Interconnect Parasitics and Partitioning in Fully-Analog In-Memory Computing Architectures," 2022 IEEE International Symposium on Circuits and Systems (ISCAS), Austin, TX, USA, 2022, pp. 389-393, doi: 10.1109/ISCAS48785.2022.9937884.
