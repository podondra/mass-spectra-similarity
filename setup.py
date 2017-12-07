from setuptools import setup

setup(
    name='mss',
    packages=['mss'],
    include_package_data=True,
    install_requires=['Flask', 'Flask-PyMongo']
)
