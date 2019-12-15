from setuptools import setup, find_packages

setup(name='otus-qa',
      version='1',
      url='https://github.com/victorinausk/otus_qa',
      license='MIT',
      author='Victoria',
      author_email='victoria.uskova@gmail.com',
      description='Otus qa python code',
      packages=find_packages(exclude=['tests']),
      setup_requires=['pytest>=5.2.2'],
      zip_safe=False)
