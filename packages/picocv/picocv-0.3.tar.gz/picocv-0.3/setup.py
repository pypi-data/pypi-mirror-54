from distutils.core import setup
setup(
  name = 'picocv',
  packages = ['picocv'],
  version = '0.3',
  license='MIT',
  description = 'PICO semi-auto label correction algorithm for Computer Vision',
  author = 'James Yougchae Chee',
  author_email = 'litcoderr@gmail.com',
  url = 'https://github.com/litcoderr/picocv',
  download_url = 'https://github.com/litcoderr/picocv/archive/v_0.3.tar.gz',
  keywords = ['deeplearning', 'pytorch', 'machinelearning'],
  install_requires=[
          'torch',
          'numpy',
  ],
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