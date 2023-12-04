import os
import json
from sphinx.util import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


TEMPLATE_CONTENT_LATEST = """
<div id="sphinx_versioning_container">
    <span style="vertical-align: middle;">{{ _('Versions') }}</span>
    <select style="vertical-align: middle; margin-left: 5px;" onchange="window.location.href=this.value" id="sphinx_versioning_dropdown_menu">
        <option value="/">Latest</option>
        <!-- Additional versions will be populated here by JavaScript -->
    </select>
</div>
<script>
    fetch('/_static/sphinx_versioning_plugin/versions.json')
        .then(response => response.json())
        .then(versions => {
            const dropdown = document.getElementById('sphinx_versioning_dropdown_menu');
            const container = document.getElementById('sphinx_versioning_container');

            // Check if the versions array is empty
            if (versions.length === 0) {
                // Hide the entire container if there are no versions
                container.style.display = 'none';
            } else {
                versions.forEach(version => {
                    const option = document.createElement('option');
                    option.value = `/_static/sphinx_versioning_plugin/${version}/`;
                    option.text = version;

                    // If current page URL contains this version, set it as selected
                    if(window.location.pathname.includes(`_static/sphinx_versioning_plugin/${version}/`)) {
                        option.selected = true;
                    }
                    dropdown.appendChild(option);
                });
            }
        });
</script>
"""


TEMPLATE_CONTENT_VERSIONED = """
<div id="sphinx_versioning_container">
    <span style="vertical-align: middle;">{{ _('Versions') }}</span>
    <select style="vertical-align: middle; margin-left: 5px;" onchange="window.location.href=this.value" id="sphinx_versioning_dropdown_menu">
        <option value="/">Latest</option>
        <!-- Additional versions will be populated here by JavaScript -->
    </select>
</div>
<script>
    fetch('/_static/sphinx_versioning_plugin/versions.json')
        .then(response => response.json())
        .then(versions => {
            const dropdown = document.getElementById('sphinx_versioning_dropdown_menu');
            const container = document.getElementById('sphinx_versioning_container');

            // Check if the versions array is empty
            if (versions.length === 0) {
                // Hide the entire container if there are no versions
                container.style.display = 'none';
            } else {
                versions.forEach(version => {
                    const option = document.createElement('option');
                    option.value = `/_static/sphinx_versioning_plugin/${version}/`;
                    option.text = version;

                    // If current page URL contains this version, set it as selected
                    if(window.location.pathname.includes(`_static/sphinx_versioning_plugin/${version}/`)) {
                        option.selected = true;
                    }
                    dropdown.appendChild(option);
                });
            }
        });
</script>

"""


def update_version_json(app):
    """Updates the versions.json file with the list of current versions."""
    versions_dir = os.path.join(app.srcdir, "_static", "sphinx_versioning_plugin")
    
    # Get versions
    sphinx_versions = get_version_list(app)

    # Write to versions.json
    json_path = os.path.join(versions_dir, "versions.json")
    with open(json_path, 'w') as f:
        json.dump(sphinx_versions, f)


def write_template_file(app, versioning_type):
    """
    Write the template file for the latest build. The build should be triggered by `sphinx build`.
    The template should have link to all the versions available.
    """
    templates_dir = os.path.join(app.srcdir, "_templates/sidebar")
    template_path = os.path.isfile(os.path.join(templates_dir, "sphinx_versioning.html"))

    # create the directory if it doesn't exist
    os.makedirs(templates_dir, exist_ok=True)

    # # if the template file already exists, don't write it again
    # if template_path:
    #     return

    # else write the template content to api_docs_sidebar.html
    with open(os.path.join(templates_dir, "sphinx_versioning.html"), "w") as f:
        if versioning_type != "1":
            print("Writing latest version template")
            f.write(TEMPLATE_CONTENT_LATEST)
        else:
            print("Writing versioned template")
            f.write(TEMPLATE_CONTENT_VERSIONED)


def get_version_list(app):
    """Get a list of versions by listing subdirectories of _static/sphinx_versioning_plugin/."""
    versions_dir = os.path.join(app.srcdir, "_static", "sphinx_versioning_plugin")
    if not os.path.exists(versions_dir):
        return []
    
    # List subdirectories
    subdirs = [d for d in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, d))]
    return sorted(subdirs, reverse=True)  # Assuming you'd like the versions sorted in descending order


def update_version_json(app, versions):
    """Updates the versions.json file with the list of current versions."""
    versions_dir = os.path.join(app.srcdir, "_static", "sphinx_versioning_plugin")

    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
    
    # Write to versions.json
    json_path = os.path.join(versions_dir, "versions.json")
    with open(json_path, 'w') as f:
        json.dump(versions, f)


def generate_versioning_sidebar(app, config):

    # write the template file
    write_template_file(app, os.environ.get("SPHINX_VERSIONING_PLUGIN"))

    # get the versions
    versions = get_version_list(app)

    # Now also update the JSON file after generating sidebar
    update_version_json(app, versions)


def setup(app):

    app.connect("config-inited", generate_versioning_sidebar)
