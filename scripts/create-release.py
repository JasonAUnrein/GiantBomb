#!/usr/bin/env python
"""
This script is used to create the release package.
"""
# Imports ######################################################################
from __future__ import print_function
import os
import sys
import shutil
import argparse
import pypandoc
import subprocess

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "09/02/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.03"

# Globals ######################################################################
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LIB_DIR = os.path.realpath(os.path.join(THIS_DIR, '..', 'lib'))
PROJ_NAME = "GiantBomb"


def remove_directory(top, remove_top=True, filter=None):
    '''
    Removes all files and directories, bottom-up.

    @type top: str
    @param top: The top-level directory you want removed
    @type remove_top: bool
    @param remove_top: Whether or not to remove the top directory
    '''
    if filter is None:
        filter = lambda x: True

    for root, dirs, files in os.walk(top, topdown=False):
        for name in [x for x in files if filter(x)]:
            os.remove(os.path.join(root, name))

        for name in dirs:
            os.rmdir(os.path.join(root, name))

    if remove_top:
        os.rmdir(top)


def ex(command, cwd=None):
    """Execute a command and return the output.  This will raise an Exception if
    the return code is non-zero.
    """
    shell = not type(command) is list

    p = subprocess.Popen(command, shell=shell, cwd=cwd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output, _ = p.communicate()

    if p.returncode:
        raise Exception("command failed: %s" % output)

    return output


def make_docs():
    """Create the documentation and add it to ../lib/docs"""
    doc_build_dir = os.path.join(THIS_DIR, '..', 'docs')
    doc_html_build = os.path.join(doc_build_dir, '_build', 'html')
    doc_dest_dir = os.path.join(THIS_DIR, '..', 'lib', 'docs')

    ex("make clean && make html", cwd=doc_build_dir)

    remove_directory(doc_dest_dir, False)

    items = set(os.listdir(doc_html_build)) ^ set(['.buildinfo', 'objects.inv'])
    for item in items:
        source = os.path.abspath(os.path.join(doc_html_build, item))
        dest = os.path.abspath(os.path.join(doc_dest_dir, item))

        if not os.path.exists(doc_dest_dir):
            os.makedirs(doc_dest_dir)

        if os.path.isdir(source):
            shutil.copytree(source, dest)
        else:
            shutil.copyfile(source, dest)


def update_readme():
    markup_file = os.path.realpath(os.path.join(LIB_DIR, '..', 'README.md'))
    rst_file = os.path.realpath(os.path.join(LIB_DIR, '..', 'lib', 'README.rst'))

    rst = pypandoc.convert(markup_file, 'rst')

    with open(rst_file, 'wb') as fh:
        fh.write(rst)


if __name__ == '__main__':
    release_dir = os.path.realpath(os.path.join(LIB_DIR, '..', 'release'))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--destdir", help="directory to put the generated zip file", type=str,
        default=release_dir)
    args = parser.parse_args()

    # Read the version from our project
    sys.path.append(LIB_DIR)
    from giantbomb import VERSION
    # Read the version from our project
    __version__ = VERSION

    remove_directory(release_dir, remove_top=False, filter=lambda x: "keep" not in x)

    # Build the docs
    update_readme()
    make_docs()

    try:
        subprocess.check_output([sys.executable, 'setup.py', 'sdist', '--formats=gztar'], stderr=subprocess.STDOUT, cwd=LIB_DIR)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise

    # move gztar
    gz_filename, = [x for x in os.listdir(os.path.join(LIB_DIR, 'dist')) if '.tar.gz' in x]
    source = os.path.join(LIB_DIR, 'dist', gz_filename)

    if args.destdir:
        dest = os.path.join(args.destdir, gz_filename)
    else:
        dest = os.path.join(THIS_DIR, gz_filename)
    shutil.move(source, dest)

    # remove left over dirs
    for directory in ['%s.egg-info' % PROJ_NAME, 'dist', 'build', '%s-%s' % (PROJ_NAME, __version__)]:
        path = os.path.join(LIB_DIR, directory)
        if os.path.exists(path):
            remove_directory(path)
