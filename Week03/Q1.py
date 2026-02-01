print("Q1")

grades = [85, 92, 78, 95, 88]
grades.append(90)
grades.sort()

print("Sorted grades:", grades)
print("Highest grade:", grades[-1])
print("Lowest grade:", grades[0])
print("Total number of grades:", len(grades))

print()


print("Q2")

cart = ["apple", "banana", "milk", "bread", "apple", "eggs"]

print("Number of apples:", cart.count("apple"))
print("Position of milk:", cart.index("milk"))

cart.remove("apple")
last_item = cart.pop()

print("Removed item using pop:", last_item)
print("Is banana in cart?", "banana" in cart)
print("Final cart:", cart)

print()


print("Q3")

point1 = (3, 5)
point2 = (7, 2)

x1, y1 = point1
x2, y2 = point2

distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

print("Point 1:", point1)
print("Point 2:", point2)
print("x1 =", x1, "y1 =", y1)
print("x2 =", x2, "y2 =", y2)
print("Distance between points:", distance)

letters = tuple("PYTHON")
print("Characters tuple:", letters)

for l in letters: 
    print(l) 

print()


print("Q4")

monday = {"Alice", "Bob", "Charlie", "Diana"}
wednesday = {"Bob", "Diana", "Eve", "Frank"}

monday.add("Grace")

print("Monday class:", monday)
print("Wednesday class:", wednesday)
print("Both:", monday & wednesday)
print("Either:", monday | wednesday)
print("Only Monday:", monday - wednesday)
print("Only one:", monday ^ wednesday)
print("Subset?", monday <= (monday | wednesday))

print()


print("Q5")
  
contacts = {
    "Alice": "555-1234", 
    "Bob": "555-5678",
    "Charlie": "555-9999"
}

print("Alice's number:", contacts["Alice"])

contacts["Diana"] = "555-4321"
print("After adding Diana:", contacts)

contacts["Bob"] = "555-0000"
print("After updating Bob:", contacts)

del contacts["Charlie"]
print("After deleting Charlie:", contacts)

print("Names:", contacts.keys())
print("Numbers:", contacts.values())
print("Total contacts:", len(contacts))

print()


print("Q6")

inventory = {
    "Laptop": (999.99, 5),
    "Mouse": (29.99, 15),
    "Keyboard": (79.99, 10),
    "Monitor": (299.99, 8)
}

for item, info in inventory.items():
    print(item, info)

electronics = {"Laptop", "Monitor"}
accessories = {"Mouse", "Keyboard"}

print("All products:", electronics | accessories)

prices = []
for i in inventory:
    prices.append(inventory[i][0])

prices.sort()
print("Prices:", prices)
print("Lowest:", prices[0])
print("Highest:", prices[-1])

inventory["Headphones"] = (49.99, 20)
inventory["Mouse"] = (inventory["Mouse"][0], 12)
del inventory["Monitor"]

print("Final inventory:")
for item, info in inventory.items():
    print(item, info)
