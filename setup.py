from setuptools import setup

setup(name='mcdiet',
      author='Jack McIvor',
      author_email='jack@dotlovesdata.com',
      python_requires='>=3.5',
      py_modules=['mcdiet'],
      install_requires=['pulp'],
      tests_require=['pytest'],
      setup_requires=['pytest-runner'],
      zip_safe=False)
