#Project 3 Part1
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
import lxml
import io
import pickle
import math

class Milestone:

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
		stemmer = EnglishStemmer()
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


		print("Folder: ", folder_path)
		
		for word in body_t:
			if word.lower() in wordsdict.keys():
				wordsdict[word.lower()][0] += 1
				wordsdict[word.lower()].append(word_position)
				word_position += 1
			else:
				wordsdict[word.lower()] = []
				wordsdict[word.lower()].append(1)
				wordsdict[word.lower()].append(word_position)
				word_position += 1

		counter = 0
		if len(title_t) > 0:		
			for word in title_t:
				wordsdict[word.lower()][0] += 9
				counter += 1
				if counter == 10:
					break

		if len(h1_t) > 0:
			for word in h1_t:
				wordsdict[word.lower()][0] += 4
		if len(h2_t) > 0:
			for word in h2_t:
				wordsdict[word.lower()][0] += 4
		if len(h3_t) > 0:
			for word in h3_t:
				wordsdict[word.lower()][0] += 4
		if len(bold_t) > 0:
			for word in bold_t:
				wordsdict[word.lower()][0] += 2
		if len(strong_t) > 0:
			for word in strong_t:
				wordsdict[word.lower()][0] += 2

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

	def set_default(self):
		if isinstance(self, set):
			return list(self)
		raise TypeError

	def getNumber(self):
		return self.corpusCount

	def write_to_file(self, target):
		print("q")
		with open('index1.pickle', 'wb') as handle:
  			pickle.dump(target, handle)

	# def write_to_file(self, target):
	# 	print("q")
	# 	file =  open('m1.text', 'w')
	# 	file.write(target)
	# 	file.close()



if __name__ == "__main__":
	temp = Milestone("bookkeeping.json")
	temp.read_json()
	stored_dict = temp.buildInvertedIndex()
	temp.write_to_file(stored_dict)
	number_of_file = temp.getNumber()
	print(number_of_file)
	# temp.search_for_token()
	#temp.print_result()



