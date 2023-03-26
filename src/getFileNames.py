import os

d = os.listdir("../data/")
d.sort()
for file in d:
    print(file)
