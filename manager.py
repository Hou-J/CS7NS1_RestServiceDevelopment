from flask import Flask
from flask_restful import reqparse, Api, Resource
import requests, json
from time import time, sleep
from getpass import getpass

app = Flask(__name__)
api = Api(app)


class getRepo(Resource):
    def __init__(self):
        global m
        self.manger = m
        super(getRepo, self).__init__()
        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('pullStatus', type=int, location='json')
        self.reqparser.add_argument('complexity', type=float, location='json')

    def get(self):
        args = self.reqparser.parse_args()
        if args['pullStatus'] == False:
            print("GOT 1")
            return {'repo': "https://github.com/{}/{}".format(self.manger.owner, self.manger.repo)}
        if args['pullStatus'] == True:
            self.manger.workerNumNow += 1
            if self.manger.workerNumNow == self.manger.numWorkers:
                self.manger.startTime = time()
            print("WORKER NUMBER: {}".format(self.manger.workerNumNow))

    def post(self):
        pass


class cycCalculator(Resource):
    def __init__(self):
        global m
        self.manger = m
        super(cycCalculator, self).__init__()
        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('commit', type=str, location='json')  # Repeat for multiple variables
        self.reqparser.add_argument('complexity', type=str, location='json')

    def get(self):
        if self.manger.workerNumNow < self.manger.numWorkers:
            sleep(0.1)
            return {'sha': -2}
        if len(self.manger.commits) == 0:
            return {'sha': -1}
        commitSha = self.manger.commits[0]
        del self.manger.commits[0]
        print(commitSha)
        return {'sha': commitSha}

    def post(self):
        print(self.reqparser.parse_args())
        args = self.reqparser.parse_args()
        self.manger.commitsComplexity.append({'sha': args['commit'], 'complexity': args['complexity']})
        if len(self.manger.commitsComplexity) == self.manger.commitsNum:
            endTime = time() - self.manger.startTime
            totalComplexity = 0
            for x in self.manger.commitsComplexity:
                xcomp = float(x['complexity'])
                if xcomp > 0:
                    totalComplexity += xcomp
                else:
                    print("Commit {} has no computable files".format(x['sha']))
            averageComplexity = totalComplexity / len(self.manger.commitsComplexity)
            print("\n\nAverage cyclomatic complexity for the repository ({}/{}) is: {}".format(self.manger.owner,
                                                                                               self.manger.repo,
                                                                                               averageComplexity))
            print("{} workers finished work in {} seconds\n\n".format(self.manger.numWorkers, endTime))
        return {'success': True}


api.add_resource(cycCalculator, '/cyc', endpoint="cyc")
api.add_resource(getRepo, "/repo", endpoint="repo")


class manager():
    def __init__(self):
        self.numWorkers = int(input("How many workers do you want:"))
        self.workerNumNow = 0
        self.startTime = 0.0
        authgithubid = input(
            "Input your github id and password to increse the github api limit.\n\nInput your github username:")
        authgithubpwd = getpass("Input your github password:")

        self.owner = input(
            "Press enter to use default repository: python/core-worlflow\n\nOr input the repository owner:")
        if len(self.owner) != 0:
            self.repo = input("Input the repository name:")
        else:
            self.owner = "python"

            self.repo = "core-workflow"  # input("Input the repository name:")

        self.data = []
        page = 1
        self.commits = []

        endFlag = False
        while not endFlag:
            r = requests.get(
                "https://api.github.com/repos/{}/{}/commits?page={}&per_page=100".format(self.owner, self.repo, page),
                auth=(authgithubid, authgithubpwd))
            self.data += json.loads(r.text)
            if len(self.data) < page * 100:
                endFlag = True
            page += 1

        self.commitsNum = 0
        for d in self.data:
            self.commits.append(d['sha'])
            print(d['sha'])
            self.commitsNum += 1
        print("\n\nTotal number commit for the given repository: " + str(self.commitsNum))
        self.commitsComplexity = []
        self.commitNum = 0


if __name__ == '__main__':
    m = manager()
    app.run(port=5000)
