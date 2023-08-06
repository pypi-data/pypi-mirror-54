
## Purpose

Quickly train 4 gestures for the model to learn. Press the UP, DOWN, RIGHT, and LEFT arrows on your keyboard to 'label' each gesture in realtime. After 30 seconds you'll be prompted to save (append) the new training data. It will immediately show you a cross-validation score of the fitted data.

Now see your gestures work in realtime! Run `predict_gesture.py.`

This was a personal 1-day challenge to create a relatively lightweight gesture tracking script. It doesn't use convolution. It's intended for fixed camera & fixed lighting setups.

##### Requirements
- Anaconda Python >= 3.7
- Mysql
- OSX

##### OSX

Before running `python setup.py install` on osx, run (takes a while):
```
brew install mysql
```

#### Non-OSX (Not Tested)
Install the latest version of mysql for your system.


##### Create a fresh environment and Run

```
conda create --name head python=3.7
conda activate head
# Navigate to the head_controller directory
python setup.py install
```

Then use:

```
python init_db.py
```

# Quickstart

Initialize, Train, and Predict in less than 60 seconds (using your webcam).
```
python init_db.py
python capture_features.py
python predict_gesture.py
```

##### Future Updates

- Add class for continuously updating the db with live gesture predictions.
- Add api for accessing live gestures from other programs.


#### Author:
- Dan Scott 2019
- MIT License
- email: danscottlearns@gmail.com

If you're interested in adding to this library or using it for a project - I would love to hear from you.
