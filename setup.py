from setuptools import setup, find_packages


setup(
    name='selenium-pom',
    version='0.0.1',
    description="Page Object Model for Selenium",
    author="Radu Ciorba",
    author_email="radu@devrandom.ro",
    url="https://github.com/Presslabs/selenium-pom/",
    install_requires=["selenium"],
    tests_require=["pytest"],
    packages=find_packages(exclude=['tests']),
    extras_require={
        'test': tests_require
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
    ]
)
