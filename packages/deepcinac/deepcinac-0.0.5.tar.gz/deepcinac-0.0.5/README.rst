=========
DeepCINAC
=========

DeepCINAC stands for Deep Calcium Imaging Neuronal Activity Classifier.

It's a deep-learning-based Python toolbox for inferring calcium imaging neuronal activity based on movie visualization.

The code is currently being cleaned and documented so the toolbox could be easily used and work for a wide variety of data.

Keep it mind that it is still a **beta** version.

Please let us know if you encounter any issue, we will be glad to help you.

Contact us at julien.denis3{at}gmail.com

BioRxiv paper
------------- 

https://www.biorxiv.org/content/10.1101/803726v1


Installation
------------

See the `installation page <https://deepcinac.readthedocs.io/en/latest/install.html>`_ of our documentation.


Predictions
-----------

The classifier takes as inputs the motion corrected calcium imaging movie and spatial footprints of the sources (cells).

The outputs are float values between 0 and 1 for each frame and each source,
representing the probability for a cell to be active at that given frame.

The classifier was trained to consider a cell as active during the rise time of its transients.


How to-use to infer neuronal activity
-------------------------------------

**On google colab**

If you just want to infer neuronal activity of your calcium imaging data
and you don't possess a GPU or don't want to go through the process of configuring your environment to make use of it,
you can run this `notebook <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/notebooks/demo_deepcinac_predictions.ipynb>`_
using `google colab <https://colab.research.google.com>`_.

Google provides free virtual machines for you to use: with about 12GB RAM and 50GB hard drive space, and TensorFlow is pre-installed.

You will need a google account. Upload the notebook on google colab, then just follow the instructions in the notebook to go through.

**On your local device**

You can follow the steps described in this `demo file <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/general/demo_deepcinac_predictions.py>`_. 

More informations in our `documentation <https://deepcinac.readthedocs.io/>`_.



Establishing ground truth and visualising predictions
----------------------------------------------------

A GUI (Graphical User Interface) offers the tools to carefully examine the activity of each cell
over the course of the recording.

Allows to:

* Play the calcium imaging movie between any given frames, zoomed on a cell, with the traces scrolling.

* Display the source and transient profiles of cells and correlation of any transient profile with the source profiles of overlapped cells, such as described in `Gauthier et al. <https://www.biorxiv.org/content/10.1101/473470v1.abstract>`_.

* Select / deselect active periods, allowing to establish a ground truth.

* Display the predictions of the network as well as neuronal activity inferred using other methods.

Check-out this video for a quick overview of the GUI: http://www.youtube.com/watch?v=Pz7xAUqszME


The code for the GUI is getting adapted to work for several types of data, a tutorial will be very soon available. 


Generating simulated calcium imaging movies
---------------------------------------------

Coming soon...


Training your classifier
---------------------

Coming soon...


Evaluating the performance of your classifier
---------------------------------------------

Coming soon...



Documentation
-------------

Documentation of DeepCINAC can be found `here <https://deepcinac.readthedocs.io/>`_.

