






	def editText(app, name): #
		#'class':{connectionDict':{'methodString':{'methodName':'commentString'}} ie. 'polygons':{connectionDict':{'b000':{'methodName':'Multi_Cut Tool'}},
		path = os.path.join(os.path.dirname(__file__), app+'/tk_slots_'+self.hotBox.app) #get absolute path from dir of this module + relative path to directory
		file = path+'/'+'tk_slots_'+app+'_'+name+'.py'

		with open(file) as f:
			for line in f.readlines():
				if 'def b' in line and '#' in line:
					methodString = line.split('#')[0].strip().lstrip('def ').rstrip('(self):')
					commentString = line.split('#')[1]
					try:
						self.hotBox.sb.setMethodName(self.hotBox.name, methodString, commentString)
					except Exception as error:
						if error==KeyError:
							print "#Exception: ", error