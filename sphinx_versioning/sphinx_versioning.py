import json
import os
from sphinx.util import logging

logger = logging.getLogger(__name__)

def update_versions_html_context(app, config):

    # if versions.json not found, return
    if not os.path.exists(os.path.join(app.srcdir, "_versions", "versions.json")):
        return

    # Load version list from versions/versions.json
    with open(os.path.join(app.srcdir, "_versions", "versions.json")) as f:
        versions = json.load(f)

    # update html_context with versions
    app.config.html_context.update({"versions": versions})


def setup(app):
    app.connect("config-inited", update_versions_html_context)
