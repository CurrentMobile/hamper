from distutils.core import setup

setup(
    name='HamperCLI',
    version='0.1.1',
    author='Kiran Panesar',
    author_email='kiransinghpanesar@googlemail.com',
    packages=['hamper', 'hamper/helpers'],
    url='https://github.com/MobileXLabs/hamper/',
    license='LICENSE.txt',
    description='A CLI for iOS app provisioning.',
    install_requires=[
      "selenium",
      "docopt",
      "termcolor"
    ],
    entry_points={
      'console_scripts': [
        'hamper = hamper.hamper:pack',
      ]
    },
)