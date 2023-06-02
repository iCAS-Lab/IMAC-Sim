# SPICE
The _spice_ directory should contain the necessary SPICE model files for transistors, neuron and differential amplifiers.

## Sample model files
Sample model files are provided here.
- The transistor model provided here is the PTM multi-gate transistor model. The file _models_ contains the libraries for transistors of various sizes. The file _param.inc_ contains specific parameters for various transistor nodes. The directory _modelfiles_ contains the specific model parameter values for different nodes. The default library is set to the ptm14hp here which is the 14nm High-Performance FinFET model. To change the default library, you need to go the _mapIMAC_ module and modify the line that includes the transistor model.
- The neuron model provided here is an analog neuron proposed in the following paper.
  - Md Hasibul Amin, Mohammed Elbtity, Mohammadreza Mohammadi, and Ramtin Zand. 2022. MRAM-based Analog Sigmoid Function for In-memory Computing. In Proceedings of the Great Lakes Symposium on     VLSI 2022 (GLSVLSI '22). Association for Computing Machinery, New York, NY, USA, 319–323. https://doi.org/10.1145/3526241.3530376

The neuron model can be replaced with any other model but make sure the inputs and outputs are in the similar order.
- The differential amplifier subcircuits provided here are op-amp based. _diffi.sp_ represents the differential amplifier for ith layer. Hence, number of differential amplifier subcircuits in this folder must be equal or greater than the number of layers in the DNN model.
