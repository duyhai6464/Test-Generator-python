from math import log
import time, sys, pathlib

MAXN = 10**30

# Generates a list of the first primes (with product > MAXN).
def gen_primes():
	primes = []
	primes_product = 1
	for n in range(2, 10**10):
		is_prime = True
		for i in range(2, n):
			if n % i == 0:
				is_prime = False
		if is_prime: 
			primes.append(n)
			primes_product *= n
			if primes_product > MAXN: break
	return primes
primes = gen_primes()
print(f'We only need primes {primes} for MAXN = {MAXN}')

# Generates a list of the hcn <= MAXN.
def gen_hcn():
    # List of (number, number of divisors, exponents of the factorization)
	hcn = [(1, 1, [])]
	for i in range(len(primes)):
		new_hcn = []
		for el in hcn:
			new_hcn.append(el)
			if len(el[2]) < i: continue
			e_max = el[2][i-1] if i >= 1 else int(log(MAXN, 2))
			n = el[0]
			for e in range(1, e_max+1):
				n *= primes[i]
				if n > MAXN: break
				div = el[1] * (e+1)
				exponents = el[2] + [e]
				new_hcn.append((n, div, exponents))
		new_hcn.sort()
		hcn = [(1, 1, [])]
		for el in new_hcn:
			if el[1] > hcn[-1][1]: hcn.append(el)
	return hcn

start = time.time()
hcn = gen_hcn()
# From here on is only pretty printing.
print("Number of highly composite numbers less than", MAXN, "is", len(hcn),"\n")

def PrintWithCorrectSpaces(a, b, c):
	aspace = int(log(MAXN, 10)) + 5
	bspace = int(log(hcn[-1][1], 10)) + 5
	assert(len(a) < aspace)
	assert(len(b) < bspace)
	
	print(a, " "*(aspace-len(a)), b, " "*(bspace-len(b)), c)

def Factorization(exps: list):
	return "*".join([str(primes[i])+("^"+str(exps[i]) if exps[i]>1 else "") for i in range(len(exps))])
	 
PrintWithCorrectSpaces("number", "divisors", "factorization")

for el in hcn:
	PrintWithCorrectSpaces(str(el[0]), str(el[1]), Factorization(el[2]))

print(f"TIME: {time.time() - start:0.3f}")
ROOT = pathlib.Path(__file__).resolve().parent
sys.stdout = open(ROOT / "HCN.txt", 'w')
print(*[el[0] for el in hcn], sep=',')
print(*[el[1] for el in hcn], sep=',')
