import os, sys
import fileinput


# ------------------------------------------------
# Batch text editor 
# ------------------------------------------------

#set path to the directory containing the ui files.
path = os.path.join(os.path.dirname(__file__), 'tk_ui') #get absolute path from dir of this module + relative path to directory

#create a list of the names of the files in the ui folder, removing the extension.
def uiList():
	return [file_.replace('.ui','') for file_ in os.listdir(path) if file_.endswith('.ui')] #gets uiList from directory contents




def editText(app, name):
	path = os.path.join(os.path.dirname(__file__), app+'\\tk_slots_'+app) #get absolute path from dir of this module + relative path to directory
	file = path+'\\'+'tk_slots_'+app+'_'+name+'.py'

	for lineNum, line in enumerate(fileinput.input(file, inplace=1)):
		if 'def b0' in line or 'def t0' in line or 'def chk0' in line or 'def cmb0' in line or 'def v0' in line or 'def i0' in line and '#' in line:
			if len(line.split('#')) >1:
				methodString = line.split('#')[0].strip()
				commentString = line.split('#')[1].title()
				tab = '	'
				# Whatever is written to stdout or with print replaces the current line
				print (tab+methodString+'\n		\'\'\'\n'+tab+tab+commentString+'\n		\'\'\'')
			else:
				sys.stdout.write(line)
		else:
			sys.stdout.write(line) #write line contents back to line without changes




for app in ['maya', 'max']:
	for name in uiList():
	# for name in ['display']:
		try:
			# editText('maya', name)
			editText(app, name)
			print app, name
		except Exception as error:
			print app, name, error