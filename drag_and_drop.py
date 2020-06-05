import os
import sys
import subprocess


script_path = os.path.join(os.path.dirname(__file__), 'zs-ul.py')
call = ['python', script_path, '-f']
for f in sys.argv[1:]:
	call.append(f)
subprocess.Popen(call)