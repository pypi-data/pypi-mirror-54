import json
from re import compile as make_regex, finditer, MULTILINE
import random, click, json, os, re, sys, subprocess
from platform import system as gimme_system
from shutil import copy as copyfile
from transpiler2 import *
import PySimpleGUI as sg

main_boilerplate = '''import PySimpleGUI as sg

layout = [[]]
window = sg.Window('App', layout)

while True:
	event, values = window.read()
	if event in (None, 'Exit'):
		break

	if event == '':
		pass

# ~TARGET

window.close()
'''

cd = os.path.dirname(os.path.abspath(__file__))

def build_boilerplate(layout='[[]]', mouse_clicks=False, keys=False):
	# create a str with PSG code

	def do_callbacks(keys):
		return '\n'.join([f"\tif event == '{i}':\n\t\tpass" for i in keys])

	def do_mice_events(ui, boilerplate):
		# find regex pattern from all buttons
		regex_pattern = make_regex(
			r'(RButton|ReadButton|B)\([\'\"][\w\ \_\d]*[\'\"],?\s?((key)\s*=\s*[\'\"]([\w\ \_\d]+?)[\'\"])')
		# find all keys in you ui
		keys = [i.group(4) for i in finditer(regex_pattern, ui)]
		return boilerplate.replace('# ~TARGET', do_callbacks(keys))

	def do_keys_events(ui, boilerplate):
		# find regex pattern from all elements
		regex_pattern = make_regex(r'(key)\s*=\s*[\'\"]([\w\d]+?)[\'\"]')
		# find all keys in you ui
		keys = [i.group(2) for i in finditer(regex_pattern, ui)]
		return boilerplate.replace('# ~TARGET', do_callbacks(keys))

	if not mouse_clicks and not keys:
		text = main_boilerplate
	elif mouse_clicks:
		text = do_mice_events(layout, main_boilerplate)
	elif keys:
		text = do_keys_events(layout, main_boilerplate)

	return text.replace('[[]]', layout)


def just_compile(values):
	#
	# compile "XML_file + object_name" to "PSG ui"
	#
	OBJ_NAME, inputXMLui, NO_BAD_WIDGETS = values['objname'], values['xmlfile'], values['no_bad_widgets']
	# make absolute path, if just filename given
	if '/' not in inputXMLui and '\\' not in inputXMLui:
		inputXMLui = os.path.join(cd, inputXMLui)

	# validation
	inputXMLui = inputXMLui if inputXMLui[:2] != '~/' else os.path.join(
		os.environ['HOME'], inputXMLui[2:])

	python = 'python'
	if gimme_system() == 'Linux':
		python += '3'

	# idea is simple:
	# 1 copy input ui file to .
	# 2 run "psg_ui_maker.py" -> it will compile inputXMLui, and give output in RESULTPSG file
	# 3 rm   input ui file from .
	# 4 read output of rm   input ui file from .

	# 1
	ui_file = os.path.join(cd, 'tmp_untitled.ui')
	copyfile(inputXMLui, ui_file)
	# 2
	psg_ui_maker__py = os.path.join(cd, 'psg_ui_maker.py')
	NO_BAD_WIDGETS = '1' if NO_BAD_WIDGETS else '0'
	command = '{0} "{1}" {2} {3}'.format(
		python, psg_ui_maker__py, OBJ_NAME, NO_BAD_WIDGETS)
	subprocess.run(command, shell=True, stdout=subprocess.DEVNULL,
				   stderr=subprocess.DEVNULL)
	# 3
	# rm given file
	os.remove(ui_file)
	# 4
	# return psg code
	RESULTPSG = os.path.join(cd, 'result_psg.layout')
	if not os.path.exists(RESULTPSG):
		raise Exception(f'error, no obj_name="{OBJ_NAME}" found')
	content = readfile(RESULTPSG)
	os.remove(RESULTPSG)
	return content

def readfile(filename):
	with open(filename, 'r', encoding='utf-8') as ff:
		return ff.read()


