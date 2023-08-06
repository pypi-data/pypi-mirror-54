===========
 User guide
===========

Using as a feature extractor
----------------------------

In this example we take the output of the layer `fc7` of the VGG face model as
features.

.. doctest:: caffetest

   >>> import numpy
   >>> import bob.ip.caffe_extractor
   >>> import bob.io.base
   >>> from bob.io.base.test_utils import datafile
   >>> image = bob.io.base.load(datafile('8821.hdf5', 'bob.ip.caffe_extractor'))
   >>> caffe_extractor = bob.ip.caffe_extractor.VGGFace("fc7")
   >>> numpy.allclose(
   ...     caffe_extractor(image)[0:5],
   ...     [ -0.55280668, 12.35865498, -1.54516554, -13.75179005, 2.49704885],
   ...     rtol=1e-04, atol=1e-05)
   True

.. note::

   The models will automatically download to the data folder of this package as
   soon as you start using them.

Using as a convolutional filter
-------------------------------

In this example we plot some outputs of the convolutional layer `conv2_1`.

.. plot:: plot/convolve.py
   :include-source: False
