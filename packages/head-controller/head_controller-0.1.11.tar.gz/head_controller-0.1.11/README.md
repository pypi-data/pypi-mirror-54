
# Quick Install

Install the library using Python's package manager `pip`.
```
pip install head-controller
```


## Purpose

Predict your webcam gestures in realtime!

Quickly train 4 gestures for the model to learn. Press the UP, DOWN, RIGHT, and LEFT arrows on your keyboard to 'label' each gesture in realtime. After 30 seconds you'll be prompted to save (append) the new training data. It will immediately show you a cross-validation score of the fitted data.

This model doesn't use convolution. It's intended for fixed camera & fixed lighting setups.

##### Requirements
- Anaconda Python >= 3.7

##### Manual Installation

```
conda create --name head python=3.7
conda activate head
# Navigate to the head_controller directory
python setup.py install
```

# Basic Usage

Import dependencies and start training from your webcam:
```
import head_controller.db as db
import head_controller.Camera as Camera

# Initialize gesture training data
db.setup_db()

# Capture webcam gestures with live arrow-key labelling.
# Hold DOWN, UP, RIGHT, or LEFT keys while gesturing into the camera.
Camera.capture_review_submit_labels()

# Realtime predict your webcam gestures.
Camera.check_video_frame_data_predict()
```

To append more training samples, simply run the following script over and over:
```
Camera.capture_review_submit_labels()
```

##### Future Updates

- Add class for continuously updating the db with live gesture predictions.
- Add api for accessing live gestures from other programs.


#### Author:
- Dan Scott 2019
- MIT License
- email: danscottlearns@gmail.com
- website: https://pypi.org/project/head-controller/

If you're interested in adding to this library or using it for a project - I would love to hear from you.
