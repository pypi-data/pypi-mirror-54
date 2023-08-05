#!/usr/bin/env python
'''
component_tf
Created by Seria at 05/02/2019 1:41 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
from functools import partial
from mxnet.gluon import nn, loss, Trainer, HybridBlock
from mxnet import nd, init, autograd, lr_scheduler
from math import ceil
import os
from ..toolkit.utility import recordConfig
from .component import Pod


class MXsigmoid(HybridBlock):
    def __init__(self, **kwargs):
        super(MXsigmoid, self).__init__(**kwargs)

    def hybrid_forward(self, F, input):
        return F.sigmoid(input)

class MXtanh(HybridBlock):
    def __init__(self, **kwargs):
        super(MXtanh, self).__init__(**kwargs)

    def hybrid_forward(self, F, input):
        return F.tanh(input)

class MXsoftmax(HybridBlock):
    def __init__(self, **kwargs):
        super(MXsoftmax, self).__init__(**kwargs)

    def hybrid_forward(self, F, input):
        return F.softmax(input)

class MXrelu(HybridBlock):
    def __init__(self, **kwargs):
        super(MXrelu, self).__init__(**kwargs)

    def hybrid_forward(self, F, input):
        return F.relu(input)

class Duplicate(HybridBlock):
    def __init__(self, **kwargs):
        super(Duplicate, self).__init__(**kwargs)

    def hybrid_forward(self, F, input):
        return input

class MXwd(HybridBlock):
    def __init__(self, **kwargs):
        super(MXwd, self).__init__(**kwargs)

    def hybrid_forward(self, F, penalty):
        return F.zeros((1))

class MXmse(HybridBlock):
    def __init__(self, **kwargs):
        super(MXmse, self).__init__(**kwargs)

    def hybrid_forward(self, F, input, label):
        return (input-label)**2

class MXmae(HybridBlock):
    def __init__(self, **kwargs):
        super(MXmae, self).__init__(**kwargs)

    def hybrid_forward(self, F, input, label):
        return F.abs(input-label)

class MXsigmxe(HybridBlock):
    def __init__(self, **kwargs):
        super(MXsigmxe, self).__init__(**kwargs)
        self.cost = loss.SigmoidBCELoss()

    def hybrid_forward(self, F, input, label):
        return F.mean(self.cost(input, label))

class MXsftmxe(HybridBlock):
    def __init__(self, is_one_hot, **kwargs):
        super(MXsftmxe, self).__init__(**kwargs)
        self.cost = loss.SoftmaxCELoss(sparse_label=not is_one_hot)

    def hybrid_forward(self, F, input, label):
        return F.mean(self.cost(input, label))

class MX(HybridBlock):
    def __init__(self, **kwargs):
        super(MX, self).__init__(**kwargs)

    def hybrid_forward(self, F, input):
        return nd.sigmoid(input)

class AccuracyCLS(HybridBlock):
    def __init__(self, multi_class, is_one_hot, **kwargs):
        super(AccuracyCLS, self).__init__(**kwargs)
        if multi_class:
            assert not is_one_hot
        self.mulcls = multi_class
        self.onehot = is_one_hot

    def hybrid_forward(self, F, input, label):
        if self.mulcls:
            pred = F.round(input)
            correct = F.mean(pred == label, axis=-1)
            return F.mean(correct == 1)
        else:
            if self.onehot:
                label = F.argmax(label, axis=-1)
            pred = F.argmax(input, axis=-1)
            return F.mean(pred == label)

class ComponentMX(object):
    def __init__(self, channel_major=True, time_major=False):
        self.channel_major = channel_major
        self.time_major = time_major
        self.warehouse = ['CONV_1D', 'CONV', 'CONV_3D', 'CONV_TRANS', 'CONV_SEP',
                          'SIGMOID', 'TANH', 'SOFTMAX', 'RELU', 'RELU_LEAKY', 'RELU_EXP',
                          'MAX_POOL', 'AVG_POOL',
                          'DROPOUT', 'BATCH_NORM', 'EMBEDDING',
                          'RESHAPE', 'FLAT', 'SLICE',
                          'CLIP', 'DENSE',
                          'RESIZE',
                          'DUPLICATE', 'CONVERT',
                          'WEIGHT_DECAY', 'SIGM_XENTROPY', 'SFTM_XENTROPY', 'MSE', 'MAE',
                          'MOMENTUM', 'NESTEROV', 'ADAM']
        # Convolution
        self.CONV_1D = 0
        self.CONV = self.conv_2d
        self.CONV_3D = 2
        self.CONV_TRANS = 3
        self.CONV_SEP = 4
        # Activation
        self.SIGMOID = self.sigmoid
        self.TANH = self.tanh
        self.SOFTMAX = self.softmax
        self.RELU = self.relu
        self.RELU_LEAKY = self.relu_leaky
        # self.RELU_EXP = self.relu_exp
        # Pooling
        self.MAX_POOL = self.max_pool_2d
        self.AVG_POOL = self.avg_pool_2d
        # Distributing
        self.DROPOUT = self.dropout
        self.BATCH_NORM = self.batch_norm
        # self.EMBEDDING = self.embedding
        # Reshape
        # self.RESHAPE = self.reshape
        self.FLAT = self.flat
        # self.SLICE = self.slice
        # self.PAD = self.pad
        # Arithmetic
        # self.CLIP = self.clip
        self.DENSE = self.dense
        # self.ARGMAX = self.argmax
        # Image Manipulation
        # self.RESIZE = self.resize
        # Copy or Rename
        self.DUPLICATE = self.duplicate
        # self.CONVERT = self.convert
        # Loss
        self.WEIGHT_DECAY = self.weight_decay
        self.SIGM_XENTROPY = self.sigm_xentropy
        self.SFTM_XENTROPY = self.sftm_xentropy
        self.MSE = self.mse
        self.MAE = self.mae
        # Optimizer
        self.MOMENTUM = self.momentum
        self.NESTEROV = self.nesterov
        self.ADAM = self.adam
        # Metric
        self.ACC_CLS = self.accuracy_cls



    def addComp(self, name, comp, is_complete=False):
        name = name.upper()
        if name in self.warehouse:
            raise Exception('NEBULAE ERROR ⨷ %s is an existing component in warehouse.' % name)
        else:
            self.warehouse.append(name)
        if is_complete:
            def customizedComp(name):
                return Pod(partial(comp.component, name=name), comp.symbol, name, comp.message)
        else:
            assert not isinstance(comp.component, list)
            def customizedComp(**kwargs):
                message = []
                # check input so as to update message
                for s, sym in enumerate(comp.symbol):
                    if sym in kwargs:
                        message.append(kwargs[sym])
                    else:
                        message.append(comp.message[s])
                return Pod(partial(comp.component, **kwargs), comp.symbol, kwargs['name'], message)
        exec('self.%s = customizedComp' % name)

    # ------------------------------------ Convolution ------------------------------------ #

    def _getInitializer(self, initializer, param, regularizer):
        init_err = Exception('NEBULAE ERROR ⨷ %s initializer is not defined or supported.' % initializer)
        if initializer == 'xavier':
            if param is None:
                param = 'gaussian'
            else:
                if param=='normal':
                    param = 'gaussian'
            var = init.Xavier(param)
        elif initializer == 'uniform':
            if param is None:
                param = 0.5
            else:
                if param[0] != 0:
                    raise Exception('NEBULAE ERROR ⨷ mean of uniform distributed initializer must be 0 in MXNET core.')
                param = param[1]
            var = init.Uniform(param)
        elif initializer == 'normal':
            if param is None:
                param = 0.1
            else:
                if param[0]+param[1] != 0:
                    raise Exception('NEBULAE ERROR ⨷ min and max value of normal distributed initializer must be',
                                    'opposite numbers in MXNET core.')
                param = param[1]
            var = init.Normal(param)
        elif initializer == 'zero':
            var = init.Zero()
        elif initializer == 'one':
            var = init.One()
        else:
            raise init_err

        if regularizer == 'l2':
            pass
        else:
            raise Exception('NEBULAE ERROR ⨷ %s regularizer is not defined or supported.' % regularizer)

        return var

    def conv_2d(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._conv_2d, **kwargs), ['input'], kwargs['name'], [message])
    def _conv_2d(self, name, input, kernel, out_chs, w_init='xavier', w_param=None,
                 b_init=None, b_param=None, w_reg='l2', b_reg='l2', stride=(1, 1), dilation=(1, 1), keep_size=True):
        if self.channel_major:
            format = 'NCHW'
            h, w = input[0][2:]
        else:
            format = 'NHWC'
            h, w = input[0][1:3]
        if keep_size:
            y = ceil(((ceil(h / stride[0]) - 1) * stride[0] + kernel[0] + (dilation[0] - 1) * (kernel[0] - 1) - h) / 2)
            x = ceil(((ceil(w / stride[1]) - 1) * stride[1] + kernel[1] + (dilation[1] - 1) * (kernel[1] - 1) - w) / 2)
            padding = (y, x)
        else:
            padding = (0, 0)
        if not w_init is None:
            w_init = self._getInitializer(w_init, w_param, w_reg)
        if not b_init is None:
            use_bias = True
            b_init = self._getInitializer(b_init, b_param, b_reg)
        else:
            use_bias = False
        return nn.Conv2D(channels=out_chs, kernel_size=kernel, strides=stride, padding=padding, dilation=dilation,
                         layout=format, use_bias=use_bias, weight_initializer=w_init, bias_initializer=b_init, prefix=name)

    # ------------------------------------ Activation ------------------------------------ #

    def sigmoid(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._sigmoid, **kwargs), ['input'], kwargs['name'], [message])
    def _sigmoid(self, name, input):
        return MXsigmoid()

    def tanh(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._tanh, **kwargs), ['input'], kwargs['name'], [message])
    def _tanh(self, name, input):
        return MXtanh()

    def softmax(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._tanh, **kwargs), ['input'], kwargs['name'], [message])
    def _softmax(self, name, input):
        return MXsoftmax()

    def relu(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._relu, **kwargs), ['input'], kwargs['name'], [message])
    def _relu(self, name, input):
        return MXrelu()

    def relu_leaky(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._relu_leaky, **kwargs), ['input'], kwargs['name'], [message])
    def _relu_leaky(self, name, input, alpha=0.2):
        return nn.LeakyReLU(alpha)

    # ------------------------------------ Distributing ------------------------------------ #

    def dropout(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._dropout, **kwargs), ['input'], kwargs['name'], [message])
    def _dropout(self, name, input, p_drop):
        return nn.Dropout(p_drop)

    def batch_norm(self, **kwargs):
        message = []
        message.append(kwargs.get('input', '_INPUT'))
        message.append(kwargs.get('is_train', '_IS_TRAIN'))
        return Pod(partial(self._batch_norm, **kwargs), ['input', 'is_train'], kwargs['name'], message)
    def _batch_norm(self, name, input, is_train, beta=False, gamma=False):
        if self.channel_major:
            axis = 1
        else:
            axis = -1
        return nn.BatchNorm(axis=axis, momentum=0.9, epsilon=1e-05, center=beta, scale=gamma)

    # def embedding(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._embedding, **kwargs), ['input'], kwargs['name'], [message])
    # def _embedding(self, name, input, vocabulary, vec_dims, w_init='xavier', w_param=None):
    #     embd_vec = self._createVar(name+'_vec', [vocabulary, vec_dims], w_init, w_param)
    #     return tf.nn.embedding_lookup(embd_vec, input, name=name)

    # ------------------------------------ Pooling ------------------------------------ #

    def max_pool_2d(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._max_pool_2d, **kwargs), ['input'], kwargs['name'], [message])
    def _max_pool_2d(self, name, input, kernel=(2, 2), stride=(2, 2), keep_size=True, if_global=False):
        if self.channel_major:
            format = 'NCHW'
            h, w = input[0][2:]
        else:
            format = 'NHWC'
            h, w = input[0][1:3]
        if if_global:
            kernel = (h, w)
            padding = (0, 0)
        else:
            if keep_size:
                y = ceil(((ceil(h / stride[0]) - 1) * stride[0] + kernel[0] - h) / 2)
                x = ceil(((ceil(w / stride[1]) - 1) * stride[1] + kernel[1] - w) / 2)
                padding = (y, x)
            else:
                padding = (0, 0)
        return nn.MaxPool2D(pool_size=kernel, strides=stride, padding=padding, ceil_mode=True, layout=format)

    def avg_pool_2d(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._avg_pool_2d, **kwargs), ['input'], kwargs['name'], [message])
    def _avg_pool_2d(self, name, input, kernel=(2, 2), stride=(2, 2), keep_size=True, if_global=False):
        if self.channel_major:
            format = 'NCHW'
            h, w = input[0][2:]
        else:
            format = 'NHWC'
            h, w = input[0][1:3]
        if if_global:
            kernel = (h, w)
            padding = (0, 0)
        else:
            if keep_size:
                y = ceil(((ceil(h / stride[0]) - 1) * stride[0] + kernel[0] - h) / 2)
                x = ceil(((ceil(w / stride[1]) - 1) * stride[1] + kernel[1] - w) / 2)
                padding = (y, x)
            else:
                padding = (0, 0)
        return nn.AvgPool2D(pool_size=kernel, strides=stride, padding=padding, ceil_mode=True, layout=format)

    # ------------------------------------ Reshape ------------------------------------ #

    # def reshape(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._reshape, **kwargs), ['input'], kwargs['name'], [message])
    # def _reshape(self, name, input, shape):
    #     return tf.reshape(input, shape, name)
    #
    def flat(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._flat, **kwargs), ['input'], kwargs['name'], [message])
    def _flat(self, name, input):
        return nn.Flatten()
    #
    # def slice(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._slice, **kwargs), ['input'], kwargs['name'], [message])
    # def _slice(self, name, input, indices):
    #     for d in range(len(indices)):
    #         output = input[indices[d][0]:indices[d][1]]
    #     return tf.identity(output, name)
    #
    # def pad(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._pad, **kwargs), ['input'], kwargs['name'], [message])
    # def _pad(self, name, input, margin, fill_in=0):
    #     return tf.pad(input, margin, constant_values=fill_in, name=name)
    #
    # # -------------------------------------- Arithmetic -------------------------------------- #
    #
    # def clip(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._clip, **kwargs), ['input'], kwargs['name'], [message])
    # def _clip(self, name, input, min_max_vals):
    #     return tf.clip_by_value(input, min_max_vals[0], min_max_vals[1], name)

    def dense(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._dense, **kwargs), ['input'], kwargs['name'], [message])
    def _dense(self, name, input, out_chs, w_init='xavier', w_param=None,
               b_init='zero', b_param=None, w_reg='l2', b_reg='l2'):
        if not w_init is None:
            w_init = self._getInitializer(w_init, w_param, w_reg)
        if not b_init is None:
            use_bias = True
            b_init = self._getInitializer(b_init, b_param, b_reg)
        else:
            use_bias = False
        return nn.Dense(out_chs, use_bias=use_bias, flatten=False, weight_initializer=w_init, bias_initializer=b_init)

    # def argmax(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._argmax, **kwargs), ['input'], kwargs['name'], [message])
    # def _argmax(self, name, input, axis):
    #     return tf.argmax(input, axis, name=name)
    #
    # # ------------------------------------ Image Manipulation ------------------------------------ #
    #
    # def resize(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._resize, **kwargs), ['input'], kwargs['name'], [message])
    # def _resize(self, name, input, size, method='bilinear'):
    #     if method == 'bilinear':
    #         return tf.image.resize_bilinear(input, size, name=name)
    #     elif method == 'bicubic':
    #         return tf.image.resize_bicubic(input, size, name=name)
    #     elif method == 'crop':
    #         return tf.image.resize_image_with_crop_or_pad(input, size, name=name)
    #     else:
    #         raise KeyError('NEBULAE ERROR ⨷ %s is not a legal resize method.' % method)
    #
    #
    # # ------------------------------------ Redefine or Rename ------------------------------------ #
    #
    def duplicate(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._duplicate, **kwargs), ['input'], kwargs['name'], [message])
    def _duplicate(self, name, input):
        return Duplicate()
    #
    # def convert(self, **kwargs):
    #     message = kwargs.get('input', '_INPUT')
    #     return Pod(partial(self._convert, **kwargs), ['input'], kwargs['name'], [message])
    # def _convert(self, name, input, dtype, trainable=False):
    #     '''
    #     convert data type or convert list/numpy array to tensor
    #     :param name:
    #     :param input: input tensor / list / numpy array
    #     :param dtype:
    #     :param trainable: if tensor is trainable
    #     :return: tensor
    #     '''
    #     if isinstance(input, (tf.Tensor, tf.SparseTensor, tf.Variable)):
    #         return tf.cast(input, tf.as_dtype(dtype), name=name)
    #     else:
    #         return tf.Variable(input, trainable=trainable, name=name)

    # ------------------------------------ Loss ------------------------------------ #

    def weight_decay(self, **kwargs):
        return Pod(partial(self._weight_decay, **kwargs), ['penalty'], kwargs['name'],
                   [nd.ones((1)) * kwargs['penalty']])
    def _weight_decay(self, name, penalty, decay_scope=None):
        if not decay_scope is None:
            raise Exception('NEBULAE ERROR ⨷ weight decay cannot be manipulated explicitly in MXNET core.')
        return MXwd()

    def sigm_xentropy(self, **kwargs):
        message = []
        message.append(kwargs.get('input', '_INPUT'))
        message.append(kwargs.get('label', '_LABEL'))
        return Pod(partial(self._sigm_xentropy, **kwargs), ['input', 'label'], kwargs['name'], message)
    def _sigm_xentropy(self, name, input, label):
        return MXsigmxe()

    def sftm_xentropy(self, **kwargs):
        message = []
        message.append(kwargs.get('input', '_INPUT'))
        message.append(kwargs.get('label', '_LABEL'))
        return Pod(partial(self._sftm_xentropy, **kwargs), ['input', 'label'], kwargs['name'], message)
    def _sftm_xentropy(self, name, input, label, is_one_hot):
        return MXsftmxe(is_one_hot)

    def mse(self, **kwargs):
        message = []
        message.append(kwargs.get('input', '_INPUT'))
        message.append(kwargs.get('label', '_LABEL'))
        return Pod(partial(self._mse, **kwargs), ['input', 'label'], kwargs['name'], message)
    def _mse(self, name, input, label):
        return MXmse()

    def mae(self, **kwargs):
        message = []
        message.append(kwargs.get('input', '_INPUT'))
        message.append(kwargs.get('label', '_LABEL'))
        return Pod(partial(self._mae, **kwargs), ['input', 'label'], kwargs['name'], message)
    def _mae(self, name, input, label):
        return MXmae()

    # ------------------------------------ Optimizer ------------------------------------ #

    def _lrStrategy(self, lr, lr_decay, miles, param):
        if lr_decay == 'exp':
            return lr_scheduler.FactorScheduler(step=miles, factor=param, base_lr=lr)
        elif lr_decay == 'poly':
            return lr_scheduler.PolyScheduler(max_update=miles, base_lr=lr, pwr=param)
        elif lr_decay == 'cosine':
            pass  #return tf.train.polynomial_decay(lr, mileage, miles, power=param, cycle=True)
        elif lr_decay == 'stair':
            pass  #return tf.train.piecewise_constant(mileage, [i*param for i in range(1, len(lr))], lr)
        else:
            raise KeyError('NEBULAE ERROR ⨷ %s decay is not supported or defined.' % lr_decay)

    def momentum(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._momentum, **kwargs), ['input', 'media'], kwargs['name'], [message, '_MEDIA'])
    def _momentum(self, name, lr, input=None, mmnt=0.9, update_scope=None, ignore_name=None,
                  lr_decay=None, lr_miles=None, decay_param=None, grad_limit=None, media=None):
        recordConfig(os.path.join(os.getcwd(), 'temp_config.json'),
                     {'lr': lr, 'mmnt': mmnt, 'update_scope': update_scope, 'ignore_name': ignore_name,
                      'lr_decay': lr_decay, 'lr_miles': lr_miles, 'decay_param': decay_param, 'grad_limit': grad_limit})
        # N.B. media is network and wd factor
        mod_params, wd = media
        wd = wd.asscalar()
        if isinstance(lr_decay, str):
            lr_s = self._lrStrategy(lr, lr_decay, lr_miles, decay_param)
        else:
            lr_s = lr_scheduler.LRScheduler(base_lr=lr)
        optz = Trainer(mod_params, 'SGD',
                       {'learning_rate': lr, 'momentum': mmnt, 'wd': wd,
                        'lr_scheduler': lr_s, 'clip_gradient': grad_limit})
        return optz

    def nesterov(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._nesterov, **kwargs), ['input', 'media'], kwargs['name'], [message, '_MEDIA'])
    def _nesterov(self, name, lr, input=None, mmnt=0.9, update_scope=None, ignore_name=None,
                  lr_decay=None, lr_miles=None, decay_param=None, grad_limit=None, media=None):

        recordConfig(os.path.join(os.getcwd(), 'temp_config.json'),
                     {'lr': lr, 'mmnt': mmnt, 'update_scope': update_scope, 'ignore_name': ignore_name,
                      'lr_decay': lr_decay, 'lr_miles': lr_miles, 'decay_param': decay_param, 'grad_limit': grad_limit})
        # N.B. media is network and wd factor
        mod_params, wd = media
        wd = wd.asscalar()
        if isinstance(lr_decay, str):
            lr_s = self._lrStrategy(lr, lr_decay, lr_miles, decay_param)
        else:
            lr_s = lr_scheduler.LRScheduler(base_lr=lr)
        optz = Trainer(mod_params, 'NAG',
                       {'learning_rate': lr, 'momentum': mmnt, 'wd': wd,
                        'lr_scheduler': lr_s, 'clip_gradient': grad_limit})
        return optz

    def adam(self, **kwargs):
        message = kwargs.get('input', '_INPUT')
        return Pod(partial(self._adam, **kwargs), ['input', 'media'], kwargs['name'], [message, '_MEDIA'])
    def _adam(self, name, lr, input=None, mmnt1=0.9, mmnt2=0.999, update_scope=None, ignore_name=None,
                  lr_decay=None, lr_miles=None, decay_param=None, grad_limit=None, media=None):
        recordConfig(os.path.join(os.getcwd(), 'temp_config.json'),
                     {'lr': lr, 'mmnt1': mmnt1, 'mmnt2': mmnt2, 'update_scope': update_scope,
                      'ignore_name': ignore_name, 'lr_decay': lr_decay, 'lr_miles': lr_miles,
                      'decay_param': decay_param, 'grad_limit': grad_limit})
        # N.B. media is network and wd factor
        mod_params, wd = media
        wd = wd.asscalar()
        if isinstance(lr_decay, str):
            lr_s = self._lrStrategy(lr, lr_decay, lr_miles, decay_param)
        else:
            lr_s = lr_scheduler.LRScheduler(base_lr=lr)
        optz = Trainer(mod_params, 'Adam',
                       {'learning_rate': lr, 'beta1': mmnt1, 'beta2': mmnt2, 'wd': wd,
                        'lr_scheduler': lr_s, 'clip_gradient': grad_limit})
        return optz

    # ------------------------------------ Metric ------------------------------------ #

    def accuracy_cls(self, **kwargs):
        message = []
        message.append(kwargs.get('input', '_INPUT'))
        message.append(kwargs.get('label', '_LABEL'))
        return Pod(partial(self._accuracy_cls, **kwargs), ['input', 'label'], kwargs['name'], message)
    def _accuracy_cls(self, name, input, label, multi_class=False, is_one_hot=False):
        return AccuracyCLS(multi_class, is_one_hot)