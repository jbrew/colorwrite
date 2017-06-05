import itertools


a = [1,2,3,4]
b = [5,6,7]

itertools.izip_longest(a,b)

print [x+y for x, y in itertools.izip_longest(a,b,fillvalue=0)]