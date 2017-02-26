import pipes
import time

while(True):
    time.sleep(0.001)
    f = pipes.Template().open('percent.txt', 'r')
    for line in f:
        print line