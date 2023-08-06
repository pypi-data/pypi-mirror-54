#!/bin/bash
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
#
# Update the application source code in this environment.
# Runs either `pip --update` or `git pull` depending on the options specified during startsite.
# Also remove all `*.pyc` files in these repositories.

set -e
umask 0007

PRJDIR={{project_dir}}
ENVDIR=$PRJDIR/{{env_link}}
REPOS=$ENVDIR/{{repos_link}}

function pull() {
    repo=$REPOS/$1
    cd $repo
    pwd
    git pull
    find -name '*.pyc' -exec rm -f {} +
    cd $PRJDIR
}

cd $PRJDIR
. $ENVDIR/bin/activate
LOGFILE=$VIRTUAL_ENV/freeze.log
echo "Run pull.sh in $PRJDIR ($VIRTUAL_ENV)" >> $LOGFILE
date >> $LOGFILE
pip freeze >> $LOGFILE

{% for name in dev_packages.split() -%}
pull {{name}}
{%- endfor %}

{% if pip_packages -%}
pip install -U {{pip_packages}}
{%- endif %}
