class Crypt(object):
	chars_ = list(set(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.,@#$_&-+()/*\"':;!?~`|={}\\%[] ")))
	chars = ""
	for i in chars_:chars = chars + i

	def __init__(self, key=0.0):
		"""create new Crypt object. Crypt(key=0.0)"""
		self.setKey(key)
		self._char = list(Crypt.chars)
		self._enc1 = list(Crypt.chars)
		self._enc2 = list(Crypt.chars)
		self._reset()
		
	def setKey(self, key):
		"""set encryption key."""
		self.key = str(key)
		if int(key.split(".")[0]) > 20 or int(key.split(".")[1]) > 20:raise ValueError("invalid key")
		self._reset()
		
	def _reset(self):
		self._enc1 = list(Crypt.chars)
		self._enc2 = list(Crypt.chars)
		k1 = int(self.key.split(".")[0])
		self._enc1.extend(self._enc1[:k1])
		del self._enc1[:k1]
		k2 = int(self.key.split(".")[1])
		self._enc2.extend(self._enc2[:k2])
		del self._enc2[:k2]
		
	def _flip(self):
		# self._enc2.insert(0, self._enc2[-1])
		# del self._enc2[-1]
		self._enc2.append(self._enc2[0])
		del self._enc2[0]
		
	def encrypt(self, value):
		value = list(str(value))
		res = ''
		for char in value:
			if char in self._char:
				key = self._enc1.index(char)
				res_ = self._enc2[key]
				res = res + res_
			else:
				res = res+char
			self._flip()
		self._reset()
		return res
		
	def decrypt(self, value):
		value = list(str(value))
		res = ''
		for char in value:              
			if char in self._char:
				key = self._enc2.index(char)
				res_ = self._enc1[key]
				res = res + res_
			else:
				res = res+char
			self._flip()
		self._reset()
		return res
	
	def write(self, filename, data):
		cdata = self.encrypt(data)
		with open(filename, 'w') as f:
			f.write(cdata)
		return len(cdata)
	
	def read(self, filename):
		with open(filename) as f:
			cdata = f.read()
		data = self.decrypt(cdata)
		return data
