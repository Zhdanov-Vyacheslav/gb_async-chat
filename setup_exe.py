import os

from cx_Freeze import setup, Executable

base_dir = os.path.dirname(__file__)
about = {}
if base_dir:
    os.chdir(base_dir)
with open(os.path.join(base_dir, "gb_chat", "__about__.py")) as f:
    exec(f.read(), about)


executables = [
      Executable('gb_chat/client_run.py',
                 targetName='client.exe',
                 base='Win32GUI'
                 ),
      Executable('gb_chat/server_run.py', targetName='server.exe')
]

include_files = ['config.json']

options = {
      'build_exe': {
            'include_msvcr': True,
            'build_exe': about.get("__title__"),
            'include_files': include_files,
      }
}

setup(name=about.get("__title__"),
      version=about.get("__version__"),
      description=about.get("__summery__"),
      executables=executables,
      options=options
      )
