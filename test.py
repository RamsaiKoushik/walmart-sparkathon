dic = {"1":4, "2":8, "3":5, "4":10, "5":6, "6":9}

sorted_dict = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
print(sorted_dict)

i=0
ls = []
for item in sorted_dict:
    ls.append(item[0])
    i+=1
    if (i==5):
        break

print(ls)