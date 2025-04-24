from setuptools import setup, find_packages

setup(
    name='djbackup',
    version='2.0.0',
    packages=find_packages(),
    description='dj_backup is an installable module for Django that is used for backup purposes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/FZl47/dj_backup',
    author='FZl47',
    author_email='fzl8747@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)