from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='chordparser',
      version='0.1.1',
      description='Parse and analyse chords',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.6',
          'Topic :: Text Processing',
          ],
      keywords='chord music parse notation',
      url='http://github.com/titus-ong/chordparser',
      author='Titus Ong',
      author_email='titusongyl@gmail.com',
      license='MIT',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      install_requires=[],
      zip_safe=False)
