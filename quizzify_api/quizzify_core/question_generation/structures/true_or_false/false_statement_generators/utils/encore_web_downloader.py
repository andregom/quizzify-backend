import subprocess
cmd = "python -m spacy download en_core_web_sm"

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, err = p.communicate()

print(out)

