# sphinx_versioning
A Sphinx extension to manage versioned documentation.

## Overview

`sphinx-versioning` is a Sphinx extension that manages versioned documentation, allowing users to maintain multiple versions of their documentation with ease. This plugin makes it simple to create, view, and navigate between different versions, providing an enhanced user experience.

### Features

- **Version Creation**: Easily create new versions of your documentation using the command-line interface.

- **Version Deletion**: Manage your existing versions, including the ability to delete obsolete ones.

- **Version Navigation**: Conveniently navigate between different versions through a drop-down menu.

- **Virtual Environment Support**: Virtual Environment Support: Optionally use a virtual environment when building a new version, ensuring that documentation is built with a consistent set of dependencies and avoid. 

## Installation

```sh
pip install sphinx-versioning
```

## Usage

### Configuration in Sphinx

1. In your Sphinx project's `conf.py` file, add 'sphinx_versioning' to the extensions list:

```python
extensions = [
    ...
    'sphinx_versioning',
    ...
]
```

2. Update your `conf.py` file to include the `sphinx_versioning.html` template in the `html_sidebars` configuration:

```python
html_sidebars = {
    '**': [
        # ... other sidebars ...
        # Suggest putting the extension above the search bar for better UX.
        'sidebar/sphinx_versioning.html',
    ]
}
```

3. If you haven't set it already, set `html_static_path` as follows:

```python
html_static_path = ['_static']
```

### Command Line Interface

The `sphinx-version` command-line tool provides functionality to manage versions:

#### Create a New Version based on the current source files:

```sh
sphinx-version VERSION_NAME
```
Where `VERSION_NAME` is a user-defined name for the documentation version (e.g., 'v1.0').

#### Create a New Version using a Virtual Environment:

To create a new version using a virtual environment and install dependencies from specific requirements files:

```sh
sphinx-version VERSION_NAME --venv --requirements req1.txt,req2.txt
```

> **Note**: The `--requirements` flag expects the requirements file names. These files should be located in the same directory as the Sphinx documentation. The `--requirements` flag should always be used with the `--venv` flag.


> **Why use a virtual environment?**: Using a virtual environment ensures that each version of your documentation is built with a consistent set of dependencies. This can help avoid unexpected changes or issues that might arise if Sphinx or its extensions/themes update over time.

#### Delete an Existing Version:

```sh
sphinx-version VERSION_NAME -d
```

