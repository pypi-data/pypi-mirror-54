.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


============================
Idiap - Resnet V2 - MSCeleba
============================

Inspired by `**FaceNet** <https://github.com/davidsandberg/facenet>`_ we here at Idiap trained our own CNN using the Inception Resnet 2 architecture using MSCeleba database.
In this `link <https://gitlab.idiap.ch/bob/bob.bio.htface/blob/277781d9c99738ff141218e1ce04103f9a427b0c/bob/bio/htface/config/tensorflow/MSCELEBA_inception_resnet_v2_center_loss.py>`_ you can find the script that trains this neural network.

To trigger this training it's necessary to use the `bob.learn.tensorflow <http://gitlab.idiap.ch/bob/bob.learn.tensorflow/>`_ package and run the following command::

  $ ./bin/jman submit --name CELEB-GRAY --queue gpu -- bob_tf_train_generic MSCELEBA_inception_resnet_v2_center_loss_GRAY.py
  

Some quick details about this CNN (just as a mental note):

  - The hot encoded layer has 99879 neurons.
  - MSCeleba has a lot of mislabeling, a very simple prunning was implemented `in this python package <http://gitlab.idiap.ch/tiago.pereira/bob.db.msceleb>`_.
  - Faces were detected and croped to :math:`182 \times 182` using `MTCNN <https://gitlab.idiap.ch/bob/bob.ip.mtcnn>`_ face and landmark detector
  - The following data augmentation strategies were implemented:
     * Random crop to :math:`160 \times 160`
     * Random Flip
     * Images were normalized to have zero mean and standard deviation one
  - Learning rate of 0.01
  - Adagrad as Optimizer
  - Batch size of 16


Two versions of it were trained: one providing color images for training and another one providing  gray scale images.

