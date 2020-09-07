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
            for p in current:
                for g in current:
                    if p != g:
                        s = Polynomial.s_polynomial(p,g) % current
                        if s != 0:
                            result.append(s)
            done = (current == result)
        return result
    
    def __contains__(self, other):
        # assume other is a polynomial
        return other % self.basis == 0