#Project 3 Part1
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
import lxml
import io
import pickle

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

		data = open(folder_path).read()
		text = BeautifulSoup(data, "lxml").get_text()
		words = tokenizer.tokenize(text)

		print("Indexing: ", folder_path)
		
		for word in words:
			if word.lower() in wordsdict.keys():
				wordsdict[word.lower()] += 1
			else:
				wordsdict[word.lower()] = 1
		return wordsdict
		# print doc_dict

	def files_to_words(self):
		files = {}
		for folder_path in self.folder_list:
			files[folder_path] = self.token_file(folder_path)
		return files


	def buildInvertedIndex(self):
		files = self.files_to_words()
		invertedIndex = {}
		for file_name in files.keys():
			for word in files[file_name].keys():
				if word not in invertedIndex.keys():

					invertedIndex[word] = []
					invertedIndex[word].append(file_name)
				else:
					invertedIndex[word].append(file_name)
		# print(invertedIndex)
		return dict(invertedIndex)

	def set_default(self):
		if isinstance(self, set):
			return list(self)
		raise TypeError

	def getNumber(self):
		return self.corpusCount

	def write_to_file(self, target):
		print("q")
		with open('m2.pickle', 'wb') as handle:
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



