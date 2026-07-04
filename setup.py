from setuptools import setup, find_packages

setup(
    name="lexer",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "lexer_lib": ["regex_grammar.txt"],   # relative to package root
    },
    include_package_data=True,
)