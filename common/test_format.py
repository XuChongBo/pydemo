from colorama import Fore
n = 10
for i in range(1,n+1): 
    print '{:<{}}'.format('#'*i, n)

for i in range(1,n+1): 
    print '{:>{}}'.format('#'*i, n)

from colorama import Fore, Back, Style
a = []
for i in range(10): 
    if i % 3 == 0 :
        a.append(Fore.GREEN+'y')
    else:
        a.append(Fore.RED+'x')
        a.append(Fore.BLUE+'o')

a.append(Style.RESET_ALL)
print ''.join(a)
