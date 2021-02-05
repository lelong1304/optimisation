import numpy as np

N = 5
r = 0.04
d = 0.9592
u = 1.0425
K = 98
S0 = 100

R = 1+(r/52)
p_u = (R-d)/(u-d)
p_d = (u-R)/(u-d)


def calcul_option_price():
    S = np.zeros([N+1,N+1])
    S[0,0] = S0
    for i in range(N+1):
        for j in range(i+1):
            S[i,j] = S0*pow(u,j)*pow(d,(i-j))
    return S
S = calcul_option_price()
def calcul_vente_Euro():

    V = np.zeros([N+1,N+1])

    for j in range(N+1):
        V[N,j] = max(K-S[N,j], 0)

    for i in range(N-1,-1,-1):
        for j in range(i+1):
            V[i,j] = 1/R * (p_u*V[i+1,j+1] + p_d*V[i+1,j])
    return V

def calcul_vente_American():
    V = np.zeros([N+1,N+1])

    for j in range(N+1):
        V[N,j] = max(K-S[N,j], 0)

    for i in range(N-1,-1,-1):
        for j in range(i+1):
            V[i,j] = max((p_u*V[i+1,j+1] + p_d*V[i+1,j])/R, max(K-S[i,j],0))
    return V

print(p_u, p_d, R)
v1 = calcul_vente_Euro()
print(v1)
print("\nPrice of EU Put: ", v1[0,0])
v2 = calcul_vente_American()
print(v2)
print("\nPrice of Ame Put: ", v2[0,0])
