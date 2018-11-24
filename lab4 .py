 # -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:13:17 2018

@author: kartik
"""
from math import exp
from random import random
from random import seed

def initialize_network(n_inputs,n_hidden,n_outputs):
    network = []
    hidden_layer = [{'weights':[random() for i in range(n_inputs+1)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(n_hidden+1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network

# calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]
    return activation

# transfer neuron activation

def transfer(activation):
    return 1.0/(1.0+exp(-activation))

def forward_propogate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'],inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

# calculate the derivative of a neuron output
def transfer_derivative(output):
    return output * (1.0 - output)

# backpropogate error and store in neurons
def backward_propogation_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i+1]:
                    error += (neuron['weights'][j]*neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j]-neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])
# update network weights with error
def update_weights(network,row,l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i-1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
                neuron['weights'][-1] += l_rate * neuron['delta']
# train a network for a fixed number of epochs
def train_network(network,train,l_rate,n_epoch,n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            output = forward_propogate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i] - output[i])**2 for i in range(len(expected))])
            backward_propogation_error(network, expected)
            update_weights(network, row, l_rate)
        print(">epoch = %d,lrate = %.3f,error = %.3f" % (epoch,l_rate,sum_error))
#Test training backprop algorithm
seed(1)
dataset=[[2.7810836, 2.550537003, 0],
         [1.465489372, 2.362125076, 0],
         [3.396561688, 4.400293529, 0],
         [1.38807019, 1.850220317, 0],
         [3.06407232, 3.005305973, 0],
         [7.627531214, 2.759262235, 1],
         [5.332441248, 2.088626775, 1],
         [6.922596716, 1.77106367, 1],
         [8.675418651, -0.242068655, 1],
         [7.673756466, 3.508563011, 1]]
n_inputs=len(dataset[0])-1
n_outputs=len(set([row[-1] for row in dataset]))
network= initialize_network(n_inputs, 2 , n_outputs) 
train_network(network, dataset, 0.5, 20, n_outputs)           
for layer in network:
    print(layer)
    
"""
>epoch = 0,lrate = 0.500,error = 6.226
>epoch = 1,lrate = 0.500,error = 5.397
>epoch = 2,lrate = 0.500,error = 5.269
>epoch = 3,lrate = 0.500,error = 5.068
>epoch = 4,lrate = 0.500,error = 4.638
>epoch = 5,lrate = 0.500,error = 4.268
>epoch = 6,lrate = 0.500,error = 3.904
>epoch = 7,lrate = 0.500,error = 3.549
>epoch = 8,lrate = 0.500,error = 3.214
>epoch = 9,lrate = 0.500,error = 2.901
>epoch = 10,lrate = 0.500,error = 2.615
>epoch = 11,lrate = 0.500,error = 2.356
>epoch = 12,lrate = 0.500,error = 2.124
>epoch = 13,lrate = 0.500,error = 1.917
>epoch = 14,lrate = 0.500,error = 1.733
>epoch = 15,lrate = 0.500,error = 1.571
>epoch = 16,lrate = 0.500,error = 1.427
>epoch = 17,lrate = 0.500,error = 1.299
>epoch = 18,lrate = 0.500,error = 1.186
>epoch = 19,lrate = 0.500,error = 1.085
[{'weights': [-1.4991574097533398, 1.8124462072040899, 1.373562784124192], 'output': 0.02661557520048483, 'delta': -0.004706282904724357}, {'weights': [0.38909594876157794, -0.09039690106810404, 0.09004471193724925], 'output': 0.9349011172710473, 'delta': 0.0025732266804154367}]
[{'weights': [2.6333219309236275, -0.1497531360187956, -1.2649549004379637], 'output': 0.2172490655284883, 'delta': -0.03694361833364}, {'weights': [-2.5156632435951014, 1.1307827752337396, 0.4107875725651124], 'output': 0.7945888880040852, 'delta': 0.03352666497398998}]
"""
