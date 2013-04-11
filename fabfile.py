# -*- coding: utf-8 -*-
import sys

from fabric.api import *

env.user = 'root'
env.hosts = ['cocoa.fm']

def pack():

    local('python setup.py sdist --formats=gztar', capture=False)


def deploy():

    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s.tar.gz' % dist, '/tmp/cocoa.tar.gz')
    run('mkdir /tmp/cocoa')
    with cd('/tmp/cocoa'):
        run('tar xzf /tmp/cocoa.tar.gz')
