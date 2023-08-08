import os
from sphinx.util import logging

logger = logging.getLogger(__name__)

TEMPLATE_CONTENT = """{% if sphinx_versions %}
    <h4>{{ _('Versions') }}</h4>
    <ul style="list-style-type: none;" id="sphinx_versioning_plugin_ul">
    {%- for item in sphinx_versions %}
        <li style="margin-bottom: 10px;"><a href="{{ pathto('_static/sphinx_versioning_plugin/{}'.format(item), 1) }}">{{ item }}</a></li>
    {%- endfor %}
    </ul>
{% endif %}
"""


def write_template_file(app):
    templates_dir = os.path.join(app.srcdir, "_templates/sidebar")
    template_path = os.path.isfile(os.path.join(templates_dir, "sphinx_versioning.html"))

    # create the directory if it doesn't exist
    os.makedirs(templates_dir, exist_ok=True)

    # if the template file already exists, don't write it again
    if template_path:
        return

    # else write the template content to api_docs_sidebar.html
    with open(os.path.join(templates_dir, "sphinx_versioning.html"), "w") as f:
        f.write(TEMPLATE_CONTENT)


def get_version_list(app):
    """Get a list of versions by listing subdirectories of _static/sphinx_versioning_plugin/."""
    versions_dir = os.path.join(app.srcdir, "_static", "sphinx_versioning_plugin")
    if not os.path.exists(versions_dir):
        return []
    
    # List subdirectories
    subdirs = [d for d in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, d))]
    return sorted(subdirs, reverse=True)  # Assuming you'd like the versions sorted in descending order


def generate_versioning_sidebar(app, config):
    # write the template file
    write_template_file(app)

    # Get versions from the directory structure
    sphinx_versions = get_version_list(app)

    logger.info(f"list of versions:{sphinx_versions}")

    # update html_context with versions
    app.config.html_context.update({"sphinx_versions": sphinx_versions})


def setup(app):

    app.connect("config-inited", generate_versioning_sidebar)
