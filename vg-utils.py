import sublime
import sublime_plugin
import re
import random
import ast
import string

def get_random_int(low, high):
	return str(random.randint(low, high))

def get_random_float(low, high, fmt):
	return fmt.format(random.uniform(low, high))

def get_random_string(choice_set, length):
	return ''.join(random.choice(choice_set) for _ in range(length))

def insert_into_view(edit, view, type, params):
	expression = 'get_random_{}({})'.format(type, params['params'])
	for region in view.sel():
		view.insert(edit, region.begin(), eval(expression))

class RandomIntCommand(sublime_plugin.TextCommand):
	def run(self, edit, **params):
		insert_into_view(edit, self.view, 'int', params)

class RandomFloatCommand(sublime_plugin.TextCommand):
	def run(self, edit, **params):
		insert_into_view(edit, self.view, 'float', params)

class RandomStringCommand(sublime_plugin.TextCommand):
	def run(self, edit, **params):
		insert_into_view(edit, self.view, 'string', params)

default_params = {
	'int': 'low = 0, high = 10',
	'float': 'low = 0.0, high = 10.0, fmt = \'{0:.2f}\'',
	'string': 'length = 8, choice_set = string.ascii_lowercase'
}

class RandomWindowDispatch:
	def __init__(self, type):
		self.type = type
		self.current_params = default_params[type]

	def run(self, window):
		self.window = window
		self.window.show_input_panel('Random {} parameters'.format(type), self.current_params, self.apply, None, None)

	def apply(self, params):
		self.current_params = params
		self.window.active_view().run_command('random_{}'.format(self.type), {'params' : self.current_params})

class RandomIntWindowCommand(sublime_plugin.WindowCommand):
	dispatch = RandomWindowDispatch('int')
	def run(self):
		self.dispatch.run(self.window)

class RandomFloatWindowCommand(sublime_plugin.WindowCommand):
	dispatch = RandomWindowDispatch('float')
	def run(self):
		self.dispatch.run(self.window)

class RandomStringWindowCommand(sublime_plugin.WindowCommand):
	dispatch = RandomWindowDispatch('string')
	def run(self):
		self.dispatch.run(self.window)