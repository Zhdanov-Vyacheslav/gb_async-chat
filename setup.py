import os

from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)
about = {}
if base_dir:
    os.chdir(base_dir)
with open(os.path.join(base_dir, "gb_chat", "__about__.py")) as f:
    exec(f.read(), about)


def parse_requires(filename) -> list:
    with open(filename) as rf:
        requires = [ln.strip() for ln in rf.readlines() if not ln.startswith("#")]
    return requires


install_requires = parse_requires("requirements.txt")

setup(name=about.get("__title__"),
      version=about.get("__version__"),
      description=about.get("__summary__"),
      author=about.get("__author__"),
      author_email=about.get("__email__"),
      packages=find_packages(),
      include_package_data=True,
      data_files=[(".", ["config.json"])],
      install_requires=install_requires,
      entry_points={
          "console_scripts": ["gb_chat = client_run:main", "gb_chat_server = server_run:main"]
      }
      )
