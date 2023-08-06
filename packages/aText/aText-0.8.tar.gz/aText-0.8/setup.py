from setuptools import setup

sdist = setup(name='aText',
	version='0.8',
	description='Analysis of Text (aText)',
	url='http://github.com/sjskdas/aText',
	author='Subrata Das',
	author_email='sdas@machineanalytics.com',
	license='Machine Analytics',
	packages=['aText'],
	package_data={'aText': ['*.jar','*.xlsx','*.ipynb','*.bat','*.txt']},
	zip_safe=False)