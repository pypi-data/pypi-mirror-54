from distutils.core import setup

setup(name='omega-cli',
    version='0.1',
    description='Omega installer for Numworks',
    author='Quentin Guidée',
    author_email='quentin.guidee@gmail.com',
    url='https://github.com/Omega-Numworks/Omega-CLI-Installer',
    packages=['omega-cli'],
    install_requires=[
        'click',
        'PyInquirer'
    ],
)
