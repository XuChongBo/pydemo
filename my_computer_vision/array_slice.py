#Slicing returns a view into the array specified by intervals
#The shape of the image array img is  (rows, columns, color channels)

im[i,:] = im[j,:]# set the values of row i with values from row j
im[:,i] = 100   # set all values in column i to 100
im[:100,:50].sum()  # the sum of the values of the first 100 rows and 50 columns 
im[50:100,50:100]# rows 50-100, columns 50-100 (100th not included)
im[i].mean()    # average of row i
im[:,-1]        # last column
im[-2,:] (or im[-2]) # second to last row. If you only use one index it is interpreted as the row index
