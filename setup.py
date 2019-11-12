from setuptools import setup

requires = [""]

setup(
    name='lgsvl_tools',
    version='0.1',
    description='Command Line Tools for LGSVL Simulator',
    url='https://github.com/tier4/lgsvl_tools.git',
    author='Masaya Kataoka',
    author_email='ms.kataoka@gmail.com',
    license='MIT',
    keywords='simulation ROS',
    packages=[
        "lgsvl_tools"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)