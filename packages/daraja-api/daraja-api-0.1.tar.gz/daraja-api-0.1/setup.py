from distutils.core import setup
setup(
  name = 'daraja-api',         
  packages = ['daraja_api'],   
  version = '0.1',     
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