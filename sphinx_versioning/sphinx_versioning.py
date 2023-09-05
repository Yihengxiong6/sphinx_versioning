import os
from sphinx.util import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


HOME_PAGE_TEMPLATE = """"""


def latest_build_setup(app):
    """
    Write the template file for the latest build. The build should be triggered by `sphinx build`.
    The template should have link to all the versions available.
    """
    templates_dir = os.path.join(app.srcdir, "_templates/sidebar")
    template_path = os.path.isfile(os.path.join(templates_dir, "sphinx_versioning.html"))

    # create the directory if it doesn't exist
    os.makedirs(templates_dir, exist_ok=True)

    # if the template file already exists, don't write it again
    if template_path:
        return

    # else write the template content to api_docs_sidebar.html
    with open(os.path.join(templates_dir, "sphinx_versioning.html"), "w") as f:
        f.write(TEMPLATE_CONTENT_LATEST_BUILD)


def version_build_setup(app):
    """
    Write the template file for the version build. The build should be triggered by `sphinx-version -v <version>`.
    The template should only have link to the latest version.
    """
    templates_dir = os.path.join(app.srcdir, "_templates/sidebar")

    os.makedirs(templates_dir, exist_ok=True)

    # write the template content to sphinx_versioningapi_docs_sidebar.html
    with open(os.path.join(templates_dir, "sphinx_versioning.html"), "w") as f:
        f.write(TEMPLATE_CONTENT_VERSION_BUILD)


def get_version_list(app):
    """Get a list of versions by listing subdirectories of _static/sphinx_versioning_plugin/."""
    versions_dir = os.path.join(app.srcdir, "_static", "sphinx_versioning_plugin")
    if not os.path.exists(versions_dir):
        return []
    
    # List subdirectories
    subdirs = [d for d in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, d))]
    return sorted(subdirs, reverse=True)  # Assuming you'd like the versions sorted in descending order


def versioning_build(app, config):
    
    sphinx_versions_env = os.environ.get("SPHINX_VERSIONING_PLUGIN")
    
    if sphinx_versions_env == "1":
        logger.info("Versioned docs build")
        version_build_setup(app)
        return

    # Set up for the latest build
    latest_build_setup(app)

    # Get versions from the directory structure
    sphinx_versions = get_version_list(app)

def setup(app):

    app.connect("config-inited", versioning_build)
