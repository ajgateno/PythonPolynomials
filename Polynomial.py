
class Polynomial:
	pass


class Monomial:
	def __init__(self, coeff, indets):
		"""
		Initializes a monomial with coefficient <coeff>
		and len(<indets>) many intedeterminates, whose 
		powers are determinedby the entries of the tuple 
		<indets>.

		<indets> is a tuple with scalar entries.
		<coeff> is a scalar coefficient.
		"""
		self.coeff = coeff
		self.indets = indets
	
	def __add__(self, other):
		"""
		Takes as inputs two Monomials and outputs the
		Monomial representing the sum of the two iff
		the two monomials have the same indetermin-
		ates.
		"""
		if (self.indets == other.indets):
			new_coeff = self.coeff + other.coeff
			new_indets = self.indets
			return Monomial(new_coeff, new_indets)
		else:
			raise Exception("Incompatible indets {} and {} in Monomial addition".format(self.indets,other.indets))
	
	def __eq__(self, other):
		return self.coeff == other.coeff and self.indets == other.indets
	
	def __repr__(self):
		return "{} * {}".format(self.coeff, self.indets)
