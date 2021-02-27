import matplotlib.pyplot as plt

def drawLines(x,y,name,color,titlename,fileName):
    plt.figure(dpi=200)
    for i in range(0, len(y)):
        plt.plot(x, y[i], label= name[i], linewidth=1, color = color[i])
    #plt.xlabel('date')
    #plt.ylabel('value')
    plt.title(titlename)
    plt.legend()
    plt.savefig(fileName, dpi=200, format='svg', transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)
    #plt.show()