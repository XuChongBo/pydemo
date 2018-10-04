import time
import progressbar
p = progressbar.ProgressBar()
N = 1000
p.start(N)
for i in range(N):
    time.sleep(0.01)
    p.update(i+1)
p.finish()
