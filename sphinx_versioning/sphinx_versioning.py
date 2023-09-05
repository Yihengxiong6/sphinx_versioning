import os
from sphinx.util import logging
import shutil

from jinja2 import Template

logger = logging.getLogger(__name__)


STATIC_SITE_TEMPLATE ="""
{% if sphinx_versions %}
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Iframe Navigator</title>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
            }
            
            #contentSelector {
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 10;
            }
            
            #contentIframe {
                border: none;
                width: 100%;
                height: 100%;
            }
        </style>
        <script>
            function loadIframeContent() {
                const selectElement = document.getElementById("contentSelector");
                const selectedValue = selectElement.value;
                const iframeElement = document.getElementById("contentIframe");
                iframeElement.src = selectedValue;
            }
        </script>
    </head>

    <body>
        <label for="contentSelector">Version</label>
        <select id="contentSelector" onchange="loadIframeContent()">
            <option value="latest/index.html" selected>Latest</option>
        {%- for item in sphinx_versions %}
            <option value="{{ '{}/index.html'.format(item) }}">{{ item }}</option>
        {%- endfor %}
            <!-- Add more options as necessary -->
        </select>

        <iframe id="contentIframe" src="latest/index.html" width="100%" height="600" frameborder="0"></iframe>

    </body>

    </html>
{% endif %}
"""


def latest_build_setup(app, sphinx_versions):
    """
    Write the template file for the latest build. The build should be triggered by `sphinx build`.
    The template should have link to all the versions available.
    """
    versions_output_dir = os.path.dirname(app.outdir)
    
    template = Template(STATIC_SITE_TEMPLATE)
    template_rendered = template.render(sphinx_versions=sphinx_versions)

    print("The template rendered is: ")
    print(template_rendered)

    # write the static site template to index.html
    with open(os.path.join(versions_output_dir, "index.html"), "w") as f:
        f.write(template_rendered)

    # copy the generated version folders from sphinx_versioning_plugin to versions_output_dir
    for version in sphinx_versions:
        version_dir = os.path.join(app.srcdir, "sphinx_versioning_plugin", version)
        shutil.copytree(version_dir, os.path.join(versions_output_dir, version), dirs_exist_ok=True)


def version_build_setup(app):
    """
    Write the template file for the version build. The build should be triggered by `sphinx-version -v <version>`.
    The template should only have link to the latest version.
    """
    templates_dir = os.path.join(app.srcdir, "_templates/sidebar")

    os.makedirs(templates_dir, exist_ok=True)

    # write the template content to sphinx_versioning api_docs_sidebar.html
    with open(os.path.join(templates_dir, "sphinx_versioning.html"), "w") as f:
        f.write(TEMPLATE_CONTENT_VERSION_BUILD)


def get_version_list(app):
    """Get a list of versions by listing subdirectories of _static/sphinx_versioning_plugin/."""
    versions_dir = os.path.join(app.srcdir, "sphinx_versioning_plugin")
    print("The versions dir is: ")
    print(versions_dir)
    if not os.path.exists(versions_dir):
        return []
    
    print(os.listdir(versions_dir))
    # List subdirectories
    subdirs = [d for d in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, d))]
    print("The subdirs are: ")
    print(subdirs)
    return sorted(subdirs, reverse=True)  # Assuming you'd like the versions sorted in descending order


def versioning_build(app, config):
    
    sphinx_versions_env = os.environ.get("SPHINX_VERSIONING_PLUGIN")
    
    if sphinx_versions_env == "1":
        logger.info("Versioned docs build")
        version_build_setup(app)
        return

    # Get versions from the directory structure
    sphinx_versions = get_version_list(app)

    # Set up for the latest build
    latest_build_setup(app, sphinx_versions)

    # update html_context with versions
    app.config.html_context.update({"sphinx_versions": sphinx_versions})


def setup(app):

    app.connect("config-inited", versioning_build)
