#!/usr/bin/env python

"""
Uploads the package to PyPI.
"""

import os
import subprocess
import shutil
import sys

PYTHON_EXE = sys.executable
PIP_EXE = os.path.join(os.path.dirname(PYTHON_EXE), "pip")

# Equivalent to 'rm -rf build dist'
if os.path.exists('build'):
    shutil.rmtree('build', ignore_errors=True)
if os.path.exists('dist'):
    shutil.rmtree('dist', ignore_errors=True)

# Equivalent to 'pip install wheel twine'
subprocess.check_call([PIP_EXE, 'install', 'wheel', 'twine'])

print("Building Source and Wheel (universal) distribution…")
# Equivalent to 'python setup.py sdist bdist_wheel --universal'
subprocess.check_call([PYTHON_EXE, 'setup.py', 'sdist', 'bdist_wheel', '--universal'])

print("Uploading the package to PyPI via Twine…")
# Equivalent to 'twine upload dist/* --verbose'
subprocess.check_call(['twine', 'upload', 'dist/*', '--verbose'])

print("Pushing git tags…")
subprocess.check_call(['git', 'push', '--tags'])
