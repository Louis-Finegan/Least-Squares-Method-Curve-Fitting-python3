from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
   name='least_squares',
   version='1.0',
   description='Curvefitting different models over data using the method of least squares (From Scratch with numpy)',
   author='Louis Finegan',
   author_email='louis02finegan@gmail.com',
   packages=['least_squares'],
   install_requires=['numpy'],
   keywords=[
        'python', 
        'least-squares', 
        'curve-fitting', 
        'linear fit', 
        'exponential fit',
        'power fit',
        'limited exponential fit',
        'logistic curve fit'
        ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]           
)