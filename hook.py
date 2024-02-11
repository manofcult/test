__VERSION__ = '2.0'
__REV__ = filter(str.isdigit, '$Revision: 635 $')
__IMM__ = '1.8'
__DEBUGGERAPP__ = ''
arch = 32
win7mode = False

# try:
# 	import debugger
# except:
# 	pass
try:
	import immlib as dbglib
	from immlib import LogBpHook
	__DEBUGGERAPP__ = "Immunity Debugger"
except:		
	try:
		import pykd
		import windbglib as dbglib
		from windbglib import LogBpHook
		dbglib.checkVersion()
		arch = dbglib.getArchitecture()
		__DEBUGGERAPP__ = "WinDBG"
	except SystemExit:
		print("-Exit.")
		import sys
		sys.exit(1)
	except Exception:
		#import traceback
		print("Do not run this script outside of a debugger !")
		#print traceback.format_exc()
		import sys
		sys.exit(1)
