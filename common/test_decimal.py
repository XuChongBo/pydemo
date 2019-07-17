#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from decimal import Decimal, getcontext

print( Decimal.from_float(12.222) )
# 结果为Decimal('12.2219999999999995310417943983338773250579833984375')
print( Decimal('%.3f' % 12.222) )
print( Decimal('%.3f' % 12.2224) )
print( Decimal('%.3f' % 12.2225) )
print(Decimal('%.3f' % 12.222) == Decimal('%.3f' % 12.2224))
print(Decimal('%.3f' % 12.225) == Decimal('%.3f' % 12.2224))

print("multi:", float(Decimal('%.3f' % 12.225))*3.00)

print(Decimal('50.5679').quantize(Decimal('0.00')))
# 结果为Decimal('50.57')，结果四舍五入保留了两位小数


print(str(Decimal('3.40').quantize(Decimal('0.0'))))
# 结果为'3.4'，字符串类型

print("div:", Decimal(1)/Decimal(7))
print("div:", Decimal(1)/Decimal(7.0))

##注意慎用有效数字要求,数值大丢失精度大
getcontext().prec = 6  #系统默认值: 28.  The default values are precision=28, rounding=ROUND_HALF_EVEN,
print("div:", Decimal(1)/Decimal(7))

# 结果为Decimal('0.142857')，六个有效数字
print( Decimal.from_float(12.222) )
print( Decimal.from_float(8.3) )
print(Decimal.from_float(12.222)/Decimal.from_float(8.3))
print(Decimal.from_float(12.222)*Decimal.from_float(8.3))  # 结果6位有效数字 101.443  
