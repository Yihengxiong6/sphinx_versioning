import os
from sphinx.util import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


TEMPLATE_CONTENT_LATEST_BUILD = """{% if sphinx_versions %}
    <span style="vertical-align: middle;">{{ _('Versions') }}</span>
    <select style="vertical-align: middle; margin-left: 5px;" onchange="window.location.href=this.value" id="versionDropdown">
        <option value="/" selected>Latest</option>
        {%- for item in sphinx_versions %}
            <option value="{{ pathto('_static/sphinx_versioning_plugin/{}'.format(item), 1) }}">{{ item }}</option>
        {%- endfor %}
    </select>
{% endif %}
"""

TEMPLATE_CONTENT_VERSION_BUILD = """<span style="vertical-align: middle;">{{ _('Versions') }}</span>
    <select style="vertical-align: middle; margin-left: 5px;" onchange="window.location.href=this.value" id="versionDropdown">
        <option value="/">Latest</option>
    </select>
"""


def write_template_file_for_latest_build(app):
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


def write_template_file_for_version_build(app):
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


def update_sidebar_links_for_versioned_docs(versions_dir, versions):
    """
    Update the index.html files under each version in `_static/sphinx_versioning_plugin/` with the available versions.
    """
    for version in versions:
        index_file_path = os.path.join(versions_dir, version, "index.html")
        
        if os.path.exists(index_file_path):
            with open(index_file_path, 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')
                
                # Find the select tag with the specified id
                select_tag = soup.find("select", {"id": "versionDropdown"})
                
                # If the select tag exists, update its content
                if select_tag:
                    select_tag.clear()  # Clear existing options
                    
                    option_latest = soup.new_tag("option", value="/")
                    option_latest.string = "Latest"
                    select_tag.append(option_latest)
                    
                    for v in versions:
                        option = soup.new_tag("option", value=f"../{v}")
                        option.string = v

                        # If this option corresponds to the current version, mark it as selected
                        if v == version:
                            option.attrs["selected"] = "selected"

                        select_tag.append(option)

            with open(index_file_path, 'w') as f:
                f.write(str(soup))


def generate_versioning_sidebar(app, config):
    
    sphinx_versions_env = os.environ.get("SPHINX_VERSIONING_PLUGIN")
    
    if sphinx_versions_env == "1":
        logger.info("Versioned docs build")
        write_template_file_for_version_build(app)
        return

    # write the template file
    write_template_file_for_latest_build(app)

    # Get versions from the directory structure
    sphinx_versions = get_version_list(app)
    
    # Update the sidebar links for versioned docs
    versions_dir = os.path.join(app.srcdir, "_static", "sphinx_versioning_plugin")

    update_sidebar_links_for_versioned_docs(versions_dir, sphinx_versions)

    # update html_context with versions
    app.config.html_context.update({"sphinx_versions": sphinx_versions})


def setup(app):

    app.connect("config-inited", generate_versioning_sidebar)
