#!/usr/bin/env python3

import argparse
import os
import shutil
from sphinx.cmd.build import build_main
import tempfile
import logging

logging.basicConfig(level=logging.INFO, format='[sphinx-versioning] %(message)s')

parser = argparse.ArgumentParser(description='Manage Sphinx versioned documentation.')
parser.add_argument('--version', type=str, required=True, help='Version to manage')
parser.add_argument('-d', '--delete', action='store_true', help='Delete the version')

args = parser.parse_args()

docs_dir = os.getcwd()
parent_dir = os.path.dirname(docs_dir)

logging.info(f"current docs_dir is {docs_dir}")

if args.delete:
    if not os.path.exists(os.path.join(docs_dir, f"_static/sphinx_versioning_plugin/{args.version}")):
        logging.error(f"[ERROR] {args.version} is not found!")
        exit()

    # Delete version
    shutil.rmtree(f"_static/sphinx_versioning_plugin/{args.version}")

# Add a new version
else:
    # Create a temporary directory
    with tempfile.TemporaryDirectory(dir=parent_dir) as temp_dir:

        # Copy the documentation source to the temporary directory
        shutil.copytree('.', temp_dir, dirs_exist_ok=True)

        # Remove the versions directory from the temporary directory
        shutil.rmtree(os.path.join(temp_dir, '_static/sphinx_versioning_plugin'), ignore_errors=True)

        # Build the docs using the temporary directory as the source
        result = build_main(["-b", "html", temp_dir, f"_static/sphinx_versioning_plugin/{args.version}"])

        if result == 2:
            logging.info(f"[ERROR] Failed to build the version {args.version}")
        
        logging.info("Version {args.version} is added. Run sphinx build to see the version on the sidebar")