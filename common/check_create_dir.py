import os
import sys

if __name__=='__main__':
    if 2==len(sys.argv):
        output_dir = sys.argv[1]
    else:
        print "usage: %s output_dir" % __file__
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        print "warning: %s exists!" % output_dir
