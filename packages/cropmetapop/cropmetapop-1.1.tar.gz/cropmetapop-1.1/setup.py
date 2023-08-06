from setuptools import setup

setup(name='cropmetapop',
      version='1.1',
      description='The crop metapopulation modelisation software',
      url='https://sourcesup.renater.fr/wiki/cmp/start#english',
      author='Equipe DEAP',
      author_email='baptiste.rouger@inra.fr',
      license='GNU GPL v3',
      packages=['cropmetapop'],
      install_requires=[
          'simuPOP',
          'numpy',
          'python-igraph'
      ],
      scripts=['bin/cropmetapop'],
      zip_safe=False)
