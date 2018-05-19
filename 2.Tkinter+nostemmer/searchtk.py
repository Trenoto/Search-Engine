import pickle
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
import math
import json



class searchEngine:

	def __init__(self, query,database):
		self.database = database
		self.datalist = []
		self.corpusCount = 37497
		self.query = query


	def token_query(self):
		self.datalist = []
		query_dict = {}
		tokenizer = RegexpTokenizer(r'\w+')
		stemmer = EnglishStemmer()
		query_t = tokenizer.tokenize(self.query.lower())

		for word in query_t:
			self.datalist.append(word)
			if word not in query_dict.keys():
				query_dict[word] = 1
			else:
				query_dict[word] += 1
		print(query_dict)
		return self.nlizeQuery(query_dict)

	def nlizeQuery(self, wordsdict):
		normalfactor = 0
		for word in wordsdict.keys():
			wordsdict[word] = 1 + math.log10(wordsdict[word])
			if word in self.database.keys():
				df = len(self.database[word])
				idf =  math.log10(self.corpusCount/df)
			else:
				idf = 0	
			# wt
			wordsdict[word] *= idf * wordsdict[word] 
			normalfactor += wordsdict[word]**2
		normalfactor = math.sqrt(normalfactor)
		for word in wordsdict.keys():
			if word in self.database.keys():
				wordsdict[word] = wordsdict[word]/normalfactor
			else:
				wordsdict[word] = 0
		# print(wordsdict)
		return wordsdict

	def cosineSim(self):
		cosim = {}
		query_dict = self.token_query() 
		for word in query_dict.keys():
			if word in self.database.keys():
				for docId in self.database[word].keys():
					if docId in cosim.keys():
						single_score = self.database[word][docId][0] * query_dict[word]
						cosim[docId] += single_score
					else:
						cosim[docId] = self.database[word][docId][0] * query_dict[word]
		return cosim

	def cstPhrase(self):
		cosim = self.cosineSim()
		wordlist = self.datalist
		if len(self.datalist) > 1:
			for i in range(len(wordlist)-1):
				if wordlist[i] in self.database.keys() and wordlist[i+1] in self.database.keys():
					for docId in cosim.keys():
						if docId in self.database[wordlist[i]].keys():
							if docId in self.database[wordlist[i+1]].keys():
								for j in range(len(self.database[wordlist[i]][docId])-1):
									for k in range(len(self.database[wordlist[i+1]][docId])-1):
										if self.database[wordlist[i+1]][docId][k+1] - self.database[wordlist[i]][docId][j+1] == 1:
											cosim[docId] *= 1.2
		return cosim
	def rankDoc(self):
		score = self.cstPhrase()
		return sorted(score.items(), key=lambda x: (-x[1], x[0]), reverse=False)

	def printResult(self):
		i= 0
		tklist = []
		result = self.rankDoc()
		# print(result)
		if len(result) == 0:
			print("no result")
		else:	
			with open("bookkeeping.json") as data_file:
				try:
					data = json.load(data_file)
				except ValueError:
					data ={}
			for docId in result:
				i += 1
				tklist.append(data[docId[0]])
				if i == 10:
					break
			print(i)
		return tklist