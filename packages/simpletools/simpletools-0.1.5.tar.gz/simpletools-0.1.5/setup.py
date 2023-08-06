from setuptools import setup

setup(name='simpletools',
      version='0.1.5',
      description='simpletools',
      url='https://github.com/getsimpletools/simpletools-python/tree/master',
      author='Marcin Rosinski',
      author_email='marcin@getsimpletools.com',
      license='BSD-3',
      packages=['simpletools'],
      install_requires=['pika>=1.0.0'],
      zip_safe=False)