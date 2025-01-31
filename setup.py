from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='quick-flask',
    version='1.0.0',
    description='CLI tool to quickly generate Flask apps',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Aditya Godse',
    author_email='adimail2404@gmail.com',
    url='https://github.com/adimail/quickflask',
    packages=find_packages(include=['quick_flask', 'quick_flask.*']),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'quickflask = quick_flask.create:create_flask_app',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.6",
)
