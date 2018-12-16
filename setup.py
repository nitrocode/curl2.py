from setuptools import setup


setup(
    name='curltopy',
    version='0.1.2',
    author='',
    author_email='',
    description='Converts curl statements to python using command line',
    long_description=open('README.md').read(),
    url="https://github.com/nitrocode/curl2.py",
    packages=['curltopy'],
    scripts=['bin/curltopy']
)
