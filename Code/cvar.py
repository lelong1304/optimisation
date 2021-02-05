import matplotlib.pyplot as plt
import numpy as np

mu = [0.11, 0.12, 0.15]
vol = [0.1, 0.15, 0.2]

b = [10,10,10]
n = 3
T=3
S = 4
alpha = 0.95
y = np.zeros([S,n])
u = np.zeros([S,n])
for s in range(S):
    for i in range(n):
        y[s,i] = b[i]*np.exp((mu[i]-vol[i]**2/2)*T + vol[i]*T**0.5*np.random.normal())
    u[s,:] = b-y[s,:]
print(y)
print(u)


VaR = []
CVaR = []
ret = []
for k in range(1000):
    x = np.random.random(size = (n,1))
    x = x/np.sum(x)
    loss = np.dot(u, x)

    VaR.append(np.quantile(loss, alpha))
    CVaR.append(np.mean(loss[loss>VaR[k]]))
    ret.append(np.dot(mu,x))
fig = plt.figure()
plt.scatter(CVaR,ret)

plt.title("Figure 1")
plt.xlabel("CVaR at 95%")
plt.ylabel("Portfolio return")
plt.savefig('11')
print(CVaR)
print(sum(ret))