def first():
	print("fuck me")

def second(x):
	print(x)

funcs = {
	"first": first, 
	"second": lambda x: second(x),
}

funcs["first"]()
funcs["second"](3)
