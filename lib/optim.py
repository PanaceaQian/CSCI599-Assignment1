from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


""" Super Class """
class Optimizer(object):
    """
    This is a template for implementing the classes of optimizers
    """
    def __init__(self, net, lr=1e-4):
        self.net = net  # the model
        self.lr = lr    # learning rate

    """ Make a step and update all parameters """
    def step(self):
        raise ValueError("Not Implemented Error")


""" Classes """
class SGD(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-4):
        self.net = net
        self.lr = lr

    def step(self):
        for layer in self.net.layers:
            for n, dv in layer.grads.items():
                layer.params[n] -= self.lr * dv


class SGDM(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-4, momentum=0.0):
        self.net = net
        self.lr = lr
        self.momentum = momentum
        self.velocity = {}  # last update of the velocity

    def step(self):
        #############################################################################
        # TODO: Implement the SGD + Momentum                                        #
        #############################################################################
        for layer in self.net.layers:
            for n, dv in layer.grads.items():
                if n not in self.velocity:
                    self.velocity[n] = np.zeros_like(dv)
                self.velocity[n] = self.momentum * self.velocity[n] - self.lr * dv
                layer.params[n] += self.velocity[n]                    
                # layer.params[n] -= self.lr * dv
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################


class RMSProp(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-2, decay=0.99, eps=1e-8):
        self.net = net
        self.lr = lr
        self.decay = decay
        self.eps = eps
        self.cache = {}  # decaying average of past squared gradients

    def step(self):
        #############################################################################
        # TODO: Implement the RMSProp                                               #
        #############################################################################
        for layer in self.net.layers:
            for n, dv in layer.grads.items():
                if n not in self.cache:
                    self.cache[n] = np.zeros_like(dv)
                self.cache[n] = self.decay * self.cache[n] + (1 - self.decay) * np.square(dv)
                layer.params[n] -= (self.lr * dv) / np.sqrt(self.cache[n] + self.eps)
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################


class Adam(Optimizer):
    """ Some comments """
    def __init__(self, net, lr=1e-3, beta1=0.9, beta2=0.999, t=0, eps=1e-8):
        self.net = net
        self.lr = lr
        self.beta1, self.beta2 = beta1, beta2
        self.eps = eps
        self.mt = {}
        self.vt = {}
        self.t = t

    def step(self):
        #############################################################################
        # TODO: Implement the Adam                                                  #
        #############################################################################
        self.t += 1
        for layer in self.net.layers:
            for n, dv in layer.grads.items():
                if n not in self.mt:
                    self.mt[n] = np.zeros_like(dv)
                self.mt[n] = self.beta1 * self.mt[n] + (1 - self.beta1) * dv
                
                if n not in self.vt:
                    self.vt[n] = np.zeros_like(dv)
                self.vt[n] = self.beta2 * self.vt[n] + (1 - self.beta2) * np.square(dv)
                
                _mt = self.mt[n] / (1 - np.power(self.beta1, self.t))
                _vt = self.vt[n] / (1 - np.power(self.beta2, self.t))
                             
                layer.params[n] -= (self.lr * _mt) / (np.sqrt(_vt) + self.eps)    
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
