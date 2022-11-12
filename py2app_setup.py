from setuptools import setup

APP = ['console.py']
OPTIONS = {
    'argv_emulation': True
}

setup(
    app=APP,
    OPTIONS={'py2app': OPTIONS},
    setup_requires=['py2app']
)
