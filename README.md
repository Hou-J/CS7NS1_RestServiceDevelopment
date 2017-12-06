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
	
