
class Polynomial:
	def __init__(self, monos):
		"""
		Initializes a new polynomial with monomials <monos>
		"""
		self.monos = monos
	
	def total_deg(self):
		"""
		Get the total degree of this polynomial
		"""
		return max([x.deg() for x in self.monos])
	
	def sort(self, ordering="lex"):
		"""
		Order this polynomial with one of three monomial orderings
		- lex
		- grlex TODO
		- grevlex TODO
		"""
		if ordering == "lex":
			self.monos.sort(reverse=True, key=(lambda x : x.indets))
	
	def copy(self):
		"""
		Get a deep copy of this Polynomial
		"""
		return Polynomial([x.copy() for x in self.monos])
	
	def get_leading_term(self):
		"""
		get the leading term of this Polynomial
		"""
		cpy = self.copy()
		return cpy.monos[0]

	def get_leading_coeff(self):
		"""
		get the leading coefficient of this Polynomial
		"""
		return self.get_leading_term().coeff
	
	def get_leading_indets(self):
		"""
		get the leading indets of this Polynomial
		"""
		return self.get_leading_term().indets
	
	def __add__(self, other):
		"""
		Adds two polynomials, <self> and <other>, together.
		"""
		new_monos = list()
		for i in range(len(self.monos)):
			appended = False
			for j in range(len(other.monos)):
				if self.monos[i].indets == other.monos[j].indets and not appended:
					new_monos.append(self.monos[i] + other.monos[j])
					appended = True
			if not appended:
				new_monos.append(self.monos[i])
		result = Polynomial(new_monos)
		result.flush()
		return result
	
	def __neg__(self):
		"""
		Returns the additive inverse of this polynomial
		"""
		return Polynomial([-a for a in self.monos])
	
	def __sub__(self, other):
		"""
		Subtracts the polynomial <other> from the polynomial <self>
		"""
		return self + -other
	
	def flush(self):
		"""
		Get rid of zero terms in our <self.monos> list
		and TODO: combine like terms
		"""
		new_monos = list()
		for i in self.monos:
			if i.coeff != 0: # Monomials with coeff == 0 are reduntant
				new_monos.append(i)
		self.monos = new_monos
	
	def __repr__(self):
		"""
		Return a string representation of our Polynomial object
		"""
		result = ""
		for i in self.monos:
			result += str(i) + " + "
		return result[:-3] if len(self.monos) > 0 else "0"
	
	def __eq__(self, other):
		"""
		Return whether two polynomials are equal
		"""
		return len(self.monos) == len(other.monos) and all([x in other.monos for x in self.monos])


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
	
	def num_variables(self):
		"""
		Returns the number of indeterminates that comprise
		<self>
		"""
		return len(self.indets)
	
	def copy(self):
		"""
		get a deep copy of this Monomial
		"""
		return Monomial(self.coeff, self.indets)
	
	def divides(self, other):
		"""
		Takes two Monomials and outputs True iff <self>
		divides other. Variable ordering is assumed to
		follow the order of the <.indets> tuple.
		"""
		if self.num_variables() <= other.num_variables():
			for i in range(self.num_variables()):
				if self.indets[i] != other.indets[i]:
					return False
			return True
		return False
	
	def deg(self):
		return sum(self.indets)
	
	def __eq__(self, other):
		return self.coeff == other.coeff and self.indets == other.indets
	
	def __neg__(self):
		return Monomial(-self.coeff, self.indets)

	def __sub__(self, other):
		return self + -other

	def __mul__(self, other):
		"""
		Get the product of two monomials
		"""
		op1 = self.copy()
		op2 = other.copy()
		if self.num_variables() < other.num_variables():
			p = [0 for x in range(other.num_variables() - self.num_variables())]
			op1.indets += tuple(p)
		elif self.num_variables() > other.num_variables():
			p = [0 for x in range(self.num_variables() - other.num_variables())]
			op2.indets += tuple(p)
		new_coeff = op1.coeff * op2.coeff
		new_indets = [op1.indets[i] + op2.indets[i] for i in range(op1.num_variables())]
		return Monomial(new_coeff, tuple(new_indets))

	def __repr__(self):
		return "{} * {}".format(self.coeff, self.indets)