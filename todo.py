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
		self.todo_list = []
		for e in self.todo_file.firstChild.childNodes:
			if e.nodeType == e.ELEMENT_NODE:
				self.todo_list.append(e)
		
	def save(self):
		f = open(self.todo_file_name, "w")
		f.write(self.todo_file.toprettyxml().replace("\t", "").replace("\n\n", "").encode("utf-8"))
		f.close()
	
	def create_new_file(self, file_name):
		f = open(self.todo_file_name, "w")
		f.write("<?xml version=\"0.1\" encoding=\"UTF-8\" ?><todolist></todolist>")
		f.close()
	
	def remove_todo_by_id(self, i):
		for t in self.todo_list:
			if t.nodeType == t.ELEMENT_NODE:
				if int(t.attributes["id"].value) == int(i):
					self.todo_file.firstChild.removeChild(t)
					return
	
	def set_priority(self, i, p=""):
		for e in self.todo_file.firstChild.childNodes:
			if e.nodeType == e.ELEMENT_NODE:
				if int(e.attributes["id"].value) == int(i):
					e.attributes["priority"] = p
					return
	
	def add_todo(self, content):
		i = self.get_max_id()+1
		e = self.todo_file.createElement("todo")
		e.attributes["id"] = str(i)
		e.attributes["task"] = content.decode("utf-8")
		e.attributes["priority"] = ""
		
		print "Ajout du todo :"
		self.print_todo(e)
		
		self.todo_file.firstChild.appendChild(e)
	
	def print_todo(self, todo):
		print colored(" #%2d" % int(todo.attributes["id"].value), "blue"), ":", self.colorize_todo(todo.attributes["task"].value)
		
	def get_todo_by_id(self, i, todo_list=None):
		if todo_list == None:
			todo_list = self.todo_list
			
		for t in todo_list:
			if int(t.attributes["id"].value) == int(i):
				return t
		
		return None
	
	def get_todos_by_tag(self, tag, todo_list=None):
		if todo_list == None:
			todo_list = self.todo_list
	
	def sort_todos_by_id(self, todo_list=None):
		if todo_list == None:
			todo_list = self.todo_list
			
		return sorted(todo_list, key=lambda k: k.attributes["id"].value)
	
	def count_todos(self):
		return len(self.todo_list)
	
	def print_all(self):
		for todo in self.todo_list:
			self.print_todo(todo)
	
	def colorize_todo(self, text):
		text = text.split(" ")
		for i in range(0, len(text)):
			if text[i][0] == '#':
				text[i] = colored(text[i], "green")
		return " ".join(text)
				
	
	def print_todos(self, todo_list=None):
		if todo_list == None:
			todo_list = self.todo_list
		
		for t in todo_list:
			self.print_todo(t)
	
	def get_max_id(self):
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
			
