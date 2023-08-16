from setuptools import setup, find_packages

setup(
    name='sphinx-versioning',
    version='0.1.0',
    packages=find_packages(),
    scripts=['scripts/sphinx-version'],
    url='https://github.com/Yihengxiong6/sphinx_versioning',
    author='Yiheng Xiong',
    author_email='georgex8866@gmail.com',
    description='A Sphinx extension to manage versioned documentation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Documentation',
        'Framework :: Sphinx :: Extension'
    ],
    keywords='sphinx documentation versioning',
    python_requires='>=3.7',
    install_requires=['Sphinx', 'beautifulsoup4'],
)
