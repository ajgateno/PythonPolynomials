class Polynomial:
	def __init__(self, terms):
		self.terms = terms
		self._simplify()
		self.__radd__ = self.__add__
		self.__rmul__ = self.__mul__
	
	def sort_term(self, labels):
		labels.sort()
	
	def group_like_terms(self):
		groups = {}
		for term in self.terms:
			mono = str({x:term[x] for x in term if x != "const"})
			if mono in groups:
				groups[mono].append(term)
			else:
				groups[mono] = [term]
		result = [groups[x] for x in groups]
		return result
	
	def copy(self):
		return Polynomial(self.terms.copy())
	
	def _simplify(self):
		for term in range(len(self.terms)):
			if "const" not in self.terms[term]:
				self.terms[term]["const"] = 1
		new_terms = []
		for term in range(len(self.terms)):
			new_term = {}
			for label in self.terms[term]:
				if self.terms[term][label] != 0:
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
				else:
					curr[label] = group[0][label]
			result.append(curr)
		self.terms = result
		self.terms = [x for x in self.terms if x["const"] != 0]
	
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
						else:
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
		return len(self.terms) == len(other.terms) and all([self.terms[x] in other.terms for x in range(len(self.terms))])

	def __pow__(self, other):
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
				if label != "const":
					curr += label + ("^" + str(term[label]) if term[label] != 1 else "")
			curr += " + "
			result += curr
		return result[:-2] if len(result) else ""
