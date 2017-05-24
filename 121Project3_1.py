#Project 3 Part1
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer

class Milestone:

	def __init__(self, json_file_name):
		self.json_file = json_file_name
		self.folder_list = []
		self.tf_dict = defaultdict(list)

	def read_json(self):
		with open(self.json_file) as data_file:
			data = json.load(data_file)
		for d in data:
			self.folder_list.append(d.encode('utf-8'))

	def tokenize_file_and_get_tf(self):
		file = open("tf.txt", "a")
		tokenizer = RegexpTokenizer(r'\w+')
		important_token_set = set()
		count = 0
		for folder_path in self.folder_list:
			normal_tf = defaultdict(int)
			important_tf = defaultdict(int)
			data = open(folder_path).read()
			soup = BeautifulSoup(data, 'lxml')

			#normal tokens which appear in body tag
			for sentence in soup.find_all("body"):
				tokens = tokenizer.tokenize(sentence.text.encode("utf-8"))
				for token in tokens:
						normal_tf[token] += 1 

			print(normal_tf)

			#important tokens which appear in header, bold, title and strong
			for bold_text in soup.find_all("b"):
				for token in tokenizer.tokenize(bold_text.text.encode('utf-8')):
					important_token_set.add(token)
			for h1 in soup.find_all("h1"):
				for token in tokenizer.tokenize(h1.text.encode('utf-8')):
					important_token_set.add(token)
			for h2 in soup.find_all("h2"):
				for token in tokenizer.tokenize(h2.text.encode('utf-8')):
					important_token_set.add(token)
			for h3 in soup.find_all("h3"):
				for token in tokenizer.tokenize(h3.text.encode('utf-8')):
					important_token_set.add(token)
			for p in soup.find_all("p"):
				for token in tokenizer.tokenize(p.text.encode('utf-8')):
					important_token_set.add(token)
			for header in soup.find_all("header"):
				for token in tokenizer.tokenize(header.text.encode('utf-8')):
					important_token_set.add(token)
			for strong in soup.find_all("strong"):
				for token in tokenizer.tokenize(strong.text.encode('utf-8')):
					important_token_set.add(token)

			# for token in important_token_set:
			# 	important_tf[token] += (normal_tf[token] + 1)

			file.write("doc:" + folder_path + "\n")
			# file.write("important token:" + "\n")

			# for key, value in important_tf.items():
			# 	file.write(key + ": " + str(value) + "\n")
			file.write("normal token:" + "\n")
			for key, value in normal_tf.items():
				file.write(key + ": "+ str(value)  + "\n")

			# self.tf_dict[folder_path].append(important_tf)
			# self.tf_dict[folder_path].append(normal_tf)
		file.close()

	def print_result(self):
		print(len(self.tf_dict))




if __name__ == "__main__":
	temp = Milestone("bookkeeping.json")
	temp.read_json()
	temp.tokenize_file_and_get_tf()
	#temp.print_result()



