from setuptools import setup, find_packages

setup(
  name = 'stadista',
  packages = ["src"],
  version = '0.1',
  license='MIT',
  description = 'Toolbox to work with several platforms\'s data such as Youtube\'s stats',
  author = 'Tester86',                   
  author_email = 'tester86t@gmail.com',      
  url = 'https://github.com/Tester86/stadista', 
  download_url = 'https://github.com/Tester86/passfactory/stadista.py/v_01.tar.gz',   
  keywords = ['STATS', 'TOOLBOX', 'PROBABILITY'],
  install_requires=[
    'matplotlib',
    'requests',
    'numpy'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',    
    'Intended Audience :: Developers',    
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',    
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)