from setuptools import setup
from setuptools import find_packages
from trionyx_accounts import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name = 'trionyx-accounts',
    packages = find_packages(),
    include_package_data=True,
    version = __version__,
    description = 'Trionyx app for accounts',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    author = 'Maikel Martens',
    author_email = 'maikel@martens.me',
    license='GPL3',
    url = 'https://github.com/krukas/Trionyx-Accounts',
    download_url = 'https://github.com/krukas/Trionyx-Accounts/releases/tag/{}'.format(__version__),
    keywords = ['Django', 'Trionyx', 'app', 'accounts', 'contacts',],
    python_requires='~=3.5',
    install_requires=[
    ],
    extras_require={
        'dev': [
            'Trionyx',
            'colorlog',
            'django-extensions',
            'django-debug-toolbar',
            'Werkzeug',
            'coverage',
            'flake8',
            'pydocstyle',
            'ipython',
            'Sphinx',
            'sphinx_rtd_theme',
        ]
    },
    entry_points={
        'trionyx.app': [
            'trionyx_accounts=trionyx_accounts',
        ],
    }
)