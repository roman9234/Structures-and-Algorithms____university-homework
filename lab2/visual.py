import matplotlib.pyplot as plt

plt.scatter(10, 23, s=7, c='r')
plt.scatter(24, 43, s=7, c='b')

for x in range(0,64,16):
    plt.axline((x,5), (x,10))
    plt.axline((0,x), (10,x))

plt.plot((0,10),(10,20))
plt.plot((0,123),(10,1))
plt.fill_between((0,16), 16, 32, color='blue', alpha=0.2)
plt.fill_between((16,32), 16, 32, color='red', alpha=0.2)

plt.xticks(list(x for x in range(0,64+16,4)))
plt.yticks(list(x for x in range(0,64+16,4)))

plt.xlim(0,64)
plt.ylim(0,64)

plt.show()

# .venv\Scripts> .\activate




































