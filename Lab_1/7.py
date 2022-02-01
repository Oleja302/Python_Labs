list = ["www.amazon.com","olx.com","donnu.ru"]

newList = [i if i.find("www",0,3) == -1 else "http://" + i for i in list]
newList = [i if i.find(".com",len(i) - 4,len(i)) != -1 else i + ".com" for i in newList]
print(newList)

print()

newList = ["http://" + i for i in list if i.find("www",0,3) != -1] + [i + ".com" for i in list if i.find(".com",len(i) - 4,len(i)) == -1] + [i for i in list if i.find(".com",len(i) - 4,len(i)) != -1 and i.find("www",0,3) == -1]
print(newList)

