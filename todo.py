#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	  pypodcatcher.py : A simple podcast client commandline software
	
	           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004
 
	Copyright (C) 2013 Thomas Maurice <tmaurice59@gmail.com>
	 
	Everyone is permitted to copy and distribute verbatim or modified
	copies of this license document, and changing it is allowed as long
	as the name is changed.
	 
		         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
		TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
	 
	 0. You just DO WHAT THE FUCK YOU WANT TO.
	 
"""

__author__ = "Thomas Maurice"
__copyright__ = "Copyright 2014, Thomas Maurice"
__license__ = "WTFPL"
__version__ = "0.2"
__maintainer__ = "Thomas Maurice"
__email__ = "tmaurice59@gmail.com"
__status__ = "Development"

import xml.dom.minidom as minidom
import sys
import os
from termcolor import *

class TodoList:
	"""
		TodoList class implementation

		This class is used to represend a todo list object.
		It has several components. On the one hand some
		general info about the todo list (the filename
		the xml nodelist...) and a more conveinient to use
		xml nodelist with only the interesting xml nodes.
		This is to say that you shall never use the *self.todo_file*
		xml nodelist but  always the *self.todo_list*

		The main important variables here are:
		 - self.todo_file_name: Obviously the xml file
		 - self.todo_file: The xml nodelist directly loaded from the file
		 - self.todo_list: The xml nodelist stripped from the blank one
	"""
	def __init__(self, todo_file):
		"""
			Initializes a TodoList obect from an XML file
		"""
		self.todo_file_name = todo_file
		try:
			self.todo_file = minidom.parse(todo_file)
			self.regenerate_todo_list()
			
		except:
			self.create_new_file(todo_file)
			print "The file was non-existant, created it"
			self.todo_file = minidom.parse(todo_file)
			self.regenerate_todo_list()
	
	def regenerate_todo_list(self):
		"""
			Regenerates the self.todo_list variable
			
			This will strip out the blank nodes of
			the main xml nodelist. Must be called
			after each addition/deletion of members
		"""
		self.todo_list = []
		for e in self.todo_file.firstChild.childNodes:
			if e.nodeType == e.ELEMENT_NODE:
				self.todo_list.append(e)
		
	def save(self):
		"""
			Saves the todolist
			
			Saves the self.todo_file to a file
		"""
		f = open(self.todo_file_name, "w")
		f.write(self.todo_file.toprettyxml().replace("\t", "").replace("\n\n", "").encode("utf-8"))
		f.close()
	
	def create_new_file(self, file_name):
		"""
			Creates a new bare file containing nothing to do
		"""
		f = open(self.todo_file_name, "w")
		f.write("<?xml version=\"0.1\" encoding=\"UTF-8\" ?><todolist></todolist>")
		f.close()
	
	def remove_todo_by_id(self, i):
		"""
			Removes a node in the self.todo_file by its ID 
		"""
		for t in self.todo_list:
			if t.nodeType == t.ELEMENT_NODE:
				if int(t.attributes["id"].value) == int(i):
					self.todo_file.firstChild.removeChild(t)
					return
	
	def set_priority(self, i, p=""):
		"""
			Changes the priority of a todo
			
			NOT IMPLEMENTED YET, the priority still has no effect on
			nothing. Will be implemented soon.
		"""
		for e in self.todo_file.firstChild.childNodes:
			if e.nodeType == e.ELEMENT_NODE:
				if int(e.attributes["id"].value) == int(i):
					e.attributes["priority"] = p
					return
	
	def add_todo(self, content):
		"""
			Creates a new Todo containing the "content" content
		"""
		i = self.get_max_id()+1
		e = self.todo_file.createElement("todo")
		e.attributes["id"] = str(i)
		e.attributes["task"] = content.decode("utf-8")
		e.attributes["priority"] = ""
		
		print "Ajout du todo :"
		self.print_todo(e)
		
		self.todo_file.firstChild.appendChild(e)
	
	def print_todo(self, todo):
		"""
			Prints a todo with pretty colors <3
		"""
		print colored(" #%2d" % int(todo.attributes["id"].value), "blue"), ":", self.colorize_todo(todo.attributes["task"].value)
		
	def get_todo_by_id(self, i, todo_list=None):
		"""
			Returns the XML node corresponding to the todo with the id "i"
			within the given todo_list. If None, then the one used by
			the class shall be used. This is the case most of the time
		"""
		if todo_list == None:
			todo_list = self.todo_list
			
		for e in self.todo_file.firstChild.childNodes:
			if e.nodeType == e.ELEMENT_NODE:
				if int(e.attributes["id"].value) == int(i):
					return e
		
		return None
	
	def get_todos_by_tag(self, tag, marker="#"):
		"""
			Search all the todos which match the given tag
		"""
		if tag[0] != marker:
			tag = marker+tag
		
		l = []
		
		for e in self.todo_file.firstChild.childNodes:
			if e.nodeType == e.ELEMENT_NODE:
				text = e.attributes["task"].value.split(" ")
				for i in range(0, len(text)):
					if text[i][0] == marker:
						if text[i].lower() == tag.lower():
							l.append(e)
		
		return l
	
	def sort_todos_by_id(self, todo_list=None):
		"""
			Sorts the todo list by ID
		"""
		if todo_list == None:
			todo_list = self.todo_list
			
		return sorted(todo_list, key=lambda k: k.attributes["id"].value)
	
	def count_todos(self):
		"""
			Returns the number of todos currently registered
		"""
		return len(self.todo_list)
	
	def print_all(self):
		"""
			Print all the todos registered
		"""
		for todo in self.todo_list:
			self.print_todo(todo)
	
	def colorize_todo(self, text):
		"""
			Colorizes a todo, this means setting a pretty color on hashtags
		"""
		text = text.split(" ")
		for i in range(0, len(text)):
			if text[i][0] == '#':
				text[i] = colored(text[i], "green")
			elif text[i][0] == '+':
				text[i] = colored(text[i], "magenta")
			elif text[i][0] == '@':
				text[i] = colored(text[i], "yellow")
		return " ".join(text)
				
	
	def print_todos(self, todo_list=None):
		"""
			Prints all the todos within a list
		"""
		if todo_list == None:
			todo_list = self.todo_list
		
		for t in todo_list:
			self.print_todo(t)
	
	def get_max_id(self):
		"""
			Returns the maximum ID within the todo list
		"""
		m = 0
		for e in self.todo_list:
			if int(e.attributes["id"].value) > m:
				m = int(e.attributes["id"].value)
		return m
	
if __name__ == "__main__":
	fname = os.environ["HOME"] + "/.todo.xml"
	if len(sys.argv) == 1:
		print "Help for", sys.argv[0]
		print "\ttodo.py ls -- Display all the todos"
		print "\ttodo.py add <texte> -- Add a todo, the text may contain #hastags"
		print "\ttodo.py rm #number -- Removes a todo"
	elif len(sys.argv) == 2:
		if sys.argv[1] == "ls":
			t = TodoList(fname)
			print colored("> %d todo(s) en mémoire" % t.count_todos(), "white", attrs=["bold"])
			t.print_all()
	elif len(sys.argv) >= 3:
		t = TodoList(fname)
		if sys.argv[1] == "add":
			t.add_todo(" ".join(sys.argv[2:]))
			t.save()
		if sys.argv[1] == "rm":
			t.remove_todo_by_id(sys.argv[2])
			t.save()
		if sys.argv[1] == "sh":
			l = t.get_todos_by_tag(sys.argv[2])
			l = t.sort_todos_by_id(l)
			t.print_todos(l)
		if sys.argv[1] == "sc":
			l = t.get_todos_by_tag(sys.argv[2], "+")
			l = t.sort_todos_by_id(l)
			t.print_todos(l)
		if sys.argv[1] == "sp":
			l = t.get_todos_by_tag(sys.argv[2], "@")
			l = t.sort_todos_by_id(l)
			t.print_todos(l)
			
