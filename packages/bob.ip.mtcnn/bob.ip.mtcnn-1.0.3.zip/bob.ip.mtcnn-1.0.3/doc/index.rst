.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Fri 17 Jul 02:49:53 2016 CEST

.. _bob.ip.mtcnn:

====================================================
 Bob interface for mtcnn face and landmark detection
====================================================

This package binds the face and landmark detection from the paper:


    @ARTICLE{7553523, 
        author={K. Zhang and Z. Zhang and Z. Li and Y. Qiao}, 
        journal={IEEE Signal Processing Letters}, 
        title={Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks}, 
        year={2016}, 
        volume={23}, 
        number={10}, 
        pages={1499-1503}, 
        keywords={Benchmark testing;Computer architecture;Convolution;Detectors;Face;Face detection;Training;Cascaded convolutional neural network (CNN);face alignment;face detection}, 
        doi={10.1109/LSP.2016.2603342}, 
        ISSN={1070-9908}, 
        month={Oct},}


User guide
==========


Face Detection and Landmark detection
-------------------------------------

The most simple face detection task is to detect a single face in an image. This task can be achieved using a single command:

   >>> import bob.ip.mtcnn
   >>> import bob.io.base
   >>> import bob.io.base.test_utils
   >>> color_image = bob.io.base.load(bob.io.base.test_utils.datafile('testimage.jpg', 'bob.ip.facedetect'))
   >>> bounding_box, landmarks = bob.ip.mtcnn.FaceDetector().detect_single_face(color_image)
   >>> print(bounding_box.topleft)
   (64, 77)

.. plot:: plot/plot_single_faces.py
   :include-source: False



Multiple Face Detection
-----------------------

The detection of multiple faces can be achieved with a single command:

.. doctest:: mtcnntest

   >>> import bob.ip.mtcnn
   >>> import bob.io.base
   >>> import bob.io.base.test_utils
   >>> color_image = bob.io.base.load(bob.io.base.test_utils.datafile('multiple-faces.jpg', 'bob.ip.mtcnn'))
   >>> bounding_box, landmarks = bob.ip.mtcnn.FaceDetector().detect_all_faces(color_image)
   >>> print ((bounding_box[0].topleft, bounding_box[0].bottomright))
   ((28, 189), (102, 244))

.. plot:: plot/plot_multiple_faces.py
   :include-source: False


Landmark detection
------------------

The detection of landmarks can be done as the following:

.. doctest:: mtcnntest

   >>> import bob.ip.mtcnn
   >>> import bob.io.base
   >>> import bob.io.base.test_utils
   >>> color_image = bob.io.base.load(bob.io.base.test_utils.datafile('testimage.jpg', 'bob.ip.facedetect'))
   >>> bounding_box, landmarks = bob.ip.mtcnn.FaceDetector().detect_single_face(color_image)
   >>> print (landmarks['leye'])
   (174, 219)



Face genometric normalization
-----------------------------

The detection of landmarks can be done as the following:

.. doctest:: mtcnntest

   >>> import bob.ip.mtcnn
   >>> import bob.io.base
   >>> import bob.io.base.test_utils
   >>> color_image = bob.io.base.load(bob.io.base.test_utils.datafile('testimage.jpg', 'bob.ip.facedetect'))
   >>> color_image_norm = bob.ip.mtcnn.FaceDetector().detect_crop(color_image, final_image_size=(224, 224))
   >>> color_image_norm_align = bob.ip.mtcnn.FaceDetector().detect_crop_align(color_image, final_image_size=(224, 224))


.. plot:: plot/plot_align_faces.py
   :include-source: False





Python API
==========

.. toctree::
   :maxdepth: 2

   py_api
   references
