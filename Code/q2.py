import numpy
import matplotlib.pyplot as plt
import  scipy.optimize._linprog as linprog

def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = numpy.random.rand(n)
    return k / sum(k)
class asset():
    def __init__(self, N, r, u, d, S0):
        self.N = N
        self.r = r
        self.u = u
        self.d = d
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

def init_function():
    c = numpy.zeros(1+n+S)
    c[n] = 1
    c[n+1:] = h

    A_ub = numpy.zeros([S+1,S+n+1])
    for element in uj:
        A_ub[0,:n] = element *(-1)
    for s in range(S):
        A_ub[s+1, :n] = u[s,:]
        A_ub[s+1, n] = -1
        A_ub[s+1, n+s+1] = -1
    b_ub = numpy.zeros(S+1)
    b_ub[0] = R*(-1)

    A_eq = numpy.zeros([1,S+n+1])
    A_eq[0,:n] = 1
    b_eq = [1]

    return (c,A_eq,b_eq,A_ub,b_ub)

assets = []
n = 4
S = 4 #scenario
assets.append(asset(N= S, r= 0.04, u=1.0425, d=0.9592, S0=100))
assets.append(asset(N=S, r=0.04, u=1.0325, d=0.9685, S0=100))
assets.append(asset(N=S, r=0.04, u=1.0389, d=0.9625, S0=100))
assets.append(asset(N=S, r=0.04, u=1.0752, d=0.93, S0=100))

uj = [0.11, 0.12, 0.15, 0.14]
alpha = 0.95
R = 0.14
h = 1/((1-alpha)*S)
number_assert = len(assets)

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




c , A_eq , b_eq, A_ub, b_ub, = init_function()

x = linprog.linprog(c = c, A_eq = A_eq, b_eq = b_eq, A_ub = A_ub, b_ub = b_ub)

print("result :")
print("calcul price en periode de l'option 1 par example : ")
print(assets[0].prices)
print("calcul price en periode de l'option 2 par example : ")
print(assets[1].prices)

print("VaR: ", x.x[n])
print("CVaR: ", x.fun)
print("Portfolio :", x.x[:n])



