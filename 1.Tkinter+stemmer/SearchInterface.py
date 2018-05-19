
from tkinter import *
import webbrowser
import searchtk
import pickle


def callback(event):
	webbrowser.open_new(r"http://"+event.widget.cget("text"))

class Interface:
	def __init__(self):
		self.query = ""
		self.top = Tk()
		self.database = {}
		self.top.title("Search Engine")

	def load_pickle(self):
		with open("index.pickle",'rb') as handle:
			self.database = pickle.load(handle)

	def callback(event):
		webbrowser.open_new(r"http://"+self.url)


	def __print_result(self):

		self.query = self.entry.get()
		se = searchtk.searchEngine(self.query,self.database)
		self.new_window = Toplevel(self.top)
		self.new_window.title("Result")
		# self.new_window.geometry('{}x{}'.format(1000, 500))
		result = se.printResult()
		sp = se.ssnippet()
		if len(self.query) == 0:
			label = Label(self.new_window, text = "Please Enter your query")
		elif len(result) == 0:
			label = Label(self.new_window, text = "No Result")
		else: 
			label = Label(self.new_window, text = "Showing the first " + str(len(result)) + " result(s) for \""+ self.query  + "\":")
		label.pack()
		for i in range(len(result)):
			link = Label(self.new_window, text=result[i], fg="blue", cursor="hand2")
			lb = Label(self.new_window, text = "Snippet: "+ sp[i])
			link.pack()
			lb.pack()
			link.bind("<Button-1>", callback)



	def create_widge(self):
		self.top.geometry('{}x{}'.format(1000, 500))
		label = Label(self.top, text = "Enter your query:")
		self.entry = Entry(self.top)
		self.entry.pack()
		button1 = Button(self.top, text = "Show", command = self.__print_result)
		button2 = Button(self.top, text = "Quit", command = self.top.quit)
		label.place(relx=.5, rely=.42, anchor="center")
		self.entry.place(relx=.5, rely=.5, anchor="center")
		button1.place(relx=.45, rely=.57, anchor="center")
		button2.place(relx=.52, rely=.57, anchor="center")

		self.top.mainloop()


interface = Interface()
interface.load_pickle()
interface.create_widge()