import sublime
import sublime_plugin
import re
import random
import ast

def random_int(params):
	return str(random.randint(params['low'], params['high']))

def random_float(params):
	return params['format'].format(random.uniform(params['low'], params['high']))

def insert_into_view(edit, view, func, params):
	for region in view.sel():
		view.insert(edit, region.begin(), func(params))

class RandomIntCommand(sublime_plugin.TextCommand):
	def run(self, edit, **params):
		insert_into_view(edit, self.view, random_int, params)

class RandomFloatCommand(sublime_plugin.TextCommand):
	def run(self, edit, **params):
		insert_into_view(edit, self.view, random_float, params)

random_number_params = {
	'int': { 'low': 0, 'high': 10, },
	'float': { 'low': 0.0, 'high': 10.0, 'format': '{0:.2f}'}
}

def params_to_string(params):
	return ', '.join('{0} = {1}'.format(key, value) for key, value in params.items())

def string_to_params(params_text):
	params_text_split = params_text.split(',')
	params = {}
	for param_text in params_text_split:
		match = re.match(r"\s*(\S+)\s*=\s*(\S+)\s*", param_text)
		if match is None:
			raise RuntimeError('Invalid parameter format')
		params[match.group(1)] = match.group(2)
	return params

class RandomNumberWindowCommand(sublime_plugin.WindowCommand):
	def run_internal(self, type):
		self.type = type
		self.default_params = random_number_params[type]
		self.window.show_input_panel('Random {} parameters'.format(type), params_to_string(self.default_params), self.apply, None, None)

	def apply(self, params_text):
		try:
			params = string_to_params(params_text)
			for key, value_text in params.items():
				old_value = self.default_params.get(key)
				if old_value is None:
					raise RuntimeError('Unrecognized parameter "{}"'.format(key))
				old_value_type = type(old_value)
				value = old_value_type(value_text)
				print(type(value))
				if old_value != value:
					self.default_params[key] = value
			self.window.active_view().run_command('random_{}'.format(self.type), self.default_params)
		except RuntimeError as e:
			sublime.error_message(str(e))

class RandomIntWindowCommand(RandomNumberWindowCommand):
	def run(self):
		self.run_internal('int')

class RandomFloatWindowCommand(RandomNumberWindowCommand):
	def run(self):
		self.run_internal('float')