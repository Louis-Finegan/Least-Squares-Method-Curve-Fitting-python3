from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='least-squares',
   version='1.0',
   description='Curvefitting different models over data using the method of least squares (From Scratch with numpy)',
   author='Louis Finegan',
   author_email='louis02finegan@gmail.com',
   packages=['least-squares'],
   install_requires=['numpy'], #external packages as dependencies
)