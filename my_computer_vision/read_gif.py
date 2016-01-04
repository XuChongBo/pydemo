import Image
a = Image.open("12.gif")
palette = a.getpalette()
assert(palette%3==0)
tuple_list = zip(*[iter(c)]*3)
a.putpalette()

