# Important Note

This code is an experiment to make a simple app that can find a reference image on the screen and click on it. It is written in Python and uses the PyAutoGUI and OpenCV libraries. The app is designed to automate simple, repetitive tasks that would otherwise be done by a human. It is not designed to be used in production environments. It's just a fun experiment.

# Installation

- replace the reference png in the data folder or optionally you can pass the path to the reference image as a command line argument (`python refact.py data/ref2.png`)
- install the dependencies: `pip install -r requirements.txt`
- run the app: `python main.py` or `python refact.py data/ref2.png`

# How it works

The app takes a screenshot of the screen and then uses OpenCV to find the reference image in the screenshot. If the reference image is found, the app will click on the center of the reference image. If the reference image is not found, the app will wait and try again. This process repeats until the application is stopped.
