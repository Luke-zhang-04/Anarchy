git-%:
	git commit -a -m"$(@:git-%=%)"
	git push -u origin master

git add-%:
	git add .
	git commit -a -m"$(@:add-%=%)"
	git push -u origin master

pyinstaller add-%:
	pyinstaller --add-data '$(@:add-%=%):.' --onefile main.py

pyinstaller init:
	pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' --hidden-import tkinter main.py