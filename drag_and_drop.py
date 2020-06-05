import sys
import subprocess


call = ['python', 'zs-ul.py', '-f']
for f in sys.argv[1:]:
	call.append(f)
subprocess.Popen(call)
