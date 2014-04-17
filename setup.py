import site

sp = site.getsitepackages()[-1]

filer = open('Spinne.py', 'r')
c = filer.read()
filer.close()

filew = open(sp + '\\Spinne.py', 'w')
filew.write(c)
filew.close()
