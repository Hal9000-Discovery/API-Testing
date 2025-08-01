"""



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


print("\n")


word1 = "abc"
word2 = "pqr"

for char1, char2 in zip(word1, word2):
    print(f"{char1} {char2}", end=" ")  

print("\n")


# Get rid of duplicates in a list
nums   = [0,0,1,1,1,2,2,3,3,4]
#nums   = [0,0,1,2,2,3,3,4]

if not nums:
    print("The list is empty.")
else:
    print("The list is not empty.")
    print(f"The first element is: {nums[0]}")
    print(f"The last element is: {nums[-1]}")
    print(f"The length of the list is: {len(nums)}")

# Initialize the 'slow' pointer 'i'
# This pointer marks the end of the  unique elements subarray
# nums[0] is always unique initially if the array is not empty
i = 0

# Iterate with  'fast' pointer 'j' through the list starting from the second element
for j in range(1, len(nums)):  
    # If the current element is different from the last unique element
    if nums[j] != nums[i]:
        i += 1  # Move the 'slow' pointer forward
        nums[i] = nums[j]  # Update the next position with the new unique element   
    # Print the current state of the list
    print(f"Current state of nums: {nums[:i+1]} (unique elements up to index {i})") 

print("\n")
print("\n")
print("for loop with range ")
i=0

list_number   = [0,0,1,1,1,2,2,3,3,4]
for j in range(1, len(list_number)):
    print(f"Unique element at index(j) {j}: {list_number[j]}")
    if list_number[j] != list_number[i]:
        print(f"Found a new unique element: {list_number[j]} at index(j) {j}")
        print(f"Updating index(i) {i+1} with {list_number[j]}")
        i += 1
        print(f"Moving 'i' to {i}, current unique elements: {list_number[:i+1]}")


print("\n")
print("\n")
print("for loop with range ")
i= 0
list1 = [1,2,3,4,5,6,7,8,9]
for i in range(0, len(list1),1):
    print(list1[:i], end=" ")

print("\n")
print("\n")
print("for loop no range")
for item in list1:
    print(item, end=" ")    

"""
print("\n")
print("\n")

total = 0
amounts = [10, 20, 30, 40, 50]
for i in range(0,len(amounts),1):
    if amounts[i] > 30:
        print(f"Amount {amounts[i]} is greater than 30 at index {i}") 
    if amounts[i] < 30:
        print(f"Amount {amounts[i]} is less than 30 at index {i}")
    if amounts[i] == 30:
        print(f"Amount {amounts[i]} is equal to 30 at index {i}")

  
    
    total += amounts[i]
print(f"Total of amounts greater than 30: {total}")     
print(amounts[:], end=" \n")
print(amounts[:4], end=" \n")
print(amounts[1:4], end=" \n")
print("\n")
print(amounts[:-2], end=" \n")  # Print all elements except the last one
print(amounts[-2:], end=" \n")  # Print the last two elements
print(amounts[-3:-5:-1], end=" \n")  # Print the last two elements
print("\n")

k=3
n = len(amounts)
print(f"n value is {n} and k value is {k} and the (n-k) index is {n-k} and the (n-k) element is {amounts[n-k]}")
print(amounts[n-k:] + amounts[:n-k], end=" \n") 


for i in range(len(amounts[:])):
    print(f"Index {i} has value {amounts[i]}")


nums = [1,2,3,4,5,6,7,8,9]
n =  len(nums)
k = k % n #  handle cases where k   > n

def reverse(arr, start, end):
    while start < end:
        arr[start]= arr[end]
        start += 1
        end -= 1

reverse(nums,0, n-1)
print (nums)