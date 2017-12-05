import setuptools

setuptools.setup(
    name="python_story",
    version="0.1.0",
    url="https://github.com/itsjoel/python-story",

    author="Joel Newman",
    author_email="me@itsjoel.online",

    description="A quick way to make simple interactive stories",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=["termcolor>1.0.0"],

    # https://docs.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-mock'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
