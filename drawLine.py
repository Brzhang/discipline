import matplotlib.pyplot as plt
import constant

def drawLines(x,y,name,color,titlename,fileName):
    print('will draw: ', titlename, fileName)
    fig = plt.figure(dpi=constant.drawDpi)
    for i in range(0, len(y)):
        plt.plot(x, y[i], label= name[i], linewidth=1, color = color[i])
    #plt.xlabel('date')
    #plt.ylabel('value')
    plt.title(titlename)
    plt.legend()
    plt.xticks(x,rotation=270, size=4)
    #fig.autofmt_xdate()
    plt.savefig(fileName + '.' + constant.fileType, dpi=constant.drawDpi, format=constant.fileType, transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)
    return plt