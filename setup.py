from setuptools import setup, find_packages

setup(
    name='quick-flask',
    version='0.1.0',
    description='CLI tool to quickly generate Flask apps',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aditya Godse',
    author_email='adimail2404@gmail.com',
    url='https://github.com/adimail/quickflask',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'quickflask = quick_flask.create:create_flask_app',
        ],
    },
    package_data={
        'quick_flask': ['boilerplate/base/*', 'boilerplate/base/**/*.py'],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
