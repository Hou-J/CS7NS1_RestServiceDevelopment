note: 

	After I almost done my work and testing my code, I tried to delete the repository I pulled from the python/core-workflow (the 
one I want to calculate), I need to see what will happen if I start from a empty folder. So I delete the pulledRepo folder (the folder I 
stored the pulled files).
	
    Then I run my worker code again without making a new folder "pulledRepo", (which obivously I shouldn't), and the code in worker.py 
"rm my .git" deleted my .git folder, so all my git commit and log are gone (used to have more than 15 commits I think), and then the git 
logs which I pulled from python/core-workflow are here in my logs.
	
    I'm new to git and github, and I even find this issue last saturday (Dec 9), I tried to fix this in serverl ways, but failed. I even 
tried some file recovery applications, still, I cannot find the file that I accidently deleted. So I do not have my logs here in my 
repositorys.
	
    I'm so sorry that this happened, this obivious taught me a lesson and I will be more careful with my logs, .git folder and codes, 
but currently I really can not do anything to save the situation, and I do not have the time to redo my work from scrach, so all I can 
do is add more comment to the code (later this week), to show that I really do know my code. I would appreciate if you can take this 
into account when grading. Thank you.



rest task
	Jiongxu Hou 17304249 for CS7NS1 Scalable Computing

dependencies
	radon: 
		used to calculate cyclomatic complexity
		can be installed through	pip install radon
	Flask:
		used to implement the restfull api
		can be installed through	pip install flask
	requests:
		used to get requests
		can be installed through	pip install requests

manager:
	the ip and port is hardcode and set as default: http://127.0.0.1:5000
	start with:	python manger.py
	required input:
		number of workers
		github username
		github password(used package getpass)
		the repository belonged user
		the repository name
		
worker:
	the ip and port is hardcode and set as default: http://127.0.0.1:5000
	start with:	python worker.py
	no required input
	need open exact number of workers as the manager required
	
