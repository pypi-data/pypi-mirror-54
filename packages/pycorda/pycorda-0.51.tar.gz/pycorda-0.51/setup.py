from setuptools import setup

setup(
	name='pycorda',
	version='0.51',
	author='Jamiel Sheikh',
	packages=['pycorda'],
	install_requires=[
		'jaydebeapi',
		'pandas',
		'matplotlib',
		'datetime',
		'requests',
		'pyjks',
		'chart_studio'

	],
	include_package_data=True,
)