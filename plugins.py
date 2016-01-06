import glob
import os
from logs import logs as log
import json
import imp
logs=log()
def load():
	logs.write("In plugin loader",'working')
	plugins=[]
	if os.path.isdir("plugins"):
		plugin=[x[0] for x in os.walk('plugins')][1]
		logs.write("Loading plugin {0}".format(plugin.split("plugins/")[1]),'trying')
		logs.write("plugin.json file path should be {0}/plugin.json".format(plugin),'working')
		if os.path.isfile('{0}/plugin.json'.format(plugin)):
			pluginfo=json.loads(open('{0}/plugin.json'.format(plugin)).read())
			plugins.append({plugin.split("plugins/")[1]:pluginfo})
			logs.write("Loaded plugin {0}".format(plugin.split("plugins/")[1]),'success')
		else:
			logs.write("plugin.json file not found for plugin {0}".format(plugin.split("plugins/")[1]),'error')
		return plugins
	else:
		logs.write("Plugin directory not found", 'error')
		return False
def execute(plugin, command):
	def checkdicts(checkvar):
		logs.write("Looking for {0} dictionary".format(checkvar), 'trying')
		for plugdict in plugin.values()[0]:
			logs.write("Checking dictionary {0}".format(plugdict),'trying')
			if plugdict.keys()[0]==checkvar:
				logs.write("Found dictionary {0}".format(checkvar), 'success')
				checkval=plugdict.values()[0]
				break
		return checkval
	logs.write("Executing plugin {0}".format(plugin),'working')
	plugtype=checkdicts('type')
	logs.write("Plugin type is {0}".format(plugtype), 'working')
	if plugtype=="python":
		logs.write("Checking to get the name of the python file", 'trying')
		pyfile=checkdicts('file')
		logs.write("Trying to import python file {0}".format(pyfile), 'trying')
		pyimport="plugins/{0}/{1}".format(plugin.keys()[0],pyfile)
		logs.write("Import path is {0}".format(pyimport), 'workng')
		imvar = imp.load_source('plugfile', pyimport)
		logs.write("Imported python plugin", 'success')
		plugfunction = checkdicts('function')
		required=checkdicts('require')
		needed=[]
		finalargs=[]
		for item in required:
			needed.append(item)
		if required==["command"]:
			finalargs.append(command)
		else:
			#TODO: here fetch required arguments
			return "Done"
		finalargs=tuple(finalargs)
		result = getattr(imvar, plugfunction)(finalargs)
		return result
