from flask import Flask
from flask_restful import reqparse, Api, Resource
import requests, json
from time import time

app = Flask(__name__)
api = Api(app)


class cycCalculator(Resource):
    # get method can return the sha code to the worker
    # when the worker request a commit, it use get function
    # then the server return the top sha in the list it get from github
    # after the commit sha was given to the worker,
    # it will be deleted from the list.
    def get(self):
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('commit', type=str, location='json')
        reqparser.add_argument('complexity', type=str, location='json')

        # check if the worker is enough
        if workerNumNow < numWorkers:
            return False
        # check if the whole work is done
        if len(commits) == 0:
            return True
        # give the first commit to the worker and then delete it
        commitSha = commits[0]
        del commits[0]
        print(commitSha)
        return commitSha

    def post(self):
        # 'pull' is used to give the github url to worker to pull the repository
        # 'commit' is the hash code of that commit
        # 'complexity' is the average cyclomatic complexity
        reqparser = reqparse.RequestParser()
        reqparser.add_argument('pull', type=bool, location='json')
        reqparser.add_argument('commit', type=str, location='json')
        reqparser.add_argument('complexity', type=str, location='json')
        args = reqparser.parse_args()
        # if not get the url, then return the url
        if args['pull'] == False:
            return "https://github.com/{}/{}".format(owner, repo)

        # if pulled the depository, and the workers number is enough, then start count time
        if args['pull'] == True:
            global workerNumNow
            workerNumNow += 1
            if workerNumNow == numWorkers:
                global startTime
                startTime = time()
            print("WORKER NUMBER: {}".format(workerNumNow))
        # store the complexity to a list for calculate later
        commitsComplexity.append(args['complexity'])
        print("Average complexity for commit {} is {}.".format(args['commit'], args['complexity']))

        # as there is the pull function without complexity added, so a None is added to the list, so need to +1
        if len(commitsComplexity) == commitsNum + 1:
            endTime = time() - startTime
            totalComplexity = 0
            for x in commitsComplexity:
                if x != None:
                    xcomp = float(x)
                    totalComplexity += xcomp

                    # calculate the average complexity
                    averageComplexity = totalComplexity / commitsNum
            print("\n\nAverage cyclomatic complexity for the repository ({}/{}) is: {}"
                  .format(owner, repo, averageComplexity))
            print("{} workers finished work in {} seconds\n\n".format(numWorkers, endTime))


api.add_resource(cycCalculator, '/cyc', endpoint="cyc")

if __name__ == '__main__':
    numWorkers = int(input("How many workers do you want:"))
    workerNumNow = 0
    startTime = 0.0
    data = []
    page = 1
    commits = []
    owner = input(
        "\nPress enter to use default repository: python/core-worlflow\nOr input the repository owner:")
    if len(owner) != 0:
        repo = input("Input the repository name:")
    else:
        owner = "python"
        repo = "core-workflow"

    endFlag = False
    while not endFlag:
        r = requests.get(
            "https://api.github.com/repos/{}/{}/commits?page={}&per_page=100".format(owner, repo, page))
        data += json.loads(r.text)
        # each page has 100 commit max, so check if it reach the end through checking if the data is less than page *100
        if len(data) < page * 100:
            endFlag = True
        page += 1
    # total commits number
    commitsNum = 0
    for d in data:
        commits.append(d['sha'])
        print(d['sha'])
        commitsNum += 1
    print("\n\nTotal number commit for the given repository: " + str(commitsNum))
    # use a list to store the complexity of each commit.
    commitsComplexity = []
    app.run(port=5000)
