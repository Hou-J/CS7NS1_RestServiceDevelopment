	Jiongxu Hou 17304249 for CS7NS1 Scalable Computing

#Rest Service Development Task
The task is focussed on the efficient computation of code complexity for a given GitHub repository, utilising a set of nodes as appropriate to minimise execution time from submission to result return.

The manager is to distribue the tasks to mutiple workers one at a time, after the worker finished the given task, it will ask for a new task till all tasks is done.

The *plot.pdf* shows the results of the time needed in calculating different GitHub repositories as well as the relations of worker number and the time used in the calculation.

##Dependencies
Install all independence: *pip install -r requirements.txt* 

or:

###radon: 
To calculate cyclomatic complexitycan, installed: *pip install radon*
	
###flask:
To implement the restfull api, install: *pip install flask*
	
###flask_restful:
To implement the restfull api, install: *pip install flask_restful*
	
###requests:
To get requests, install: *pip install requests*

##manager.py:
The ip and port is hardcode and set as default: http://127.0.0.1:5000

start with: *python manger.py [$numberOfWorkers, $repositoryUser, $repositoryName]*
		
		
##worker.py:

The ip and port is hardcode and set as default: http://127.0.0.1:5000
	
Start with: *python worker.py*
	
Need start exact number of workers ($numberOfWorkers) as the manager required
	
	
#Note: 

After I almost done with my work and started testing my code, I tried to delete the repository I pulled from the python/core-workflow (the one I want to calculate) as I want to see what will happen if I start from a empty folder. So I delete the pulledRepo folder (the folder I stored the pulled files).
	
Then I run my worker code again without making a new folder "pulledRepo" and the code in *worker.py* "rm .git/" deleted my *.git* folder, so all my git commit and log are gone (used to have more than 15 commits I think), and then the git logs which I pulled from python/core-workflow are here in my logs.
