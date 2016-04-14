import random
	

def triples(string):
	""" 
	Generates triples from the given string. So if our string was 1234, the output would be (1,2,3) and (2,3,4)
	"""
	res=[]	
	if len(string) < 3:
		return
		
	for i in range(len(string) - 2):
		res.append((string[i], string[i+1], string[i+2]))
	return res
			
def markov_table(triples,database={}):
	for triple in triples:
		w1, w2, w3 = triple
		key = (w1, w2)
		if key in database:
			database[key].append(w3)
		else:
			database[key] = [w3]
	return database

string="121314151612131415"
triples=triples(string)
database=markov_table(triples)
print database