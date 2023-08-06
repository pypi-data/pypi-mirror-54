from setuptools import setup

setup(
    name='custom-logger-zema',
    version='0.1.1',    
    description='A custom logger created for internal usage',
    author='Nirmal Kumar',
    author_email='n.ramadoss@zema.de',
    license='MIT',
    packages=['custom-logger-zema'],
    install_requires=['paho-mqtt'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3'
    ]
)
