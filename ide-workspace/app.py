m = 10

def h():
	s = 8
	print(s)
	print(m)

h()
class S:
	g = 2
	def __init__(self):
		print(m, "local")
		print(self.g, "properties")
S()