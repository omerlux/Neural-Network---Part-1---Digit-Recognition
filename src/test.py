from __future__ import division

import random as rnd
import numpy as np
import matplotlib.pyplot as plot
import mnist_dreader
import network_model
import sgd_optimizer

# dreader = mnist_dreader.dataReader()  # constructing mnist data reader object

# # Test 1 - circular batches
# for i in range(1, 12):
#     a = dreader.get_batch(1000, 'train')  # test for modulo batch

# # Test 2 - shuffle train
# fig = plot.figure()
# for i in range(0, 3):
#     a = dreader.train[i][0]
#     plot.imshow(a)  # test random
#     plot.show()
# dreader.shuffle_train()
# for i in range(0, 3):
#     a = dreader.train[i][0]
#     plot.imshow(a)  # test random
#     plot.show()
# plot.close(fig)

# # Test 3 - print batch num and label
# batch = dreader.get_batch(5, 'train')
# for i in range(0, 5):
#     a = batch[i][0]
#     plot.imshow(a)
#     plot.show()
#     print(batch[i][1])

network = network_model.network([784, 30, 10])  # making the network

# # Test 4 - feew_forward
# batch = dreader.get_batch(10, 'train')
# [output, mean_square_error, negative_log_loss] = network.feed_forward(batch)

# # Test 5 - back_prop checking - debuging gradient
# batch = dreader.get_batch(30, 'train')
# # nabla_wj ~ (C(w + epsilon*e_j) - C(w))/epsilon    *when e_j is the unit vector j
# gradient_biases, gradient_weights, loss_mse, loss_nll = network.back_prop(batch)   # should be the real derivative of the w
# epsilon = 10**-4
# gradient_w_avg_relative_error = 0
# gradient_w_sum_relative_error = 0
# max_relative_error = 0
#
# for j in range(0, (784*30+30*10)//10):  # 10% of the weights
#     w_layer = rnd.randint(0, len(network.weights)-1)              # random layer
#     w_neuron = rnd.randint(0, len(network.weights[w_layer])-1)    # random neuron
#     w = rnd.randint(0, len(network.weights[w_layer][w_neuron])-1) # random weight
#     # for each weight, will add epsilon for the w only, and calculate (C(w + epsilon*e_j) - C(w))/epsilon
#     cost_func_normal = network.feed_forward(batch)[1]       # normal cost
#     network.weights[w_layer][w_neuron][w] += epsilon
#     cost_func_epsilon = network.feed_forward(batch)[1]      # epsilon cost
#     network.weights[w_layer][w_neuron][w] -= epsilon
#
#     estimated_gradient = (cost_func_epsilon - cost_func_normal)/epsilon     # estimated gradient
#     backprop_gradient = gradient_weights[w_layer][w_neuron][w]              # backpropagation gradient
#
#     if backprop_gradient != estimated_gradient:
#         relative_error = np.abs(estimated_gradient - backprop_gradient) / np.abs(
#             estimated_gradient + backprop_gradient)  # |X-Y|/|X+Y|
#         gradient_w_sum_relative_error += relative_error
#         max_relative_error = max(max_relative_error, relative_error)
#         if j != 0:
#             gradient_w_avg_relative_error = gradient_w_sum_relative_error / j  # very low number -> estimation and real are close
#
# print(gradient_w_avg_relative_error)
# print(max_relative_error)

learning_rate = 3.0
batch_size = 10
epochs = 30
# making Stochastic gradient descent optimizer
SGD_optimizer = sgd_optimizer.SGD(network, learning_rate, batch_size, epochs)
SGD_optimizer.training_program()

