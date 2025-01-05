from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='kobidh',
    version='0.0.1',
    author='Souvik Dey',
    author_email='dsouvik141@gmail.com',
    license='<the license you chose>',
    description='This is a tool for automating your DevOps processes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='<github url where the tool code will remain>',
    py_modules=['kobidh', 'app'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        kobidh=kobidh:cli
    '''
)
