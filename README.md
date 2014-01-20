# todo.py
## Developpement information

 * Curent version: 0.1 might be slightly buggy
 * License: WTF Public License v2
 * Author: Thomas Maurice <tmaurice59@gmail.com>

## What is this script for ?
This script is intended to provide a small commandline todo tool which
can help you to be better organized. Basicallly you can manage a small
todo list, add and remove todos, as well as searching and sorting them
by keywords, hashtags, contexts and so forth.

## How to use it
First, to have some help, just type ```./todo.py``` and some syntax information
should appear. So let get started !

### Adding a todo
This is done very simply by :

    todo.py add "your text, eventually with #hastags"

This will create a new todo. If you don't have any database file one will
be created.

### Listing & removing todos
You can list todos by typing ```todo ls```, you can also can remove them
typing ```todo rm [number]```. Where *number* is the todo id, as given
by the ls command.

### Searching
You have now 3 commands to search your todos, one to search for hashtags,
one for contexts and one for people. They have exactly the same syntax:

    todo.py command termtosearch
 
Where *command* is either **sh** (**s**earch **h**ashtag), **sc** for the context
and **sp** for the people. Note that you are not forced to specify the
prefixes #, + or @, the program will do it for you. :)

## A word on #hastags, +contexts and @people
Thos things are a way to organize your todos. When you create a new todo, you
can add "special" words into them, begining with # (just like in twitter),
+ to specify the context and @ to refer to a place or a person. These are
used when performing searches to improve its accuracy. Use it!
