def checkList(list):
    if list == sorted(list):
        return True
    else:
        return False


list1 = [1, 2, 1, 5, 3, 1]
list2 = list(range(1, 10))

print(checkList(list1))
print(checkList(list2))
