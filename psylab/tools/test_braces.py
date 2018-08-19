import numpy as np
import matplotlib.pyplot as plt

def range_brace(x_min, x_max, mid=0.5, 
                beta1=100.0, beta2=100.0, height=1, 
                initial_divisions=11, resolution_factor=1.5):
    # determine x0 adaptively values using second derivitive
    # could be replaced with less snazzy:
    #   x0 = np.arange(0, 0.5, .001)
    x0 = np.array(())
    tmpx = np.linspace(0, 0.5, initial_divisions)
    tmp = beta1**2 * (np.exp(beta1*tmpx)) * (1-np.exp(beta1*tmpx)) / np.power((1+np.exp(beta1*tmpx)),3)
    tmp += beta2**2 * (np.exp(beta2*(tmpx-0.5))) * (1-np.exp(beta2*(tmpx-0.5))) / np.power((1+np.exp(beta2*(tmpx-0.5))),3)
    for i in np.arange(0, len(tmpx)-1):
        t = np.int32(np.ceil(resolution_factor*max(np.abs(tmp[i:i+2]))/np.float32(initial_divisions)))
        x0 = np.append(x0, np.linspace(tmpx[i],tmpx[i+1],t))
    x0 = np.sort(np.unique(x0)) # sort and remove dups
    # half brace using sum of two logistic functions
    y0 = mid*2*((1/(1.+np.exp(-1*beta1*x0)))-0.5)
    y0 += (1-mid)*2*(1/(1.+np.exp(-1*beta2*(x0-0.5))))
    # concat and scale x
    x = np.concatenate((x0, 1-x0[::-1])) * np.float32((x_max-x_min)) + x_min
    y = np.concatenate((y0, y0[::-1])) * np.float32(height)
    return (x,y)

fig = plt.figure()
ax = fig.add_subplot(111)

x,y = range_brace(0, 100)
ax.plot(x, (y*.1)+1,'-')
plt.ylim(0,2)
plt.show()
