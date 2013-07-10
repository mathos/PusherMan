#!/usr/bin/env python
__author__ = 'mathos'
from os.path import expanduser
home = expanduser("~")
home += "/.pusher_man"


from setuptools import setup, find_packages

long_description = """
Package manager currently in development

"""

setup(
    name='pusher_man',
    version='0.0.1',
    description='Pusher-Man is a simple implementation to get services installed, configured and out the door',
    long_description=long_description,
    author='Mathos Marcer',
    author_email='mathos.marcer@gmail.com',
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=['distribute>=0.7.3', 'Fabric>=1.6.0', 'boto>=2.8.0', 'configobj==4.7.2'],
    data_files=[
        (home, ['config/pusher.conf'])
    ],
    entry_points={
        'console_scripts': [
            'superfly = pusher_man.pusher_man:main',
        ]
    },
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Clustering',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
    ],
)
