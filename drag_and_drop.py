import sys
import subprocess


call = ['python', 'zs-ul.py', '-f']
call.extend(sys.argv[1:])
subprocess.Popen(call)
