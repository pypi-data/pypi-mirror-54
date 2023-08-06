import os
from setuptools import setup, find_packages
import shutil

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

REQUIREMENTS = [
    "numpy",
    "matplotlib"
]

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Topic :: Scientific/Engineering :: Physics",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

KEYWORDS = "physics optics interferometry"

def write_config_file():
    home = os.path.expanduser('~')

    cavcalc_conf_dir = os.path.join(home, ".cavcalc")
    if not os.path.isdir(cavcalc_conf_dir):
        os.mkdir(cavcalc_conf_dir)

    user_ini_file = os.path.join(cavcalc_conf_dir, "cavcalc.ini")
    if not os.path.exists(user_ini_file):
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "cavcalc/cavcalc.ini"),
            user_ini_file
        )

write_config_file()

setup(
    name='cavcalc',
    use_scm_version={
        "write_to" : "cavcalc/version.py"
    },
    author="Samuel Rowlinson",
    author_email="sjr@star.sr.bham.ac.uk",
    description=("cavcalc is a program for computing optical cavity parameters."),
    url="http://gitlab.sr.bham.ac.uk/sjrowlinson/cavcalc",
    license="GPL",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    setup_requires=["setuptools_scm"],
    python_requires=">=3.5",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    project_urls={
        'Source' : "http://gitlab.sr.bham.ac.uk/sjrowlinson/cavcalc"
    },
    package_data={
        'cavcalc': ['_default.mplstyle', 'cavcalc.ini']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cavcalc = cavcalc.__main__:main'
        ]
    }
)
