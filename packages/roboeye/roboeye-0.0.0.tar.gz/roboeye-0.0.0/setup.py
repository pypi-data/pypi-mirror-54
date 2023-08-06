from setuptools import setup


setup(
    name='roboeye',
    description='Enlightenment about humans for robots',
    author='Philipp Benjamin Koeppchen',
    author_email='bejamin.koeppchen@triplet.gmbh',
    url='https://triplet.gmbh/',
    packages=[
        'roboeye'
    ],
    install_requires=[
        'pyyaml==5.1.2',
        'mistletoe==0.7.2',
    ],
    extras_require={
        'dev': [
            'pytest==4.3.1',
            'pycodestyle',
        ]
    }
)
