git-%:
	git commit -a -m"$(@:git-%=%)"
	git push -u origin master

git add-%:
	git add .
	git commit -a -m"$(@:git-%=%)"
	git push -u origin master