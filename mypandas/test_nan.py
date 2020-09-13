import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10,6))
# Make a few areas have NaN values
df.iloc[1:3,1] = np.nan
df.iloc[5,3] = np.nan
df.iloc[7:9,5] = np.nan
print(df)
print(df.rolling(2).mean())
print(df.rolling(2).mean().shift(-2))
print(df/df.rolling(2).mean())
print(df.isnull().values.any())

"""
pct_change()默认遇到缺失值nan按照'pad'方法填充

pct_change(fill_method='pad')

即向前寻找最近的非nan值，计算百分比变动。实际想要的可能是

pct_change(fill_method=None)
"""
print(df.iloc[:,1].pct_change(3, fill_method=None))
print(df.iloc[:,1].pct_change(3).map(lambda x: int(x > 0.1)))
