import random
	

def triples(lst):
	""" 
	Generates triples from the given string. So if our string was 1234, the output would be (1,2,3) and (2,3,4)
	"""
	res=[]	
	if len(lst) < 3:
		return
		
	for i in range(len(lst) - 2):
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

def generate_string(seed,length,database):
	output=[]
	output.append(seed[0])
	output.append(seed[1])
	for i in range(length-2):
		i=i+2
		key=(output[i-2],output[i-1])
		options=database.get(key)
		next_state=random.choice(options)
		output.append(next_state)
	output = ''.join(output)
	return output


string=['1','2','3','5','2','6','23','1','5','3','76','4','2','3','6','3','3','3','6','7','4','6','3','6','3','6','7','8']
triples=triples(string)
database=markov_table(triples)
string=generate_string(['1','2'],15,database)
print string