> [!NOTE]  
> The current version only supports ternary (-1, 0, 1) weights and biases. We are working on a script which will support automatic multi-bit quantization and mapping of floating-point weights.

# Data
The _data_ directory should contain the test inputs, labels, weights and biases of the DNN model.
- test_data.csv: Input test data
- test_labels.csv: The labels for the test data
- Wi.csv: The weights for the ith layer.
- Bi.csv: The biases for the ith layer.


## Sample model files
Sample model files provided here are for a 400 X 120 X 84 X 10 MLP model.
- test_data.csv: Input test data for 10000 MNIST handwritten images of 20 X 20 pixels each. The 10000 X 400 csv file represents 10000 test cases, each consisting of 20 X 20 = 400 pixels.
- test_labels.csv: Label for 10000 MNIST handwritten images. The 10000 X 10 csv file contains 10 labels for each of the 10000 test images.
- W1.csv: 400 X 120 csv file, representing the weights for the first layer.
- W2.csv: 120 X 84 csv file, representing the weights for the second layer.
- W3.csv: 84 X 10 csv file, representing the weights for the third layer.
- B1.csv: 120 X 1 csv file, representing the biases for the first layer.
- B2.csv: 84 X 1 csv file, representing the biases for the second layer.
- B3.csv: 10 X 1 csv file, representing the biases for the third layer.
