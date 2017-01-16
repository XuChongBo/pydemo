import argparse

parser = argparse.ArgumentParser(description='this command surpose to process some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')

parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')

parser.add_argument( '--end_time', type=str, dest='end_time', help='end update_time of questions, format: YYYY-mm-dd HH:MM:SS')


args = parser.parse_args()
print args
print args.integers
print args.end_time

import datetime
end_time = datetime.datetime.strptime(args.end_time, '%Y-%m-%d %H:%M:%S') if args.end_time else None
print type(end_time), end_time


# python test_argparse.py 12 3 --end_time '2016-09-10 12:30:45'
