from types import SimpleNamespace


class MarketModel:
    def __init__(self):

        self.par = SimpleNamespace()

        # a. preferences
        self.par.alpha = 1/3
        self.par.beta = 2/3

        # b. endowments
        self.par.w1A = 0.8
        self.par.w2A = 0.3
        self.par.w1B = 1 - self.par.w1A
        self.par.w2B = 1 - self.par.w2A
        self.par.w1 = self.par.w1A + self.par.w1B
        self.par.w2 = self.par.w2A + self.par.w2B


        #c. P2 numeaire
        self.p2 = 1

        #Initial values
        self.par.N1 = 10
        self.par.N2 = 5

    def utility_A(self, x1, x2):
        u = x1**self.par.alpha * x2**(1-self.par.alpha)
        return u

    #Define the utility for B
    def utility_B(self, x1, x2):
        u =  x1**self.par.beta * x2**(1-self.par.beta)
        return u

    #Define A's demand
    def demand_A(self, p1, p2):
        x1 = self.par.alpha * (p1 * self.par.w1A + p2 * self.par.w2A) / p1
        x2 = (1 - self.par.alpha) * (p1 * self.par.w1A + p2 * self.par.w2A) / p2
        return x1, x2

    #Define B's demand
    def demand_B(self, p1, p2):
        x1 = self.par.beta * (p1 * self.par.w1B + p2 * self.par.w2B) / p1
        x2 = (1 - self.par.beta) * (p1 * self.par.w1B + p2 * self.par.w2B) / p2
        return x1, x2


    def check_market_clearing(self,p1):

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2