from setuptools import setup

setup(name='pizdets',
      version='0.19.97',
      description='PMachine Python package',
      url='https://github.com/catalin-rusnac/pizdets',
      author='Catalin Rusnac',
      author_email='crusnac@ist.ac.at',
      license='MIT',
      packages=['pizdets',"pizdets.pm"],
      install_requires=["zmq","google","pandas","protobuf","matplotlib"],
      zip_safe=True,
      python_requires='>=3.6')