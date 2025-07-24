
'''
This code is a simple grocery list example.
It defines a list of fruits, vegetables, and meats, 


'''

fruits =        ["apple", "banana", "cherry"]
vegetables =    ["carrot", "broccoli", "spinach"]
meats =         ["chicken", "beef", "fish"]

grocery_list = [fruits, vegetables, meats]

print (f"Print out the 3rd fruit: {fruits[2]}")  
print  (f"Print a list of all vegetables in the grocery store: {grocery_list[1]}")
print  (f"Print out the 2nd vegetable in the grocery store: {grocery_list[1][1]}")
print (f"Print out the length or the number of itemsof the grocery list: {len(grocery_list)}")

print(f"print out the list of all  vegetables in the grocery store: {grocery_list[1][0:-1]}") # Print the first two vegetables
print("\n")


for collection in grocery_list:
    print(f"Collection: {collection}")

print("\n")
for collection in grocery_list:
    for item in collection:
        print(item,end=" ")
    print ()


print("\n")

num_pad = ((1,2,3),
          (4,5,6),
          (7,8,9),
          ("*",0,"#"))


for row in num_pad:
    for num in row:
        print(num, end=" ")
    print()  # Print a new line after each row
    