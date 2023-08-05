import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

required = []
with open("requirements.txt", "r") as freq:
    for line in freq.read().split():
        required.append(line)

packages = setuptools.find_packages("modules")
packages.remove("reggol")

setuptools.setup(
    name="ravestate",
    version="0.7.0",
    url="https://github.com/roboy/ravestate",
    author="Roboy",
    author_email="info@roboy.org",

    description="Ravestate is a reactive library for real-time natural language dialog systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    package_dir={'': 'modules'},
    packages=packages,
    include_package_data=True,
    package_data={
        'raveboard': ['*.js', '*.ico', '*.html', '*.txt', '*.css'],
        'ravestate_phrases_basic_en': ['en/*.yml'],
        'ravestate_ontology': ['ravestate_ontology.yml'],
        'ravestate_roboyqa': ['answering_phrases/RoboyInfoList.yml'],
        'ravestate_persqa': ['persqa_phrases/*.yml']
    },

    install_requires=required + ["reggol>=0.2.0"],
    python_requires='>=3.6',

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
