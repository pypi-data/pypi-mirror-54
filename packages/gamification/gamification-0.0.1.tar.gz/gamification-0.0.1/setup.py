from setuptools import setup
import os
import sys


current_path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()


subpackages = []
parent = 'gamification'
subpackages_path = os.path.join(current_path, 'gamification')
for subdir, _, _ in os.walk(subpackages_path):
      subdirs = subdir.split(os.sep)
      parent_index = subdirs.index(parent) + 1
      subpackages.append('.'.join(subdirs[parent_index:]))

setup(name='gamification',
      version='0.0.1',
      description='',
      long_description=long_description,
      url='https://github.com/monzita/gamification',
      author='Monika Ilieva',
      author_email='example@hidden.com',
      license='MIT License',
      keywords='game console',
      packages=[*subpackages],
      package_data={},
      py_modules=['gamification'],
      install_requires=['docopt'],
      entry_points = {
        'console_scripts': [
            'gamification=gamification.main:main'
        ],
      },
      classifiers=[
        
      ],
      zip_safe=True)