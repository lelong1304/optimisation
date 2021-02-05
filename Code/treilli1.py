import numpy

class treilliVente():

    #N = 5 r = 0.04 u = 1.0425 d = 0.9592 K = 98 S0 = 100
    def __init__(self, N, r, u, d, K, S0):
        self.N = N
        self.r = r
        self.u = u
        self.d = d
        self.K = K
        self.S0 = S0
        self.R = 0
        self.p_u = 0
        self.p_d = 0
        self.probability()

    def probability(self):
        self.R=1+(self.r/52)
        self.p_u = (self.R-self.d)/(self.u-self.d)
        self.p_d = (self.u-self.R)/(self.u-self.d)

    def calcul_price_option(self):
        S = numpy.zeros([self.N+1,self.N+1])
        S[0,0] = self.S0
        for i in range(self.N+1):
            for j in range(i+1):
                S[i,j] = self.S0 * pow(self.u,j) * pow(self.d,(i-j))
        return S

    def EuroVente(self):
        S = self.calcul_price_option()
        #R, p_u, p_d = probability(T,N,d,u,r)
        V = numpy.zeros([self.N+1,self.N+1])
        print(S[self.N, 3])
        for j in range(self.N+1):
            V[self.N,j] = max(self.K-S[self.N, j], 0)

        for i in range(self.N-1,-1,-1):
            for j in range(i+1):
                V[i,j] = (self.p_u*V[i+1,j+1] + self.p_d*V[i+1,j])/self.R
        return V



    def AmericanVente(self):
        S = self.calcul_price_option()
        V = numpy.zeros([self.N+1,self.N+1])

        for j in range(self.N+1):
            V[self.N,j] = max(self.K-S[self.N, j], 0)

        for i in range(self.N-1,-1,-1):
            for j in range(i+1):
                V[i,j] = max((self.p_u*V[i+1,j+1] + self.p_d*V[i+1,j])/self.R, max(self.K-S[i,j],0))
        return V


vente = treilliVente(N = 400, r = 0.04, u = 1.0366, d = 0.9646, K = 98, S0 = 100)



V1 = vente.EuroVente()
for i in range(vente.N,-1,-1):
    print("i=",i, end =" ")
    for j in range(i+1):
        print(" V[",i,",",j,"] = ", V1[i,j], end =" ")
    print(" ")




V2 = vente.AmericanVente()
for i in range(vente.N,-1,-1):
    print("i=",i, end =" ")
    for j in range(i+1):
        print(" V[",i,",",j,"] = ", V2[i,j], end =" ")
    print(" ")
print("Le prix de l’option Europeenne est: ", V1[0,0])
print("Le prix de l’option American est: ", V2[0,0])


