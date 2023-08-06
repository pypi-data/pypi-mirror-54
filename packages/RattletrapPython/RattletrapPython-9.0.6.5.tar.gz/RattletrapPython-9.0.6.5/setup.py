import setuptools
import importlib
import setuptools.command.build_py
import requests
from pathlib import Path
import time

# Avoid native import statements as we don't want to depend on the package being created yet.
def load_module(module_name, full_path):
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
version = load_module("RattletrapPython.version", "RattletrapPython/version.py")
RattletrapPython = load_module(
    "RattletrapPython.rattletrap", "RattletrapPython/rattletrap.py"
)

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        rattletrap_version = version.file_version
        rattletrap_link_windows = f"https://github.com/tfausak/rattletrap/releases/download/{rattletrap_version}/rattletrap-{rattletrap_version}-windows.exe"
        rattletrap_response = requests.get(rattletrap_link_windows, allow_redirects=True)
        RattletrapPython.rattletrap_path.open("wb").write(rattletrap_response.content)
        time.sleep(5)
        setuptools.command.build_py.build_py.run(self)


setuptools.setup(
    cmdclass={"build_py": BuildPyCommand},
    name="RattletrapPython",
    packages=setuptools.find_packages(),
    python_requires=">=3.7.0",
    version=version.__version__,
    description="A package to interact with rattletrap from python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Fabio Ferreira",
    author_email="fabiorcferreira@gmail.com",
    url="https://github.com/skyborgff/RattletrapPython",
    keywords=["rocket-league", "rattletrap", "rattletrap-python"],
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={"RattletrapPython": [str(RattletrapPython.rattletrap_path)]},
    data_files=[r'./RattletrapPython/rattletrap.exe'],
    include_package_data=True,
    install_requires=['RattletrapPython'],
)
