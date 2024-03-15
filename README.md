What it does:
=============

You give it a picture of sheet music. The note-predictor tries to determine which notes are written down using a neural network (NN). Currently limited to whole notes between c1 and c2.


What you need:
==============

Aside from Python itself, you need the modules

- tensorflow
- pillow

Instal those, for example using pip.


How to use it:
==============

Replace the file "input.jpg" with your own sheet music (or use this example file). Text, including titles or composers, should be removed beforehand, eg using paint.

After making sure that all modules are properly installed, run
> python predict_notes.py

You should be presented with a prediction for what was written on the paper.


What could be coming in the future?
===================================

- extended range, including bass clef
- more complex rhythms and rests
- add a feature to remove text and similar "distractions" for the NN
- train the NN with more data
- usability in general would be nice
