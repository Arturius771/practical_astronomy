from setuptools import setup, find_packages

setup(
    name="af_practical_astronomy", 
    version="1.0.0",
    author="Artur Foden",
    description="Astronomically useful functions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Arturius771/practical_astronomy", 
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.12.4',
     packages=find_packages(where="lib"), 
    package_dir={"": "lib"},  
)
