import numpy as np
import matplotlib.pyplot as plot
import scipy
from sklearn.metrics import mean_squared_error
from sklearn.metrics import log_loss


def sigmoid(z):
    """ Sigmoid function
    1.0 / (1.0 + np.exp(-z))"""
    return scipy.special.expit(z)


def sigmoid_derivative(z):
    """ Sigmoid derivative by z"""
    return sigmoid(z)*(1-sigmoid(z))


def cost_derivative(output, y):
    """for the cost function (1/2)*(a-y)^2
    the derivative is a-y"""
    return output - y


def vectorized_res(j):
    """Return a 10-dimensional unit vector with a 1.0 in the jth
    position and zeroes elsewhere. This is used to convert a digit
    (0...9) into a corresponding desired output from the neural
    network."""
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


def cost_func_single(out, y):
    """ :returns the quadratic cost function for single sample"""
    y_vec = vectorized_res(y)
    cost_j = [np.power(aj - yj, 2) for aj, yj in zip(out, y_vec)]
    return (1/2.0)*np.sum(cost_j)



class network(object):
    def __init__(self, sizes):  # sizes=[#inputs, #2nd layer, .... , #outputs]
        """ Initializing the network object
        sizes is array that will contain the number of neurons in each layer.
        the weights and biases for each neuron will be randomly chosen from a Norm~(meu,sigma) cdf"""
        print ('Initializing network model object...')
        self.sizes = sizes
        self.num_of_layers = len(sizes)
        # Biases initiate - randomize by normal distribution biases as the numbers of neurons in the network (without
        # input neurons)
        sigma = 0.5
        meu = 0
        self.biases = [sigma * np.random.randn(dimensions, 1) + meu for dimensions in sizes[1:]]
        self.delta_biases = [np.zeros((dimensions, 1)) for dimensions in sizes[1:]]
        # dimensions: [#2nd layer, ... , #outputs], so we have X biases as the numbers of neurons except the inputs
        # Weights initiate - randomize by normal distribution weights for each neuron
        sigma2 = 0.5
        meu2 = 0
        self.weights = [sigma2 * np.random.randn(dim2, dim1) + meu2 for (dim1, dim2) in zip(sizes[:-1], sizes[1:])]
        self.delta_weights = [np.zeros((dim2, dim1)) for (dim1, dim2) in zip(sizes[:-1], sizes[1:])]
        # size[:-1], size[1:] creates pairs of elements in the sequence sizes with the next element,
        # because you pair up all elements except the last (sizes[:-1]) with all elements except the first (sizes[1:])
        self.biases_num = sum(sizes) - sizes[0]
        self.weights_num = sum(x*y for (x, y) in zip(sizes[:-1], sizes[1:]))

    def feed_forward(self, batch, only_out):
        """ Feeding forward the network with an intput of batch.
        That means we feed the network m times for an image which is a 784 input vector.
        :return the model's output - ONLY output if bool_only_out=1 else, adding:
        the loss functions. 1. mean square error, 2. negative log loss"""
        # creating the function for each loss function
        out = []
        for (x, y) in batch:
            x = np.reshape(x, (784, 1))
            for (b, w) in zip(self.biases, self.weights):
                x = sigmoid(np.dot(w, x) + b)  # a is now the output of the curr layer, and input of the next
            out.append(x)            #np.reshape(x, len(batch))
        if only_out:
            return out
        else:
            return [out,    # this is the output of the network
                    self.loss_mse(out, [y for (_, y) in batch]),
                    self.loss_nll(out, [y for (_, y) in batch])]

    def loss_mse(self, out, y):
        """ :return the mean square error of @ out compared to @ y"""
        # y - is the labels, out is the network output
        mse = 0     # mean square error
        for res, y_res in zip(out, y):
            mse += mean_squared_error(vectorized_res(y_res), res)   # calculating error from each label and output
        # for i in range(0, len(y)):
        #     y_vec = np.zeros(10)
        #     y_vec[y[i]] = 1
        #     mse = mse + mean_squared_error(y_vec, out[i])
        return mse/len(y)   # for the mean square error fix

    def loss_nll(self, out, y):
        """ :return the negative log loss of @ out compared to @ y"""
        # y - is the labels, out is the network output
        nll = 0     # negative log los = -log P(yt|yp) = -(yt log(yp) + (1 - yt) log(1 - yp))
        for res, y_res in zip(out, y):
            nll += log_loss(vectorized_res(y_res), res)  # calculating error from each label and output
        # for i in range(0, len(y)):
        #     y_vec = np.zeros(10)
        #     y_vec[y[i]] = 1
        #     nll = nll + log_loss(y_vec, out[i]) # calculating error from each label and output
        return nll/len(y)   # for the mean square error fix

    def back_prop(self, batch):
        """ batch - is a batch of input examples and labels.
        :returns the gradient vector of the batch"""
        nabla_b = [np.zeros(b.shape) for b in self.biases]      # initializing the changes in b and w
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in batch:      # for every example with label do:
            x = np.reshape(x, (784, 1))
            # FOR EACH EXMAPLE: calculating the delta in b and w for single exmaple
            nabla_b_single, nabla_w_single = self.back_prop_single(x, y)

            # NEXT: adding the nabla_x_single to the nabla_x of all exmaples
            nabla_b = [nb + delta_nb for nb, delta_nb in zip(nabla_b, nabla_b_single)]      # summing the nablas
            nabla_w = [nw + delta_nw for nw, delta_nw in zip(nabla_w, nabla_w_single)]
        return [nabla_b, nabla_w]

    def back_prop_single(self, x, y):
        # FEEDING FORWARD the network:
        nabla_b_single = [np.zeros(b.shape) for b in
                          self.biases]  # initializing the changes in b and w for single input
        nabla_w_single = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]  # saving activations for all the layers
        zs = []  # saving z vectors for all layers
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b  # setting new z= w*a+b
            zs.append(z)  # saving z
            activation = sigmoid(z)  # setting new output of the current layer
            activations.append(activation)  # saving activations
        # --> we saved all the activations and zs for each layer

        # GOING BACKWARD to calculate the cost change by:
        # BP1 -> delta_L = Nabla_C_a . sigmoid_derivative(z_L)
        # BP2 -> delta_l = ((w_l+1)T * delta_l+1) . sigmoid_derivative(z_l)
        # BP3 -> Nabla_C_bj_l = delta_j_l
        # BP4 -> Nabla_C_wjk_l = delta_j_l * activation_k_l-1
        delta = cost_derivative(activations[-1], vectorized_res(y)) * sigmoid_derivative(zs[-1])  # by BP1 equation
        nabla_b_single[-1] = delta  # by BP3
        nabla_w_single[-1] = np.dot(delta, np.transpose(activations[-2]))  # by BP4 # TODO: check size of both
        # calculating all the nabla_w when walking backwards in the network
        for l in xrange(2, self.num_of_layers):
            z = zs[-l]
            delta = np.dot(np.transpose(self.weights[-l + 1]), delta) * sigmoid_derivative(z)  # by BP2
            nabla_b_single[-l] = delta  # by BP3
            nabla_w_single[-l] = np.dot(delta, np.transpose(activations[-l - 1]))  # by BP4 # TODO: check size of both
        # --> we saved all the changes in 'w' and 'b' for the specific example.
        return nabla_b_single, nabla_w_single

    def update_wb(self, nabla_biases, nabla_weights, eta, len_batch):
        # normalizing the results as the number of exmaples
        self.weights = [w - (eta/len_batch) * nw
                        for w, nw in zip(self.weights, nabla_weights)]
        self.biases = [b - (eta/len_batch) * nb
                       for b, nb in zip(self.biases, nabla_biases)]

    def update_wb_momentum(self, nabla_biases, nabla_weights, eta, gamma, len_batch):
        """ check the website https://ruder.io/optimizing-gradient-descent/index.html#rmsprop to see momentum"""
        # normalizing the results as the number of exmaples
        self.delta_biases = [v * gamma + (eta * nb)/len_batch for v, nb in zip(self.delta_biases, nabla_biases)]
        self.delta_weights = [v * gamma + (eta * nw)/len_batch for v, nw in zip(self.delta_weights, nabla_weights)]
        self.biases = [b - nb
                       for b, nb in zip(self.biases, self.delta_biases)]
        self.weights = [w - nw
                        for w, nw in zip(self.weights, self.delta_weights)]
