from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        requirements = [line.strip() for line in lines if line and not line.startswith('#')]
    return requirements

setup(
    name='djbackup',
    version='2.0.3',
    description='dj_backup is an installable module for Django that is used for backup purposes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/FZl47/dj_backup',
    author='FZl47',
    author_email='fzl8747@gmail.com',
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
