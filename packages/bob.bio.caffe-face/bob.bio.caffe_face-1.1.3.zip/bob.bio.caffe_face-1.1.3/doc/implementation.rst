
======================
Implementation Details
======================

For more information about face recognition algorithms, please check :ref:`bob.bio.face <bob.bio.face>` which contains several different algorithms to perform photometric enhancement of facial images are implemented.

In this package several face feature extractors and their respective recommended preprocessors are available.

Feature extractors
~~~~~~~~~~~~~~~~~~

The following models are available:

* :any:`The VGG face model <bob.bio.caffe_face.extractor.VGGFeatures>` ( ``'vgg_features'``)
* :any:`The LightCNN face model <bob.bio.caffe_face.extractor.LightCNNExtractor>` (``'lightcnn'``)

Further models can be wrapped easily using the tools available in :ref:`bob.ip.caffe_extractor` and this package.