def run_gui():
	settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setting.json')

	def clear_empty_top_widget(ui):
		'''
		clear ui to easyily for coping functionality (ctrl+c)
		'''

		'''
		# case1
		sg.Frame('', key='gridLayout', layout = [
					[sg.RButton('PushButton', key='pushButton'), sg.RButton('PushButton', key='pushButton_2')]
		])
		'''
		first_line = ui.split('\n')[0]
		regex_matched = make_regex(
			r"^sg.Frame\('',\s?key='.*',\slayout\s=\s\[").match(first_line)
		if regex_matched and ui[-2:] == '])':
			new_ui = '[\n' + '\n'.join(ui.split('\n')[1:]).strip()
			return new_ui[:-1]
		return ui


	def update_clear_btn(my_window, my_values, real_value=''):
		objname = my_values['objname'] if real_value == '' else real_value
		all_object_names_in_combo = my_window['objs'].Values

		if my_values['xmlfile'] and objname and objname in all_object_names_in_combo:
			my_window['compile_btn'].Update(disabled=False)
			my_window['compilepp_btn'].Update(disabled=False)
		else:
			my_window['compile_btn'].Update(disabled=True)
			my_window['compilepp_btn'].Update(disabled=True)

	def update_app_settings():
		with open(settings_path, 'w', encoding='utf-8') as f:
			json.dump(_settings, f, ensure_ascii=False, indent=2)

	if os.path.exists(settings_path):
		try:
			with open(settings_path, 'r', encoding='utf-8') as f:
				_settings = json.load(f)
		except Exception as e:
			_settings = {
				'-memento-file-cb-' : False,
				'xmlfile' : ''
			}
			update_app_settings()
	else:
		_settings = {
			'-memento-file-cb-' : False,
			'xmlfile' : ''
		}
		update_app_settings()

	#              _
	#             (_)
	#   __ _ _   _ _
	#  / _` | | | | |
	# | (_| | |_| | |
	#  \__, |\__,_|_|
	#   __/ |
	#  |___/
	ralign = {'size': (16, 3), "justification": 'r'}
	pad = {'pad':(1,1)}
	input_frame = [
		[sg.T('\nxml file', **ralign)
		 ,sg.I(key='xmlfile', size=(35,2), **pad, change_submits=True)
		 ,sg.FileBrowse(target='xmlfile')
		 ,sg.T('possible\nobject names', justification='r')
		 ,sg.Drop(values=[''], key='objs', size=(30, 1), change_submits=True)],

		[sg.T('\nTarget object name', **ralign)
		 ,sg.I(key='objname', change_submits=True)
		 ,sg.B('compile', key='compile_btn', **pad, disabled=True)
		 ,sg.B('compile++', key='compilepp_btn', **pad, disabled=True)
		 ,sg.Radio('all keys', 1, True, key='r2_keys', **pad)
		 ,sg.Radio('mouse clicks', 1, key='r2_mouse_clicks', **pad)]
	]

	tab1_layout = [
		[sg.Frame('Input data', input_frame, **pad,)],
		[sg.B('Clear')
		 ,sg.CB('pass bad widgets', True, key='no_bad_widgets',**pad,)
		 ,sg.CB('empty top widget', True, key='empty_top_widget',**pad,)
		 ,sg.B('Execute code below (if generated with compile++ button)', **pad, disabled=True,
		 		 size=(25, 2), key='Try')],
		[sg.ML(key='psg_ui_output', size=(120, 8))]
	]
	tab3_layout = [
		[sg.CB('Remember path to previous file', False, change_submits=True, key='-memento-file-cb-')
		],
	]
	tab2_layout = [[sg.Image(filename='', key='psg_image')]]

	layout = [[ sg.TabGroup([[
		sg.Tab('transpiler', tab1_layout, **pad,),
		sg.Tab('settings', tab3_layout),
		sg.Tab('hot transpiler', tab2_layout, disabled=True)]]) ]
	]

	window = sg.Window('Transpiler', layout, auto_size_buttons=False,
								   default_button_element_size=(10, 1),
								   finalize=True)
	
	# setup
	if _settings['-memento-file-cb-']:
		window['-memento-file-cb-'].Update(True)
		window['xmlfile'].Update(_settings['xmlfile'])

	prev_values = None

	# loop
	first_time_running = True
	while True:
		if first_time_running:
			event, values = window.read(timeout=0)
			event = 'xmlfile'
			first_time_running = False
		else:
			event, values = window.read()

		if event in (None, 'Exit'):
			break

		prev_values = values
		if event == '-memento-file-cb-':
			print(values)
			_settings['-memento-file-cb-'] = values['-memento-file-cb-']
			_settings['xmlfile'] = '' if values['-memento-file-cb-'] else values['xmlfile']
			update_app_settings()

		elif event == 'xmlfile':
			myxml_file = values['xmlfile'].strip()
			# remember this file
			if _settings['-memento-file-cb-']:
				_settings['xmlfile'] = myxml_file
				update_app_settings()
			if os.path.exists(myxml_file) and os.path.isfile(myxml_file):

				# get xml
				with open(myxml_file, 'r', encoding='utf-8') as ff:
					xml_code = ff.read()

				# filter object names
				widgets_regexpattern = make_regex(
					r"^[ \s]{1,}<(widget)\s?.*?\s?name=\"(.+)\"\/?>", MULTILINE)
				layouts_regexpattern = make_regex(
					r"^[ \s]{1,}<(layout)\s?.*?\s?name=\"(.+)\"\/?>", MULTILINE)
				widgets = [i.group(2) for i in finditer(
					widgets_regexpattern, xml_code)]
				layouts = [i.group(2) for i in finditer(
					layouts_regexpattern, xml_code)]

				combo_items = ['# LAYOUTS widgets #', *layouts, '# WIDGETS widgets #', *widgets]

				# set it
				window['objs'].Update(values=combo_items)
				update_clear_btn(window, values)

				el = combo_items[1]
				if ' ' not in el:
					window['objname'].Update(el)
					update_clear_btn(window, values, real_value=el)
			else:
				window['objs'].Update(values=[])
				window['objname'].Update('')

		elif event == 'objs':
			# add only REAL object names -> those, who not contain ' '
			if ' ' not in values['objs']:
				window['objname'].Update(values['objs'])
			update_clear_btn(window, values, real_value=values['objs'])
		elif event == 'objname':
			update_clear_btn(window, values)
		elif event == 'Clear':
			window['psg_ui_output'].Update('')
		elif event == 'compile_btn':
			ui = just_compile(values)

			if values['empty_top_widget']:
				ui = clear_empty_top_widget(ui)

			window['psg_ui_output'].Update(ui)
		elif event == 'compilepp_btn':
			ui = just_compile(values)

			# case for 'speed up'
			# psg_ui_output = values['psg_ui_output']
			# ui = ... psg_ui_output ...

			ui = just_compile(values)

			if values['empty_top_widget']:
				ui = clear_empty_top_widget(ui)

			psg_ui = build_boilerplate(layout=ui,
									   mouse_clicks=values['r2_mouse_clicks'],
									   keys=values['r2_keys'])
			window['psg_ui_output'].Update(psg_ui)

		elif event == 'Try':
			try:
				psg_ui = values['psg_ui_output'].strip()
				psg_ui_lines = psg_ui.split('\n')

				'''
				case 1:
					import PySimpleGUI as sg
					...
				case 2:
					sg.Frame('', layout = [
						[...],
						[...],
						[...],
					])
				case 3:
					[
						[...],
						[...],
						[...],
					]
				'''
				if psg_ui.startswith('import PySimpleGUI as sg'):
					exec(psg_ui)
				if psg_ui_lines[0].startswith("""sg.Frame('""") and psg_ui_lines[0].endswith("""', layout = ["""):
					window2 = sg.Window('test', eval(psg_ui))
					window2.read()
					window2.close()
				if psg_ui_lines[0].startswith("""[""") and psg_ui_lines[-1].endswith("""]"""):
					possible_ui = eval(psg_ui)
					possible_ui
					if type(possible_ui) is list and type(possible_ui[0]) is not list:
						raise Exception(f"bad ui given. It's not a list of LISTS.")
					window2 = sg.Window('test', possible_ui)
					window2.read()
					window2.close()


			except Exception as e:
				sg.popup(str(e))

	window.close()


