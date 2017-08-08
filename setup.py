from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = "Page Object Model for Selenium"

tests_require = ["pytest"]
setup(
    name='selenium-pom',
    version='0.1.4',
    description="Page Object Model for Selenium",
    author="Presslabs SRL",
    author_email="ping@presslabs.com",
    url="https://github.com/Presslabs/selenium-pom",
    install_requires=["selenium"],
    tests_require=tests_require,
    packages=find_packages(exclude=['tests']),
    extras_require={
        'test': tests_require
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
    ]
)
