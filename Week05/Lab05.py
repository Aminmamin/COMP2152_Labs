# Week 05 Lab: Recursion & Functions
# COMP2152 - Python Programming

print("=" * 60)
print("WEEK 05 LAB: RECURSION & FUNCTIONS")
print("=" * 60)

# ===================== Question 1 =====================
print("\n" + "=" * 50)
print("Question 1: Fibonacci Number (#509)")
print("=" * 50)


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


print("Fibonacci values from 0 to 10:")
for i in range(11):
    print("F(" + str(i) + ") =", fib(i))

print("\nExtra tests:")
print("F(15) =", fib(15))
print("F(20) =", fib(20))


# ===================== Question 2 =====================
print("\n" + "=" * 50)
print("Question 2: FizzBuzz (#412)")
print("=" * 50)


def fizz_buzz(n):
    result = []

    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))

    return result


print("\nFizzBuzz Tests:")
print("n = 3:", fizz_buzz(3))
print("n = 5:", fizz_buzz(5))
print("n = 15:", fizz_buzz(15))
print("n = 1:", fizz_buzz(1))


# ===================== Question 3 =====================
print("\n" + "=" * 50)
print("Question 3: Binary Search (#704)")
print("=" * 50)


def binary_search_iterative(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1

    return -1


def binary_search_recursive(nums, target, left, right):
    if left > right:
        return -1

    mid = (left + right) // 2

    if nums[mid] == target:
        return mid
    elif target < nums[mid]:
        return binary_search_recursive(nums, target, left, mid - 1)
    else:
        return binary_search_recursive(nums, target, mid + 1, right)


def search_recursive(nums, target):
    if len(nums) == 0:
        return -1
    return binary_search_recursive(nums, target, 0, len(nums) - 1)


test_cases = [
    ([-1, 0, 3, 5, 9, 12], 9),
    ([-1, 0, 3, 5, 9, 12], 2),
    ([1], 1),
    ([1, 2, 3, 4, 5], 1),
    ([1, 2, 3, 4, 5], 5),
    ([1, 2, 3, 4, 5], 3),
    ([], 5)
]

print("\nIterative Results:")
for nums, target in test_cases:
    print(nums, target, "->", binary_search_iterative(nums, target))

print("\nRecursive Results:")
for nums, target in test_cases:
    print(nums, target, "->", search_recursive(nums, target))


print("\n" + "=" * 60)
print("Lab Finished")
print("=" * 60)
