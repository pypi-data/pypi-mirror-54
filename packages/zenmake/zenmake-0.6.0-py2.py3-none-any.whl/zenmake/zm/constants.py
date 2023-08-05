# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

from zm.utils import platform as _platform

APPNAME = 'zenmake'
CAP_APPNAME = 'ZenMake'
AUTHOR = 'Alexander Magola'
COPYRIGHT_ONE_LINE = '2019, %s' % AUTHOR
BUILDOUTNAME = 'out'
WAF_CACHE_DIRNAME = 'c4che'
WAF_CACHE_NAMESUFFIX = '_cache.py'
ZENMAKE_CACHE_NAMESUFFIX = '.%s.py' % APPNAME
ZENMAKE_CMN_CFGSET_FILENAME = '.%s-common' % APPNAME
WSCRIPT_NAME = 'zmwscript'

TASK_KINDS = ('stlib', 'shlib', 'program', 'objects')
TASK_FEATURES_MAP = {
    'cstlib' : 'c',
    'cshlib' : 'c',
    'cprogram' : 'c',
    'cxxstlib' : 'cxx',
    'cxxshlib' : 'cxx',
    'cxxprogram' : 'cxx',
    'dstlib' : 'd',
    'dshlib' : 'd',
    'dprogram' : 'd',
    'fcstlib' : 'fc',
    'fcshlib' : 'fc',
    'fcprogram' : 'fc',
}

TASK_FEATURES_LANGS = set(TASK_FEATURES_MAP.values())

PLATFORM = _platform()
KNOWN_PLATFORMS = (
    'linux', 'windows', 'darwin', 'freebsd', 'openbsd', 'sunos', 'cygwin',
    'msys', 'riscos', 'atheos', 'os2', 'os2emx', 'hp-ux', 'hpux', 'aix', 'irix',
)

if PLATFORM == 'windows':
    EXE_FILE_EXTS = '.exe,.com,.bat,.cmd'
else:
    EXE_FILE_EXTS = ',.sh,.pl,.py'
