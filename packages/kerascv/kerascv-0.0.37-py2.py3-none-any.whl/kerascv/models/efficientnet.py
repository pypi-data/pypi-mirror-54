"""
    EfficientNet for ImageNet-1K, implemented in Keras.
    Original paper: 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.
"""

__all__ = ['efficientnet_model', 'efficientnet_b0', 'efficientnet_b1', 'efficientnet_b2', 'efficientnet_b3',
           'efficientnet_b4', 'efficientnet_b5', 'efficientnet_b6', 'efficientnet_b7', 'efficientnet_b0b',
           'efficientnet_b1b', 'efficientnet_b2b', 'efficientnet_b3b', 'efficientnet_b4b', 'efficientnet_b5b',
           'efficientnet_b6b', 'efficientnet_b7b']

import os
import math
from keras import layers as nn
from keras.models import Model
from .common import is_channels_first, conv1x1_block, conv3x3_block, dwconv3x3_block, dwconv5x5_block, se_block


def calc_tf_padding(x,
                    kernel_size,
                    strides=1,
                    dilation=1):
    """
    Calculate TF-same like padding size.

    Parameters:
    ----------
    x : tensor
        Input tensor.
    kernel_size : int
        Convolution window size.
    strides : int, default 1
        Strides of the convolution.
    dilation : int, default 1
        Dilation value for convolution layer.

    Returns
    -------
    tuple of 4 int
        The size of the padding.
    """
    height, width = x.shape[2:]
    oh = math.ceil(height / strides)
    ow = math.ceil(width / strides)
    pad_h = max((oh - 1) * strides + (kernel_size - 1) * dilation + 1 - height, 0)
    pad_w = max((ow - 1) * strides + (kernel_size - 1) * dilation + 1 - width, 0)
    return (pad_h // 2, pad_h - pad_h // 2), (pad_w // 2, pad_w - pad_w // 2)


def round_channels(channels,
                   factor,
                   divisor=8):
    """
    Round weighted channel number.

    Parameters:
    ----------
    channels : int
        Original number of channels.
    factor : float
        Weight factor.
    divisor : int
        Alignment value.

    Returns
    -------
    int
        Weighted number of channels.
    """
    channels *= factor
    new_channels = max(int(channels + divisor / 2.0) // divisor * divisor, divisor)
    if new_channels < 0.9 * channels:
        new_channels += divisor
    return new_channels


def effi_dws_conv_unit(x,
                       in_channels,
                       out_channels,
                       strides,
                       bn_epsilon,
                       activation,
                       tf_mode,
                       name="effi_dws_conv_unit"):
    """
    EfficientNet specific depthwise separable convolution block/unit with BatchNorms and activations at each convolution
    layers.

    Parameters:
    ----------
    x : keras.backend tensor/variable/symbol
        Input tensor/variable/symbol.
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    strides : int or tuple/list of 2 int
        Strides of the second convolution layer.
    bn_epsilon : float
        Small float added to variance in Batch norm.
    activation : str
        Name of activation function.
    tf_mode : bool
        Whether to use TF-like mode.
    name : str, default 'effi_dws_conv_unit'
        Block name.

    Returns
    -------
    keras.backend tensor/variable/symbol
        Resulted tensor/variable/symbol.
    """
    residual = (in_channels == out_channels) and (strides == 1)

    if residual:
        identity = x

    if tf_mode:
        x = nn.ZeroPadding2D(
            padding=calc_tf_padding(x, kernel_size=3),
            name=name + "/dw_conv_pad")(x)
    x = dwconv3x3_block(
        x=x,
        in_channels=in_channels,
        out_channels=in_channels,
        padding=(0 if tf_mode else 1),
        bn_epsilon=bn_epsilon,
        activation=activation,
        name=name + "/dw_conv")
    x = se_block(
        x=x,
        channels=in_channels,
        reduction=4,
        activation=activation,
        name=name + "/se")
    x = conv1x1_block(
        x=x,
        in_channels=in_channels,
        out_channels=out_channels,
        bn_epsilon=bn_epsilon,
        activation=None,
        name=name + "/pw_conv")

    if residual:
        x = nn.add([x, identity], name=name + "/add")

    return x


def effi_inv_res_unit(x,
                      in_channels,
                      out_channels,
                      kernel_size,
                      strides,
                      expansion_factor,
                      bn_epsilon,
                      activation,
                      tf_mode,
                      name="effi_inv_res_unit"):
    """
    EfficientNet inverted residual unit.

    Parameters:
    ----------
    x : keras.backend tensor/variable/symbol
        Input tensor/variable/symbol.
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    kernel_size : int or tuple/list of 2 int
        Convolution window size.
    strides : int or tuple/list of 2 int
        Strides of the convolution.
    expansion_factor : int
        Factor for expansion of channels.
    bn_epsilon : float
        Small float added to variance in Batch norm.
    activation : str
        Name of activation function.
    tf_mode : bool
        Whether to use TF-like mode.
    name : str, default 'effi_inv_res_unit'
        Unit name.

    Returns
    -------
    keras.backend tensor/variable/symbol
        Resulted tensor/variable/symbol.
    """
    residual = (in_channels == out_channels) and (strides == 1)
    mid_channels = in_channels * expansion_factor
    dwconv_block_fn = dwconv3x3_block if kernel_size == 3 else (dwconv5x5_block if kernel_size == 5 else None)

    if residual:
        identity = x

    x = conv1x1_block(
        x=x,
        in_channels=in_channels,
        out_channels=mid_channels,
        bn_epsilon=bn_epsilon,
        activation=activation,
        name=name + "/conv1")
    if tf_mode:
        x = nn.ZeroPadding2D(
            padding=calc_tf_padding(x, kernel_size=kernel_size, strides=strides),
            name=name + "/conv2_pad")(x)
    x = dwconv_block_fn(
        x=x,
        in_channels=mid_channels,
        out_channels=mid_channels,
        strides=strides,
        padding=(0 if tf_mode else (kernel_size // 2)),
        bn_epsilon=bn_epsilon,
        activation=activation,
        name=name + "/conv2")
    x = se_block(
        x=x,
        channels=mid_channels,
        reduction=24,
        activation=activation,
        name=name + "/se")
    x = conv1x1_block(
        x=x,
        in_channels=mid_channels,
        out_channels=out_channels,
        bn_epsilon=bn_epsilon,
        activation=None,
        name=name + "/conv3")

    if residual:
        x = nn.add([x, identity], name=name + "/add")

    return x


def effi_init_block(x,
                    in_channels,
                    out_channels,
                    bn_epsilon,
                    activation,
                    tf_mode,
                    name="effi_init_block"):
    """
    EfficientNet specific initial block.

    Parameters:
    ----------
    x : keras.backend tensor/variable/symbol
        Input tensor/variable/symbol.
    in_channels : int
        Number of input channels.
    out_channels : int
        Number of output channels.
    bn_epsilon : float
        Small float added to variance in Batch norm.
    activation : str
        Name of activation function.
    tf_mode : bool
        Whether to use TF-like mode.
    name : str, default 'effi_init_block'
        Block name.

    Returns
    -------
    keras.backend tensor/variable/symbol
        Resulted tensor/variable/symbol.
    """
    if tf_mode:
        x = nn.ZeroPadding2D(
            padding=calc_tf_padding(x, kernel_size=3, strides=2),
            name=name + "/conv_pad")(x)
    x = conv3x3_block(
        x=x,
        in_channels=in_channels,
        out_channels=out_channels,
        strides=2,
        padding=(0 if tf_mode else 1),
        bn_epsilon=bn_epsilon,
        activation=activation,
        name=name + "/conv")
    return x


def efficientnet_model(channels,
                       init_block_channels,
                       final_block_channels,
                       kernel_sizes,
                       strides_per_stage,
                       expansion_factors,
                       dropout_rate=0.2,
                       tf_mode=False,
                       bn_epsilon=1e-5,
                       in_channels=3,
                       in_size=(224, 224),
                       classes=1000):
    """
    EfficientNet(-B0) model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    channels : list of list of int
        Number of output channels for each unit.
    init_block_channels : list of 2 int
        Numbers of output channels for the initial unit.
    final_block_channels : int
        Number of output channels for the final block of the feature extractor.
    kernel_sizes : list of list of int
        Number of kernel sizes for each unit.
    strides_per_stage : list int
        Stride value for the first unit of each stage.
    expansion_factors : list of list of int
        Number of expansion factors for each unit.
    dropout_rate : float, default 0.2
        Fraction of the input units to drop. Must be a number between 0 and 1.
    tf_mode : bool, default False
        Whether to use TF-like mode.
    bn_epsilon : float, default 1e-5
        Small float added to variance in Batch norm.
    in_channels : int, default 3
        Number of input channels.
    in_size : tuple of two ints, default (224, 224)
        Spatial size of the expected input image.
    classes : int, default 1000
        Number of classification classes.
    """
    input_shape = (in_channels, in_size[0], in_size[1]) if is_channels_first() else\
        (in_size[0], in_size[1], in_channels)
    input = nn.Input(shape=input_shape)
    activation = "swish"

    x = effi_init_block(
        x=input,
        in_channels=in_channels,
        out_channels=init_block_channels,
        bn_epsilon=bn_epsilon,
        activation=activation,
        tf_mode=tf_mode,
        name="features/init_block")
    in_channels = init_block_channels
    for i, channels_per_stage in enumerate(channels):
        kernel_sizes_per_stage = kernel_sizes[i]
        expansion_factors_per_stage = expansion_factors[i]
        for j, out_channels in enumerate(channels_per_stage):
            kernel_size = kernel_sizes_per_stage[j]
            expansion_factor = expansion_factors_per_stage[j]
            strides = strides_per_stage[i] if (j == 0) else 1
            if i == 0:
                x = effi_dws_conv_unit(
                    x=x,
                    in_channels=in_channels,
                    out_channels=out_channels,
                    strides=strides,
                    bn_epsilon=bn_epsilon,
                    activation=activation,
                    tf_mode=tf_mode,
                    name="features/stage{}/unit{}".format(i + 1, j + 1))
            else:
                x = effi_inv_res_unit(
                    x=x,
                    in_channels=in_channels,
                    out_channels=out_channels,
                    kernel_size=kernel_size,
                    strides=strides,
                    expansion_factor=expansion_factor,
                    bn_epsilon=bn_epsilon,
                    activation=activation,
                    tf_mode=tf_mode,
                    name="features/stage{}/unit{}".format(i + 1, j + 1))
            in_channels = out_channels
    x = conv1x1_block(
        x=x,
        in_channels=in_channels,
        out_channels=final_block_channels,
        bn_epsilon=bn_epsilon,
        activation=activation,
        name="features/final_block")
    in_channels = final_block_channels
    x = nn.GlobalAveragePooling2D(
        name="features/final_pool")(x)

    if dropout_rate > 0.0:
        x = nn.Dropout(
            rate=dropout_rate,
            name="output/dropout")(x)
    x = nn.Dense(
        units=classes,
        input_dim=in_channels,
        name="output/fc")(x)

    model = Model(inputs=input, outputs=x)
    model.in_size = in_size
    model.classes = classes
    return model


def get_efficientnet(version,
                     in_size,
                     tf_mode=False,
                     bn_epsilon=1e-5,
                     model_name=None,
                     pretrained=False,
                     root=os.path.join("~", ".keras", "models"),
                     **kwargs):
    """
    Create EfficientNet model with specific parameters.

    Parameters:
    ----------
    version : str
        Version of EfficientNet ('b0'...'b7').
    in_size : tuple of two ints
        Spatial size of the expected input image.
    tf_mode : bool, default False
        Whether to use TF-like mode.
    bn_epsilon : float, default 1e-5
        Small float added to variance in Batch norm.
    model_name : str or None, default None
        Model name for loading pretrained model.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """

    if version == "b0":
        assert (in_size == (224, 224))
        depth_factor = 1.0
        width_factor = 1.0
        dropout_rate = 0.2
    elif version == "b1":
        assert (in_size == (240, 240))
        depth_factor = 1.1
        width_factor = 1.0
        dropout_rate = 0.2
    elif version == "b2":
        assert (in_size == (260, 260))
        depth_factor = 1.2
        width_factor = 1.1
        dropout_rate = 0.3
    elif version == "b3":
        assert (in_size == (300, 300))
        depth_factor = 1.4
        width_factor = 1.2
        dropout_rate = 0.3
    elif version == "b4":
        assert (in_size == (380, 380))
        depth_factor = 1.8
        width_factor = 1.4
        dropout_rate = 0.4
    elif version == "b5":
        assert (in_size == (456, 456))
        depth_factor = 2.2
        width_factor = 1.6
        dropout_rate = 0.4
    elif version == "b6":
        assert (in_size == (528, 528))
        depth_factor = 2.6
        width_factor = 1.8
        dropout_rate = 0.5
    elif version == "b7":
        assert (in_size == (600, 600))
        depth_factor = 3.1
        width_factor = 2.0
        dropout_rate = 0.5
    else:
        raise ValueError("Unsupported EfficientNet version {}".format(version))

    init_block_channels = 32
    layers = [1, 2, 2, 3, 3, 4, 1]
    downsample = [1, 1, 1, 1, 0, 1, 0]
    channels_per_layers = [16, 24, 40, 80, 112, 192, 320]
    expansion_factors_per_layers = [1, 6, 6, 6, 6, 6, 6]
    kernel_sizes_per_layers = [3, 3, 5, 3, 5, 5, 3]
    strides_per_stage = [1, 2, 2, 2, 1, 2, 1]
    final_block_channels = 1280

    layers = [int(math.ceil(li * depth_factor)) for li in layers]
    channels_per_layers = [round_channels(ci, width_factor) for ci in channels_per_layers]

    from functools import reduce
    channels = reduce(lambda x, y: x + [[y[0]] * y[1]] if y[2] != 0 else x[:-1] + [x[-1] + [y[0]] * y[1]],
                      zip(channels_per_layers, layers, downsample), [])
    kernel_sizes = reduce(lambda x, y: x + [[y[0]] * y[1]] if y[2] != 0 else x[:-1] + [x[-1] + [y[0]] * y[1]],
                          zip(kernel_sizes_per_layers, layers, downsample), [])
    expansion_factors = reduce(lambda x, y: x + [[y[0]] * y[1]] if y[2] != 0 else x[:-1] + [x[-1] + [y[0]] * y[1]],
                               zip(expansion_factors_per_layers, layers, downsample), [])
    strides_per_stage = reduce(lambda x, y: x + [[y[0]] * y[1]] if y[2] != 0 else x[:-1] + [x[-1] + [y[0]] * y[1]],
                               zip(strides_per_stage, layers, downsample), [])
    strides_per_stage = [si[0] for si in strides_per_stage]

    init_block_channels = round_channels(init_block_channels, width_factor)

    if width_factor > 1.0:
        assert (int(final_block_channels * width_factor) == round_channels(final_block_channels, width_factor))
        final_block_channels = round_channels(final_block_channels, width_factor)

    net = efficientnet_model(
        channels=channels,
        init_block_channels=init_block_channels,
        final_block_channels=final_block_channels,
        kernel_sizes=kernel_sizes,
        strides_per_stage=strides_per_stage,
        expansion_factors=expansion_factors,
        dropout_rate=dropout_rate,
        tf_mode=tf_mode,
        bn_epsilon=bn_epsilon,
        in_size=in_size,
        **kwargs)

    if pretrained:
        if (model_name is None) or (not model_name):
            raise ValueError("Parameter `model_name` should be properly initialized for loading pretrained model.")
        from .model_store import download_model
        download_model(
            net=net,
            model_name=model_name,
            local_model_store_dir_path=root)

    return net


def efficientnet_b0(in_size=(224, 224), **kwargs):
    """
    EfficientNet-B0 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (224, 224)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b0", in_size=in_size, model_name="efficientnet_b0", **kwargs)


def efficientnet_b1(in_size=(240, 240), **kwargs):
    """
    EfficientNet-B1 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (240, 240)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b1", in_size=in_size, model_name="efficientnet_b1", **kwargs)


def efficientnet_b2(in_size=(260, 260), **kwargs):
    """
    EfficientNet-B2 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (260, 260)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b2", in_size=in_size, model_name="efficientnet_b2", **kwargs)


def efficientnet_b3(in_size=(300, 300), **kwargs):
    """
    EfficientNet-B3 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (300, 300)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b3", in_size=in_size, model_name="efficientnet_b3", **kwargs)


def efficientnet_b4(in_size=(380, 380), **kwargs):
    """
    EfficientNet-B4 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (380, 380)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b4", in_size=in_size, model_name="efficientnet_b4", **kwargs)


def efficientnet_b5(in_size=(456, 456), **kwargs):
    """
    EfficientNet-B5 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (456, 456)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b5", in_size=in_size, model_name="efficientnet_b5", **kwargs)


def efficientnet_b6(in_size=(528, 528), **kwargs):
    """
    EfficientNet-B6 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (528, 528)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b6", in_size=in_size, model_name="efficientnet_b6", **kwargs)


def efficientnet_b7(in_size=(600, 600), **kwargs):
    """
    EfficientNet-B7 model from 'EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,'
    https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (600, 600)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b7", in_size=in_size, model_name="efficientnet_b7", **kwargs)


def efficientnet_b0b(in_size=(224, 224), **kwargs):
    """
    EfficientNet-B0-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (224, 224)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b0", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b0b",
                            **kwargs)


def efficientnet_b1b(in_size=(240, 240), **kwargs):
    """
    EfficientNet-B1-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (240, 240)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b1", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b1b",
                            **kwargs)


def efficientnet_b2b(in_size=(260, 260), **kwargs):
    """
    EfficientNet-B2-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (260, 260)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b2", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b2b",
                            **kwargs)


def efficientnet_b3b(in_size=(300, 300), **kwargs):
    """
    EfficientNet-B3-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (300, 300)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b3", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b3b",
                            **kwargs)


def efficientnet_b4b(in_size=(380, 380), **kwargs):
    """
    EfficientNet-B4-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (380, 380)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b4", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b4b",
                            **kwargs)


def efficientnet_b5b(in_size=(456, 456), **kwargs):
    """
    EfficientNet-B5-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (456, 456)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b5", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b5b",
                            **kwargs)


def efficientnet_b6b(in_size=(528, 528), **kwargs):
    """
    EfficientNet-B6-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (528, 528)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b6", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b6b",
                            **kwargs)


def efficientnet_b7b(in_size=(600, 600), **kwargs):
    """
    EfficientNet-B7-b (like TF-implementation) model from 'EfficientNet: Rethinking Model Scaling for Convolutional
    Neural Networks,' https://arxiv.org/abs/1905.11946.

    Parameters:
    ----------
    in_size : tuple of two ints, default (600, 600)
        Spatial size of the expected input image.
    pretrained : bool, default False
        Whether to load the pretrained weights for model.
    root : str, default '~/.keras/models'
        Location for keeping the model parameters.
    """
    return get_efficientnet(version="b7", in_size=in_size, tf_mode=True, bn_epsilon=1e-3, model_name="efficientnet_b7b",
                            **kwargs)


def _test():
    import numpy as np
    import keras

    pretrained = False

    models = [
        efficientnet_b0,
        efficientnet_b1,
        efficientnet_b2,
        efficientnet_b3,
        efficientnet_b4,
        efficientnet_b5,
        efficientnet_b6,
        efficientnet_b7,
        efficientnet_b0b,
        efficientnet_b1b,
        efficientnet_b2b,
        efficientnet_b3b,
        efficientnet_b4b,
        efficientnet_b5b,
        efficientnet_b6b,
        efficientnet_b7b,
    ]

    for model in models:
        net = model(pretrained=pretrained)
        # net.summary()
        weight_count = keras.utils.layer_utils.count_params(net.trainable_weights)
        print("m={}, {}".format(model.__name__, weight_count))
        assert (model != efficientnet_b0 or weight_count == 5288548)
        assert (model != efficientnet_b1 or weight_count == 7794184)
        assert (model != efficientnet_b2 or weight_count == 9109994)
        assert (model != efficientnet_b3 or weight_count == 12233232)
        assert (model != efficientnet_b4 or weight_count == 19341616)
        assert (model != efficientnet_b5 or weight_count == 30389784)
        assert (model != efficientnet_b6 or weight_count == 43040704)
        assert (model != efficientnet_b7 or weight_count == 66347960)
        assert (model != efficientnet_b0b or weight_count == 5288548)
        assert (model != efficientnet_b1b or weight_count == 7794184)
        assert (model != efficientnet_b2b or weight_count == 9109994)
        assert (model != efficientnet_b3b or weight_count == 12233232)
        assert (model != efficientnet_b4b or weight_count == 19341616)
        assert (model != efficientnet_b5b or weight_count == 30389784)
        assert (model != efficientnet_b6b or weight_count == 43040704)
        assert (model != efficientnet_b7b or weight_count == 66347960)

        if is_channels_first():
            x = np.zeros((1, 3, net.in_size[0], net.in_size[1]), np.float32)
        else:
            x = np.zeros((1, net.in_size[0], net.in_size[1], 3), np.float32)
        y = net.predict(x)
        assert (y.shape == (1, 1000))


if __name__ == "__main__":
    _test()
