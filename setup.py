import setuptools


with open('readme.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='guildclone',
	version='1.0.0',
	author='saviour',
	description='discord bot for cloning channels and roles of a server',
	long_description=long_description,
	long_description_content_type='text/markdown', 
	url='https://github.com/s-viour/guildclone',
	packages=setuptools.find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	python_requires='>=3.5.3'
)