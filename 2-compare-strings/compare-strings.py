ans1 = input("Enter the first string: ")
ans2 = input("Enter the second string: ")

if ans1 == ans2:
    print("The strings are the same")
else:
    print("The strings are not the same")   
    
#word counter
ans3 = input("Enter the string: ")
word_count = len(ans3.split())
print("The number of words in the string is: ",word_count)

#character counter
ans4 = input("Enter the string: ")
char_count = len(ans4)
print("The number of characters in the string is: ",char_count) 


