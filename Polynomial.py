
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
	
	def num_variables(self):
		"""
		Returns the number of indeterminates that comprise
		<self>
		"""
		return len(self.indets)
	
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
	
	def __eq__(self, other):
		return self.coeff == other.coeff and self.indets == other.indets
	
	def from_string(string):
		"""
		Makes a Monomial object from a string formatted as
		in LaTeX. Ordering is assumed to follow the 
		ordering of the input polynomial.
		"""
		new_indets = list()
		new_coeff = str()
		saw_dot = False
		done_with_coeff = False
		add_to_indets = False
		curr = ""
		for i in string:
			if not done_with_coeff:
				if i.isdigit():
					new_coeff += i
				elif i == "." and not saw_dot:
					new_coeff += i
					saw_dot = True
				else:
					new_coeff = float(new_coeff)
					done_with_coeff = True
			else:
				if i == "^":
					add_to_indets = True
				elif add_to_indets and i.isdigit():
					curr += i
				elif not saw_dot and add_to_indets and i == ".":
					curr += i
					saw_dot = True
				elif not i == "." and not i.isdigit():
					saw_dot = False
					add_to_indets = False
					new_indets.append(float(curr))
					curr = ""
		new_indets.append(float(curr))
		return Monomial(new_coeff, tuple(new_indets))

	
	def __repr__(self):
		return "{} * {}".format(self.coeff, self.indets)
