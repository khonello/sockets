import sys
import time

string = 'Hello world'
for c in string:
    print(c, end= '')

    sys.stdout.flush()
    time.sleep(0.2)
