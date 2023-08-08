# sphinx_versioning
A Sphinx extension to manage versioned documentation.

## Overview

`sphinx-versioning` is a Sphinx extension that manages versioned documentation, allowing users to maintain multiple versions of their documentation with ease. This plugin makes it simple to create, view, and navigate between different versions, providing an enhanced user experience.


### Feature

- Version Creation: Easily create new versions of your documentation with a command-line - interface.

- Version Deletion: Manage your existing versions, including the ability to delete obsolete ones.

- Version Navigation: Conveniently navigate between different versions through a drop-down menu.

## Installation

```sh
pip install sphinx-versioning
```


## Usage

### Configuration in Sphinx

1. In your Sphinx project's conf.py file, add 'sphinx_versioning' to the extensions list:

```python
extensions = [
    ...
    'sphinx_versioning',
    ...
]
```

2. Update your `conf.py` file to include the `sphinx_versioning.html` template in the html_sidebars configuration:

```python
html_sidebars = {
    '**': [
        # ... other sidebars ...
        'sidebar/sphinx_versioning.html',
    ]
}
```

3. If you haven't, set html static path as follow:

```python
html_static_path = ['_static']
```


### Command Line Interface

The sphinx-version command-line tool provides functionality to manage versions:

- Create a New Version based based the current source file:

```sh
sphinx-version --version VERSION_NAME
```

- sphinx-version --version VERSION_NAME -d

```sh
sphinx-version --version VERSION_NAME -d
```
