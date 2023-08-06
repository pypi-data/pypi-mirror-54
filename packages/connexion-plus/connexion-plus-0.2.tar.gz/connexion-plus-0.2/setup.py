#from distutils.core import setup
import setuptools

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
  name = 'connexion-plus',      
  packages = ['connexion_plus'], 
  version = '0.2',
  license='MIT', 
  description = 'Connexion with benefits for microservices',
  long_description=readme,
  author = 'Peter Heiss',
  author_email = 'peter.heiss@uni-muenster.de',
  url = 'https://github.com/Heiss/connexion-plus',
  download_url = 'https://github.com/Heiss/connexion-plus/archive/0.1.tar.gz',
  keywords = ['connexion', 'microservice', 'tracing', 'prometheus', 'jaeger'],
  python_requires='>=3.6',
  install_requires=[    
          'connexion',
          'jaeger-client',
          'prometheus-flask-exporter'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
