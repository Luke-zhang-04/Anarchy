git-%: 
	git commit -a -m "$(@:git-%=%)"
	git push -u origin master

git add all-%: 
	git add .
	git commit -a -m "$(@:git-%=%)"
	git push -u origin master