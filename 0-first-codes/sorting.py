#different sort methods

a = [1,12,3,4,5]

#sort method
a.sort()
print("sorted = " , a)

#sorted method
b = sorted(a)
print(b)

#sort and show the output in reverse order
a.sort(reverse=True)
print(a)

#sort and show the output in reverse order using sorted method
b = sorted(a,reverse=True)
print(b)

#merger two sorted list
a = [1,2,3,4,5]
b = [6,7,8,9,10]
c = a + b
c.sort()
print(c)    
c.sort(reverse=True)
print(c)

#print each element in one line
for i in c :
    print(i,end=" ")
print("\n")

#print each element in one line using range
for i in range(len(c)):
    print(c[i],end=" ")
#reverse again
c.sort(reverse=True)

#





