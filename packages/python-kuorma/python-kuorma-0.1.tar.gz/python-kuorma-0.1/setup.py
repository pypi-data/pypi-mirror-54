# -*- coding: utf-8 -*-

import setuptools

setuptools._install_setup_requires({'setup_requires': ['git-versiointi']})
from versiointi import asennustiedot

setuptools.setup(
  name='python-kuorma',
  description='Python-funktioiden ja -metodien ajonaikainen ylikuormitus',
  url='https://github.com/an7oine/python-kuorma.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@pispalanit.fi',
  packages=setuptools.find_packages(),
  include_package_data=True,
  zip_safe=False,
  **asennustiedot(__file__)
)
