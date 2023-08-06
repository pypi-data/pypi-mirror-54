from setuptools import setup

setup(name='pizdets',
      version='0.19.8',
      description='PMachine Python package',
      url='https://github.com/catalin-rusnac/pizdets',
      author='Catalin Rusnac',
      author_email='crusnac@ist.ac.at',
      license='MIT',
      packages=['pizdets',"pizdets.pm"],
      install_requires=["zmq","google","pandas","google.protobuf.reflection"],
      zip_safe=True)