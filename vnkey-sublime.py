from .bogo.core import process_sequence
from pprint import pprint
import sublime
import sublime_plugin

ENABLEKEY = False

class SaveOnModifiedListener(sublime_plugin.EventListener):
  def on_modified_async(self, view):
    view.run_command('start_vn_key')

class StartVnKeyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# if vn keyboard is not enable
		if not ENABLEKEY:
			return False
		else:
			# pprint(vars(edit))
			curr_pos = self.view.sel()[0]
			word_region = self.view.word(curr_pos)
			word = self.view.substr(word_region)
			# print(curr_pos,word_region,word)
			final = self.key_send(word)
			if not final: return False
			# self.view.run_command("runchange", {"string":final})
			self.view.replace(edit, word_region,final)
			self.view.end_edit(edit)
			return True
	def key_send(self,word):
		if ENABLEKEY:
			word_after = process_sequence(word)
			if word_after == 'gía':
				word_after = "giá"
			if word_after == 'Gía':
				word_after = "Giá"	
		else:
			word_after = word
			# add fix 
	
		if word_after != word:
				return word_after
		return False

class ToggleVnCommentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global ENABLEKEY
		if ENABLEKEY:
			ENABLEKEY = False
			self.view.run_command("toggle_comment")
			ENABLEKEY =True
		else:
			self.view.run_command("toggle_comment")

class ControlVnKeyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global ENABLEKEY
		if ENABLEKEY:
			ENABLEKEY = False
			self.view.set_status('VnKey'," VNKEY: OFF")
		else:
			ENABLEKEY = True
			self.view.set_status('VnKey'," VNKEY: ON")