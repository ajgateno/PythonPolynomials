from Polynomial import Polynomial

class Ideal:
    def __init__(self, basis):
        self.basis = Ideal.standardize(basis)
    
    def standardize(basis):
        # run Buchberger's algorithm to standardize the input basis
        result = basis.copy()
        done = False
        while not done:
            current = result.copy()
            for p in range(len(current)):
                for g in range(p, len(current)):
                    if current[p] != current[g]:
                        s = Polynomial.s_polynomial(current[p],current[g]) % current
                        if s != 0:
                            result.append(s)
            done = (current == result)
        return result
    
    def __contains__(self, other):
        # assume other is a polynomial
        return other % self.basis == 0