@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True, help='Verbose mode')
@click.option('-x', '--run', default=True, is_flag=True, help='just run gui example')
@click.option('-xmlfile', type=click.Path(exists=True), help='abs or rel path to ui_file')
@click.option('-tc', '--tabchar', type=str, default='\t', help='tab character. Default is "\\t"')
@click.option('-ta', '--tabchar_amount', type=int, default=1, help='indent tab amount')
@click.option('-objname', type=str, help='object name of target container')
@click.option('-nobadwidgets', default=True, is_flag=True, help='forget about bad widgets. Default - True')
@click.option('-o', '--outputfile', type=click.Path(), help='file to output compiled PySimpleGUI ui')
@click.option('-pp_mouse', default=False, is_flag=True, help='compile++ option - do the mouse clicks events')
@click.option('-pp_keys',  default=False, is_flag=True, help='compile++ option - do the keys events')
def cli(xmlfile, objname, nobadwidgets, outputfile, pp_mouse, pp_keys, tabchar, tabchar_amount, verbose, run):

	if run and not (xmlfile and objname):
		run_gui()
	elif xmlfile and objname:

		try:
			# PRE-process
			##=#=#=#=#=#=#
			# RELATIVE path: add PWD to current file path
			if not (xmlfile.startswith('/') or xmlfile[1] == ':'):
				xmlfile = os.path.join(cd, xmlfile)
				if verbose: print(f'input = "{xmlfile}"')

			psg_ui = just_compile({'objname': objname,
								   'xmlfile': xmlfile, 'no_bad_widgets': nobadwidgets})

			# compile++
			if pp_mouse:
				psg_ui = build_boilerplate(layout=psg_ui, mouse_clicks=True)
			elif pp_keys:
				psg_ui = build_boilerplate(layout=psg_ui, keys=True)


			# POST-PROCESS
			##=#=#=#=#=#=#
			if tabchar != '\t':
				# 1 way - replace
				# psg_ui = psg_ui.replace('\t', tabchar*tabchar_amount)

				# 2 way - regex
				def replace_tab__for_spaces(input_string, my_tab_char = "*"):

					regex_pattern = re.compile(r'^([ ]{4})+', flags=re.MULTILINE)

					result = []
					for i in input_string.split('\n'):
						if regex_pattern.match(i):
							spaces = list(re.finditer(regex_pattern, i))[0].group(0)
							tab_times = int(len(spaces) / 4)
							line = re.sub(regex_pattern, my_tab_char*tab_times, i)
							result.append(line)
						else:
							result.append(i)

					return '\n'.join(result)
				def replace_tab_for_tabs(input_string, my_tab_char = "*"):

					regex_pattern = re.compile(r'^(\t)+', flags=re.MULTILINE)

					result = []
					for i in input_string.split('\n'):
						if regex_pattern.match(i):
							spaces = list(re.finditer(regex_pattern, i))[0].group(0)
							tab_times = len(spaces)
							line = re.sub(regex_pattern, my_tab_char*tab_times, i)
							result.append(line)
						else:
							result.append(i)

					return '\n'.join(result)

				tabb = tabchar*tabchar_amount
				psg_ui = replace_tab_for_tabs(psg_ui, my_tab_char=tabb)

			if outputfile: # write PSG_UI to file
				with open(outputfile, 'w', encoding='utf-8') as ff:
					ff.write(psg_ui)
			else: # output to console
				click.echo(psg_ui)

			if verbose:
				click.echo(click.style("\n~~~done", bg='black', fg='green'))

		except Exception as e:
			click.echo(click.style(str(e), bg='black', fg='red'))



if __name__ == '__main__':
	cli()
