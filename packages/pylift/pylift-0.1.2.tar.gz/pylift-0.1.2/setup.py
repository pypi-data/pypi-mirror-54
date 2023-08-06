from setuptools import find_packages, setup

setup(name='pylift',
      version='0.1.2',
      description='Python implementation of uplift modeling.',
      author='Robert Yi, Will Frost',
      author_email='robert@ryi.me',
      url='https://github.com/pylift/pylift',
      install_requires=[
            'numpy',
            'matplotlib',
            'scikit-learn',
            'scipy',
            'seaborn',
            'xgboost'
          ],
      packages=find_packages(),
      zip_safe=False)
