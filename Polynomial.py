class Polynomial:
	def __init__(self, terms):
		self.terms = terms
		self.leading_term = 0
		self._simplify()
	
	def sort_term(self, labels):
		labels.sort()
	
	def sort(self):
		"""
		sort monomials in lex order, to include more orderings later on down the line.
		"""
		self.terms.sort(key=lambda x : x["tup"], reverse=True)
	
	def group_like_terms(self):
		groups = {}
		for term in self.terms:
			labels = [(x,term[x]) for x in list(term.keys()) if x != "const" and x != "tup"]
			labels.sort()
			mono = str({labels[x][0]:labels[x][1] for x in range(len(labels))})
			if mono in groups:
				groups[mono].append(term)
			else:
				groups[mono] = [term]
		result = [groups[x] for x in groups]
		return result
	
	def copy(self):
		return Polynomial(self.terms.copy())
	
	def divided_by(self, others):
		result = [0 for x in others]
		p = self.copy()
		r = 0
		while p != 0:
			i = 0
			divided = False
			while i < len(others) and not divided:
				if Polynomial.does_term_divide(others[i].terms[0],p.terms[0]):
					result[i] = result[i] + Polynomial.term_divide(p.terms[0],others[i].terms[0])
					p = p - Polynomial.term_divide(p.terms[0],others[i].terms[0]) * others[i]
					divided = True
				else:
					i = i + 1
			if not divided:
				r = r + p.get_leading_term()
				p = p - p.get_leading_term()
		return result, r
	
	def does_term_divide(a, b):
		# check that monomials have the same indeterminates, and for each indet, a_i <= b_i
		for label in a:
			if label not in b:
				return False
			if label not in ["const", "tup"] and a[label] > b[label]:
				return False
		return True
	
	def term_divide(a, b):
		if not Polynomial.does_term_divide(b, a):
			return None
		result = {}
		for label in a:
			if label == "const":
				result[label] = a[label] / b[label]
			elif label != "tup":
				result[label] = a[label] - b[label]
		return Polynomial([result])
	
	def _simplify(self):
		for term in range(len(self.terms)):
			if "const" not in self.terms[term]:
				self.terms[term]["const"] = 1
		new_terms = []
		for term in range(len(self.terms)):
			new_term = {}
			for label in self.terms[term]:
				if self.terms[term][label] != 0 and label != "tup":
					new_term[label] = self.terms[term][label]
			new_terms.append(new_term)
		self.terms = new_terms
		result = []
		like_terms = self.group_like_terms()
		for group in like_terms:
			curr = {}
			labels = list(group[0].keys())
			for label in labels:
				if label == "const":
					curr[label] = sum([x[label] for x in group])
				elif label != "tup":
					curr[label] = group[0][label]
			if len(curr):
				result.append(curr)
		self.terms = result
		if self.terms:
			self.terms = [x for x in self.terms if x["const"] != 0]
		order = set()
		for i in self.terms:
			for j in i:
				if j != "const" and j != "tup":
					order.add(j)
		order = list(order)
		self.sort_term(order)
		for term in range(len(self.terms)):
			curr = tuple()
			for label in order:
				if label not in self.terms[term]:
					curr += (0,)
				elif label != "const" and label != "tup":
					curr += (self.terms[term][label],)
			self.terms[term]["tup"] = curr
		self.sort()
		if len(self.terms) > 1:
			self.leading_term = Polynomial([self.terms[0]])
		else:
			self.leading_term = self
	
	def get_leading_term(self):
		return self.leading_term

	def __floordiv__(self, other):
		if type(other) in [int,complex,float]:
			return self // [Polynomial([{'const':other}])]
		if type(other) is not list:
			return self // [other]
		return self.divided_by(other)[0]
	
	def __mod__(self,other):
		if type(other) in [int,complex,float]:
			return self % [Polynomial([{'const':other}])]
		if type(other) is not list:
			return self % [other]
		return self.divided_by(other)[1]
	
	def __add__(self, other):
		if type(other) in [int,float,complex]:
			return self + Polynomial([{'const':other}])
		return Polynomial(self.terms + other.terms)
	
	def __radd__(self, other):
		return self + other
	
	def __neg__(self):
		result = []
		for term in self.terms:
			curr = term.copy()
			curr["const"] = -curr["const"]
			result.append(curr)
		return Polynomial(result)
	
	def __sub__(self, other):
		return self + -other
	
	def __rsub__(self, other):
		return -self + other
	
	def __mul__(self, other):
		if other == 0:
			return Polynomial([])
		if type(other) in [int,float,complex]:
			return self * Polynomial([{'const':other}])
		result = []
		for term in range(len(self.terms)):
			for oterm in range(len(other.terms)):
				curr = self.terms[term].copy()
				for label in other.terms[oterm]:
					if label in curr:
						if label == "const":
							curr[label] *= other.terms[oterm][label]
						elif label != "tup":
							curr[label] += other.terms[oterm][label]
					else:
						curr[label] = other.terms[oterm][label]
				result.append(curr)
		return Polynomial(result)
	
	def __rmul__(self, other):
		return self * other
	
	def __eq__(self, other):
		if type(other) in [int,float,complex]:
			return self == Polynomial([{'const': other}])
		return self.terms == other.terms or len(self.terms) == len(other.terms) and all([self.terms[x] in other.terms for x in range(len(self.terms))])

	def __pow__(self, other):
		if other == 1:
			return Polynomial([{'const':1}])
		if type(other) is int:
			result = self.copy()
			for i in range(other - 1):
				result *= result
			return result
		else:
			raise Exception("unsupported operand type(s) for ** or pow(): 'Polynomial' and '" + type(other).__name__ + "'")

	def __repr__(self):
		if not self.terms:
			return "0"
		result = ""
		for term in self.terms:
			curr = ""
			if "const" in term:
				curr += str(term["const"])
			labels = list(term.keys())
			self.sort_term(labels)
			for label in labels:
				if label != "const" and label != "tup":
					curr += label + ("^" + str(term[label]) if term[label] != 1 else "")
			curr += " + "
			result += curr
		return result[:-2] if len(result) else ""
