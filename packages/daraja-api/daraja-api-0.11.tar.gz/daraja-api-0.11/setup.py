from setuptools import setup, find_packages

setup(
  name = 'daraja-api',         
  packages = find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),   
  version = '0.11',     
  license='MIT',      
  description = 'yet another python daraja api library',
  author = 'jack ogina',                  
  author_email = 'jackogina60@gmail.com',      
  url = 'https://github.com/jakhax/python_daraja_api',  
  download_url = 'https://github.com/jakhax/python_daraja_api.git',   
  keywords = ['daraja', 'safaricom', 'mpesa'],  
  install_requires=['phonenumbers','requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)