import os
import subprocess


#change current directory to 04_Platform
path = os.getcwd()+ "\\04_Platform"

#run platformio build
subprocess.Popen("pio run --target upload", cwd=path)