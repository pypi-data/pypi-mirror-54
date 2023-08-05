<div align="center">
  <a href="https://nanonets.com/">
    <img src="https://nanonets.com/logo.png" alt="The NanoNets API Python Wrapper" width="100"/>
    </a>
</div>

<h1 align="center">The NanoNets API Python Wrapper</h1>

** **

Nanonets provides an easy to use API to communicate with it's servers and build machine learning models and make predictions on image data. 
The models that can be built are - 
1. Image Classification
2. Multi-label Classification
3. Object Detection
4. OCR 

Check us out at https://nanonets.com. <br>
To find out about our GUI solution or to get your API key, check out https://app.nanonets.com

** **

## Installation

### Pip install - 
Run the following command from your terminal - 
```bash
pip install nanonets
```

### Setuptools - 
To install using setuptools, run the following commands from your terminal
```bash
git clone https://github.com/NanoNets/nanonets-python-wrapper.git
cd nanonets-python-wrapper
python setup.py install --user
```

** **

## Create Models - 
To create a new model
1. Head over to https://app.nanonets.com, login, click on the 'API Keys' tab on the left. 
2. Click on 'COPY KEY'
3. Create a model using the following python code
```python
from nanonets import ImageClassification

# from nanonets import MultilabelClassification
# from nanonets import ObjectDetection
# from nanonets import OCR

api_key = 'YOUR_API_KEY_GOES_HERE'
categories = ['list', 'of', 'your', 'labels']

model = ImageClassification(api_key, categories)
```

This will print a Model ID that you should note down for future reference. You can also find this out by visiting https://app.nanonets.com

** **

## Preparing training data
The training data, needs to be put into a dictionary format where 
* for image classification models - 
	* keys - filepaths/urls of images
	* values - labels for each image
* for multilabel classification models - 
	* keys - filepaths/urls of images
	* values - list of labels for each image
* for object detection models - 
	* keys - filepaths of images
	* values - annotation paths for each image (XML or JSON)
* for OCR models - 
	* keys - filepaths of images
	* values - annotation paths for each image (XML or JSON)

you can look into the data/annotations directory to get a better idea. 

** **

## Training and model status

To train a model on some training data - 
```python
model.train(training_dict, data_path_type='files')
```

The images will get uploaded and the training will get initialised after. 

You can check if the model is trained or not at anytime by running the following command from a python console - 
```python
api_key = 'YOUR_API_KEY_GOES_HERE'
categories = ['list', 'of', 'your', 'labels']
model_id = 'YOUR_MODEL_ID'

model = ImageClassification(api_key, categories, model_id=model_id)
model._check_model_state()
```
Or you can wait for Nanonets to email you once the training is finished. 

** **

## Inference
You can run inference on a single image or multiple images. You can use urls as well as local files. 

```python
api_key = 'YOUR_API_KEY_GOES_HERE'
categories = ['list', 'of', 'your', 'labels']
model_id = 'YOUR_MODEL_ID'

model = ImageClassification(api_key, categories, model_id=model_id)

## list of file paths of several test images
img_dir = 'PATH_TO_YOUR_IMAGES_DIR'
imglist = os.listdir(img_dir)
imglist = [img_dir + '/' + x for x in imglist]

## list of urls of several test images
urls = ['LIST', 'OF', 'YOUR', 'IMAGE', 'URLS']

## prediction functions for single file
resp_one_file = model.predict_for_file(imglist[0])
print("IC response - single image: ", resp_one_file)

## prediction functions for multiple files
resp_mul_files = model.predict_for_files(imglist)
print("IC response - multiple images: ", resp_mul_files)

## prediction functions for single url
resp_one_url = model.predict_for_url(urls[0])
print("IC response - single URL: ", resp_one_url)

## prediction functions for multiple urls
resp_mul_urls = model.predict_for_urls(urls)
print("IC response - multiple URLs: ", resp_mul_urls)
```

** **

 NOTE: The data in the ```data``` directory is meant to serve as examples and is generated randomly to demonstrate training and inference code in the ```examples``` directory. Use said data to understand the format requirements for the library and not for building models. 
