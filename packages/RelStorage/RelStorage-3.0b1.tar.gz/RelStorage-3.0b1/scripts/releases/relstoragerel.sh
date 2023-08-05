#!/opt/local/bin/bash
#
# Quick hack script to build a single release in a virtual env. Takes one
# argument, the path to python to use.
# Has hardcoded paths, probably only works on my (JAM) machine.

set -e
export WORKON_HOME=$HOME/Projects/VirtualEnvs
export VIRTUALENVWRAPPER_LOG_DIR=~/.virtualenvs
source `which virtualenvwrapper.sh`

# Make sure there are no -march flags set
# https://github.com/gevent/gevent/issues/791
unset CFLAGS
unset CXXFLAGS
unset CPPFLAGS

# If we're building on 10.12, we have to exclude clock_gettime
# because it's not available on earlier releases and leads to
# segfaults because the symbol clock_gettime is NULL.
# See https://github.com/gevent/gevent/issues/916
export CPPFLAGS="-D_DARWIN_FEATURE_CLOCK_GETTIME=0"

BASE=`pwd`/../../
BASE=`greadlink -f $BASE`


cd /tmp/RelStorage
virtualenv -p $1 `basename $1`
cd `basename $1`
echo "Made tmpenv"
echo `pwd`
source bin/activate
echo cloning $BASE
git clone $BASE RelStorage
cd ./RelStorage
pip install -U pip
pip install -U setuptools cython greenlet cffi
pip install -U wheel
# We may need different versions of deps depending on the
# version of python; that's captured in this file.
# we still need to upgrade cython first, though
# because we can get kwargs errors otherwise
pip install -U .
python ./setup.py sdist bdist_wheel
cp dist/*whl /tmp/RelStorage/
