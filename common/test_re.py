#!/usr/bin/python
import re

line = "Cats are smarter than dogs";

searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)

if searchObj:
    print "searchObj.group() : ", searchObj.group()
    print "searchObj.group(1) : ", searchObj.group(1)
    print "searchObj.group(2) : ", searchObj.group(2)
else:
    print "Nothing found!!"

line = '/data1/20180604/stat_sdk_ios/app_key_p=1A9ECEC090B5B3A3/date_p=20180604/all_0.avro'
line = 'abdate_p=33'
searchObj = re.search( r'.*date_p=(\d+).*', line, re.M|re.I)
searchObj = re.search( r'.*date_p=(\d+).*', line)


if searchObj:
    print "searchObj.group() : ", searchObj.group()
    print "searchObj.group(1) : ", searchObj.group(1)
else:
    print "Nothing found!!"


