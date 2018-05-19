#Project 3 Part1
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from pymongo import MongoClient
import lxml
import io
import pickle
import math

class buildMongoDB:

	def __init__(self, json_file_name):
		self.json_file = json_file_name
		self.folder_list = []
		self.corpusCount = 0
		
	def read_json(self):
		with open(self.json_file) as data_file:
			try:
				data = json.load(data_file)
			except ValueError:
				data ={}
		for d in data:
			self.corpusCount = self.corpusCount + 1
			self.folder_list.append(d)
			# print(d)

	def token_file(self, folder_path):
		# file = open("tf.txt", "a")
		tokenizer = RegexpTokenizer(r'\w+')
		stemmer = PorterStemmer()
		wordsdict = {}
		i = 0
		word_position = 0

		body = ""
		title = ""
		h1 = ""
		h2 = ""
		h3 = ""
		bold = ""
		strong = ""
		data = open(folder_path).read()
		# it counts title, h1, h2, h3 , b ,strong again
		for i in BeautifulSoup(data, "lxml").find_all("html"):
			body = i.text + body + " "
		body_t = tokenizer.tokenize(body)
		# title in this project is quoted by <P> </P>, only counts the first one
		for i in BeautifulSoup(data, "lxml").find_all("p"):
			title = i.text + title + " "
			break
		title_t = tokenizer.tokenize(title)
		for i in BeautifulSoup(data, "lxml").find_all("h1"):
			h1 = i.text + h1 + " "
		h1_t = tokenizer.tokenize(h1)
		for i in BeautifulSoup(data, "lxml").find_all("h2"):
			h2 = i.text + h2 + " "
		h2_t = tokenizer.tokenize(h2)
		for i in BeautifulSoup(data, "lxml").find_all("h3"):
			h3 = i.text + h1 + " "
		h3_t = tokenizer.tokenize(h3)
		for i in BeautifulSoup(data, "lxml").find_all("b"):
			bold = i.text + bold + " "
		bold_t = tokenizer.tokenize(bold)
		for i in BeautifulSoup(data, "lxml").find_all("strong"):
			strong = i.text + strong + " "
		strong_t = tokenizer.tokenize(strong)


		print("Indexing: ", folder_path)
		
		for word in body_t:
			if stemmer.stem(word) in wordsdict.keys():
				wordsdict[stemmer.stem(word)][0] += 1
				wordsdict[stemmer.stem(word)].append(word_position)
				word_position += 1
			else:
				wordsdict[stemmer.stem(word)] = []
				wordsdict[stemmer.stem(word)].append(1)
				wordsdict[stemmer.stem(word)].append(word_position)
				word_position += 1

		counter = 0		
		for word in title_t:
			wordsdict[stemmer.stem(word)][0] += 5
			counter += 1
			if counter == 10:
				break

		for word in h1_t:
			wordsdict[stemmer.stem(word)][0] += 3

		for word in h2_t:
			wordsdict[stemmer.stem(word)][0] += 3

		for word in h3_t:
			wordsdict[stemmer.stem(word)][0] += 3

		for word in bold_t:
			wordsdict[stemmer.stem(word)][0] += 1

		for word in strong_t:
			wordsdict[stemmer.stem(word)][0] += 1

		return wordsdict

	def nlizeTermFreq(self,wordsdict):
		normalfactor = 0
		for word in wordsdict.keys():
			wordsdict[word][0] = 1 + math.log10(wordsdict[word][0])
			normalfactor += wordsdict[word][0]**2
		normalfactor = math.sqrt(normalfactor)
		for word in wordsdict.keys():
			wordsdict[word][0] = wordsdict[word][0]/normalfactor
		return wordsdict

	def pages_to_words(self):
		pages = {}
		for folder_path in self.folder_list:
			pages[folder_path] = self.nlizeTermFreq(self.token_file(folder_path))
		return pages


	def buildInvertedIndex(self):
		pages = self.pages_to_words()
		invertedIndex = {}
		for file_name in pages.keys():
			for word in pages[file_name].keys():
				if word not in invertedIndex.keys():

					invertedIndex[word] = {}
					invertedIndex[word][file_name] = []
					invertedIndex[word][file_name] = pages[file_name][word]
				else:
					invertedIndex[word][file_name] = []
					invertedIndex[word][file_name] = pages[file_name][word]
		# print(invertedIndex)
		return invertedIndex

	# def store_to_mgdb(self,invertedIndex):
	# 	client = MongoClient()
	# 	db = client['index-test']
	# 	table = db.wordIndex
	# 	for word in invertedIndex.keys():
	# 		database = {}
	# 		database["_id"] = word
	# 		database.update(invertedIndex[word])
	# 		table.insert(database)
	# 	size = self.getNumber()
	# 	database = {}
	# 	database["_id"] = "corpusCount"
	# 	database["corpusCount"] = size

	def write_to_file(self, target):
		print("q")
		with open('index1.pickle', 'wb') as handle:
  			pickle.dump(target, handle)


	def getNumber(self):
		return self.corpusCount



if __name__ == "__main__":
	temp = buildMongoDB("bookkeeping.json")
	temp.read_json()
	invertedIndex = temp.buildInvertedIndex()
	# temp.store_to_mgdb(invertedIndex)
	temp.write_to_file(invertedIndex)
	number_of_file = temp.getNumber()
	print(number_of_file)
	# temp.search_for_token()
	#temp.print_result()



