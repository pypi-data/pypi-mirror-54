import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="denseblock",
	version="1.1",
	author="Whitman Bohorquez",
	author_email="whitman-2@hotmail.com",
	description="Keras Extended Dense Layer",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ElPapi42/DenseBlock",
	download_url = 'https://github.com/ElPapi42/DenseBlock/archive/v1.1.tar.gz',
	keywords = ['Keras', 'Model', 'Plug And Play'],
	packages=setuptools.find_packages(),
	install_requires=[
		"tensorflow-gpu"
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
)