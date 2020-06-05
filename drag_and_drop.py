import sys
import subprocess

# Append other args here.
call = ['python', 'zs-ul.py']
call.append('-f')
call.extend(sys.argv[1:])
subprocess.Popen(call)
