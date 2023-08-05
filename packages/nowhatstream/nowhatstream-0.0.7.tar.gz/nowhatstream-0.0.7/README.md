# NoWhat Stream

## Informations

This is a module and can be plugged in to any flask app but require a api video key to work correctly

## Create a package

To create a package we will follow the tutorial written here: 
https://packaging.python.org/tutorials/packaging-projects/

We need to change the version of the package in setup.py


First we need to create a wheel package:

`python setup.py sdist bdist_wheel`

 Now it’s time to upload your package to the Python Package Index:
 
 `python3 -m twine upload dist/*`
 