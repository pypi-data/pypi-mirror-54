import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def versionDev():
    from setuptools_scm.version import get_local_dirty_tag
    def clean_scheme(version):
        return get_local_dirty_tag(version) if version.dirty else ''

    return {'local_scheme': clean_scheme}


setuptools.setup(
    name="pipy_testing", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edwin-pan/pipy_testing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    use_scm_version = versionDev,
    setup_requires=['setuptools_scm'],
)