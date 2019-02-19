"""
assess.py is a convenient way to compare and contrast two models by seeing
which images they agree had an annotation and which image does not
"""

print('Analyzing...')
l1 = open('annotations-computervision/m1_96_list.txt').readlines()
l2 = open('annotations-computervision/m2_96_list.txt').readlines()
s1 = set(l1)
s2 = set(l2)

intersect = s1.intersection(s2)
s1diff = s1.difference(s2)
s2diff = s2.difference(s1)

print('There are {} links in s1'.format(len(s1)))
print('There are {} links in s2'.format(len(s2)))

print('There are {} similaries'.format(len(intersect)) )
for l in sorted(intersect):
	print(l,end='')

print()
print('There are {} unique to s1'.format(len(s1diff)))
for l in sorted(s1diff):
	print(l,end='')

print()
print('There are {} unique to s2'.format(len(s2diff)))
for l in sorted(s2diff):
	print(l,end='')

close('annotations-computervision/m2_96_list.txt')
close('annotations-computervision/m1_96_list.txt')

