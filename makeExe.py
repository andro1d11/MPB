import os
import shutil


command = 'pyinstaller -F -i music-notes.ico main11.py --noconsole'
os.system(command)
os.remove('main11.spec')
shutil.rmtree('build')
shutil.rmtree('__pycache__')
os.remove('main11.exe')
shutil.move('dist\\main11.exe', os.getcwd())
shutil.rmtree('dist')