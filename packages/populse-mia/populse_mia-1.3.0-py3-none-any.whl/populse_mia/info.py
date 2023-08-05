# -*- coding: utf-8 -*- # Character encoding, recommended
"""Define software version, description and requirements"""

import sys

# Current version
version_major = 1
version_minor = 3
version_micro = 0
version_extra = ""

# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(version_major, version_minor, version_micro)


# Expected by setup.py: the status of the project
CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7',
               'Programming Language :: Python :: 3.8',
               'Programming Language :: Python :: 3 :: Only',
               'Topic :: Scientific/Engineering',
               'Topic :: Utilities']

# project descriptions
DESCRIPTION = 'populse mia'
LONG_DESCRIPTION = """
===============
populse_mia
===============
[MIA] Multiparametric Image Analysis:
A complete image processing environment mainly targeted at 
the analysis and visualization of large amounts of MRI data
"""

# Other values used in setup.py
NAME = 'populse_mia'
ORGANISATION = 'populse'
MAINTAINER = 'Populse team'
MAINTAINER_EMAIL = 'populse-support@univ-grenoble-alpes.fr'
AUTHOR = 'Populse team'
AUTHOR_EMAIL = 'populse-support@univ-grenoble-alpes.fr'
URL = 'http://populse.github.io/populse_mia'
DOWNLOAD_URL = 'http://populse.github.io/populse_mia'
LICENSE = 'CeCILL'
VERSION = __version__
CLASSIFIERS = CLASSIFIERS
PLATFORMS = 'OS Independent'

if sys.version_info < (3 , 6) and sys.version_info >= (3 , 5):
    REQUIRES = [
        'capsul',
        'jinja2 == 2.8.1',
        'lark-parser>=0.7.0',
        'matplotlib<3.1',
        'mia-processes>=1.3.0',
        'nibabel',
        'nipype',
        'pillow',
        'populse-db',
        'pyqt5',
        'python-dateutil',
        'pyyaml',
        'scikit-image == 0.15.0',
        'scipy',
        'SIP',
        'sqlalchemy',
        'snakeviz',
        'soma_workflow',
        'traits',
]

elif sys.version_info >= (3 , 6):
    REQUIRES = [
        'capsul',
        'jinja2 == 2.8.1',
        'lark-parser>=0.7.0',
        'matplotlib',
        'mia-processes>=1.3.0',
        'nibabel',
        'nipype',
        'pillow',
        'populse-db',
        'pyqt5',
        'python-dateutil',
        'pyyaml',
        'scikit-image == 0.15.0',
        'scipy',
        'SIP',  
        'sqlalchemy',
        'snakeviz',
        'soma_workflow',
        'traits',
]

else:
    # python < 3.5 is not compatible anyway
    REQUIRES = []

EXTRA_REQUIRES = {
    'doc': [
        'sphinx>=1.0',
    ],
}

brainvisa_build_model = 'pure_python'

# tests to run
test_commands = ['%s -m populse_mia.test' % sys.executable]
