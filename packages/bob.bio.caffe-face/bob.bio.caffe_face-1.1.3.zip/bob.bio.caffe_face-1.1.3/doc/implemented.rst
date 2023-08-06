.. _bob.bio.caffe_face.implemented:

=======================================
Tools implemented in bob.bio.caffe_face
=======================================

Summary
-------

Face Image Feature Extractors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   bob.bio.caffe_face.extractor.VGGFeatures
   bob.bio.caffe_face.extractor.LightCNNExtractor


Face Image Preprocessors
~~~~~~~~~~~~~~~~~~~~~~~~

Several preprocessors are also available in this package that are recommended
to use with the implemented feature extractors in this package:
``'face-detect-vgg'``, ``'face-eyes-vgg'``, ``'face-detect-lightcnn'``,
``'face-eyes-lightcnn'``.


Detailed API
------------

.. automodule:: bob.bio.caffe_face

.. automodule:: bob.bio.caffe_face.extractor
   :special-members: __init__, __call__
