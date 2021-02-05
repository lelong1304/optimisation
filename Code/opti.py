import numpy
import matplotlib.pyplot as plt
import  scipy.optimize._linprog as linprog

def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = numpy.random.rand(n)
    return k / sum(k)
class asset():
    def __init__(self, N, r, u, d, K, S0):
        self.N = N
        self.r = r
        self.u = u
        self.d = d
        self.K = K
        self.S0 = S0
        self.prices = []

    def probability(self):
        R=1+(self.r/52)
        p_u = (R-self.d)/(self.u-self.d)
        p_d = (self.u-R)/(self.u-self.d)
        return R,p_u, p_d

    def calcul_price(self):
        S = numpy.zeros([self.N+1,self.N+1])
        S[0,0] = self.S0
        for i in range(self.N+1):
            for j in range(i+1):
                S[i,j] = self.S0 * pow(self.u,j) * pow(self.d,(i-j))
        self.prices = S


assets = []
S = 4
assets.append(asset(S, 0.04, 1.0425, 0.9592, 98, 100))
assets.append(asset(S, 0.04, 1.0325, 0.9685, 8, 100))
assets.append(asset(S, 0.04, 1.0389, 0.9625, 8, 100))
assets.append(asset(S, 0.04, 1.0752, 0.93, 8, 100))
number_assert = len(assets)

n = 4
#mu = numpy.random.random_sample((n,))
mu = [0.11, 0.12, 0.15, 0.14]

alpha = 0.95
y = numpy.zeros([S,n])
u = numpy.zeros([S,n])
b = []
for elem in assets:
    elem.calcul_price()
    b.append(elem.prices[0,0])
for s in range(S): # s scenario
    for i in range(n): #  assert i-th
        count = 0
        sum_tmp = 0
        for j in range(S+1):
            if assets[i].prices[s+1,j]>0 :
                sum_tmp = sum_tmp + assets[i].prices[s+1,j]
                count = count +1
        y[s,i] = sum_tmp/count
    u[s,:] = b-y[s,:]

VaR = []
CVaR = []
ret = []
for k in range(2000):
    x = rand_weights(n)
    #x = numpy.random.random_sample((n))
    #x = x/numpy.sum(x)
    loss = numpy.dot(u, x)

    VaR.append(numpy.quantile(loss, alpha))
    CVaR.append(numpy.mean(loss[loss>VaR[k]]))
    ret.append(numpy.dot(mu,x))
rng = numpy.random.RandomState(0)


sizes = 2000 * rng.rand()



R = 0.14
h = 1/((1-alpha)*S)

c = numpy.zeros(1+n+S)
#c[1]=1
#for i in range(S):
    #c[i+1]= h
c[n] = 1
c[n+1:] = h
Aeq = numpy.zeros([1,S+n+1])
Aeq[0,:n] = 1
Beq = numpy.array([1])

Aub = numpy.zeros([S+1,S+n+1])
Aub[0,:n] = [-mui for mui in mu]
for s in range(S):
    Aub[s+1, :n] = u[s,:]
    Aub[s+1, n] = -1
    Aub[s+1, n+s+1] = -1

bub = numpy.zeros(S+1)
bub[0] = -R

x = linprog.linprog(c = c, A_ub = Aub, b_ub = bub, A_eq = Aeq, b_eq = Beq)
summ = sum(x.x[:n]);
print("result :")
print(summ)
print("Portfolio structure:", x.x[:n])
print("VaR: ", x.x[n])
print("CVaR: ", x.fun)
assets[1].calcul_price()
print(assets[1].prices)

