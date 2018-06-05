import subprocess

duration = subprocess.check_output(['ffprobe', '-i', 'v1.mp4', '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
print(duration)