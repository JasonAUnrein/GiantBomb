#!/usr/bin/env python
"""
This script is used to create default documentation for a library.
"""
# Imports ######################################################################
import os
import re
import argparse

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "09/05/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "GPLv2"
__version__ = "0.03"


# Globals ######################################################################
PROJ_NAME = "GiantBomb"

# Base directory to search for modules
LIBDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'lib', PROJ_NAME))

# Base directory to put auto-generated doc files.
DOCDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'rst', 'lib'))

# The auto-generated index file (you'll need to add this to a TOC)
INDEX_FILE = "rst/auto.rst"

# Only include LIBDIR directories not matching this search.
IGNORE_DIR = re.compile('^.*\\\\tests(\\\\)?', re.IGNORECASE)


def remove_directory(top, remove_top=True):
    '''
    Removes all files and directories, bottom-up.

    @type top: str
    @param top: The top-level directory you want removed
    @type remove_top: bool
    @param remove_top: Whether or not to remove the top directory
    '''
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

        for name in dirs:
            os.rmdir(os.path.join(root, name))

    if remove_top:
        os.rmdir(top)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--noforce', help="Don't delete DOCDIR before generating documentation", action="store_true", default=False)
    parser.add_argument('--libdir', help="Base directory for library to document", default=LIBDIR)
    parser.add_argument('--docdir', help="Base directory to store generated .rst files", default=DOCDIR)
    parser.add_argument('--index', help="The auto-generated index file (you'll need to add this to a TOC)", default=INDEX_FILE)
    args = parser.parse_args()

    if not args.noforce:
        remove_directory(args.docdir, remove_top=False)

    docdir_root = os.path.split(args.docdir)[1]  # We'll skip this directory
    index = []  # Keep track of the files to put into the index

    for root, dirs, files in os.walk(args.libdir):
        module_dir = None

        for fname in [x for x in files if x.endswith('.py')]:
            docfile = None

            if (module_dir is None) and ('__init__.py' in files):
                module_dir = root[len(args.libdir) + 1:] or os.path.basename(root)

            if fname == "__init__.py":
                # Treat modules a little differently
                module_name = module_dir.replace('\\', '.')
                docfile_name = os.path.split(root)[1]
                docdir = os.path.join(args.docdir, module_dir, '..')
                docfile = os.path.abspath(os.path.join(docdir, "%s.rst" % docfile_name))
                index_entry = ('lib/%s' % module_dir).replace('\\', '/')
                automodule = module_name
            elif (os.path.split(root)[1] != docdir_root) and ('__init__.py' in files):
                # module_dir = root[len(args.libdir) + 1:]
                module_name = fname
                docfile_name = os.path.splitext(fname)[0]
                docdir = os.path.join(args.docdir, module_dir)
                docfile = os.path.abspath(os.path.join(docdir, "%s.rst" % docfile_name))
                index_entry = ('lib/%s/%s' % (module_dir, docfile_name)).replace('\\', '/')
                automodule = '.'.join([docdir[len(args.docdir) + 1:], docfile_name]).replace('\\', '.')

            if not docfile:
                continue

            # Make sure the path exists
            if not os.path.isdir(os.path.dirname(docfile)):
                os.makedirs(os.path.dirname(docfile))

            # Don't re-generate an already generated (or hand-created) file
            if not os.path.isfile(docfile):
                with open(docfile, 'wb') as fh:
                    fh.write("%s\n" % automodule)
                    fh.write("=" * len(automodule))
                    fh.write("\n\n")
                    fh.write(".. automodule:: %s\n" % automodule)
                    fh.write('   :members:\n')

                index.append(index_entry)

    with open(args.index, 'wb') as fh:
        fh.write("Auto Generated API Documentation\n")
        fh.write("================================\n\n")
        fh.write("Contents:\n\n")
        fh.write(".. toctree::\n")
        fh.write("   :maxdepth: 2\n\n")
        for item in index:
            fh.write("   %s\n" % item)
