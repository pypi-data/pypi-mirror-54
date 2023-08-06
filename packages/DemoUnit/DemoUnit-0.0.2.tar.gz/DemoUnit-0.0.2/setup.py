try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='DemoUnit',
    version='0.0.2',
    author='Shailesh Appukuttan, Andrew Davison',
    author_email='shailesh.appukuttan@unic.cnrs-gif.fr',
    packages=['DemoUnit',
              'DemoUnit.tests',
              'DemoUnit.capabilities'],
    url='https://github.com/appukuttan-shailesh/DemoUnit',
    keywords = ['electrophysiology', 'electrical', 'testing', 'validation framework'],
    license='MIT',
    description='A SciUnit library for data-driven testing of neurons.'
)
