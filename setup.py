from setuptools import setup
setup(name='imotion',
      version='1.0',
      description='Imotion: Visualizing emotions in media by robotic swarm motion',
      url='https://github.com/makokaz/Imotion',
      author='UTokyo Research Hackathon',
      author_email='None',
      license='MIT',
      packages=['Imotion'],
      install_requires=['Flask == 2.0.1',
                        'Flask-Cors == 3.0.10',
                        'textblob == 0.15.3'],
      python_requires='>=3')

import nltk
nltk.download('stopwords')
