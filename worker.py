import json, requests, subprocess

if __name__ == "__main__":
    # get the repository url
    r = requests.post("http://127.0.0.1:5000/cyc", json={'pull': False})
    repoUrl = json.loads(r.text)
    print(repoUrl)
    bashCommand = "cd pulledRepo &" \
                  "rm -rf .git/ &" \
                  "git init &" \
                  "git remote add origin {} &" \
                  "git branch --set-upstream-to=origin/<branch> master & " \
                  "git pull".format(repoUrl)
    # use cmd commend on windows to get the repository files to the pulledRrpo folder
    process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    command_output = process.stdout.read().decode()
    print(command_output)
    # let the server start the time count
    print("Repository pulled completed")
    r = requests.post("http://127.0.0.1:5000/cyc",
                     json={'pull': True})
    # count this current worker's contribution
    numDone = 0
    # keep on getting commit until no commit left
    while True:
        r = requests.get("http://127.0.0.1:5000/cyc")
        hashsha = json.loads(r.text)
        # end getting and jump out of the loop if no commit left
        if hashsha == True:
            print("No commit left")
            break
        print("Received: {}".format(hashsha))

        if hashsha == False:
            print("Waiting for enough workers...")
        else:
            # reset the code to the 'sha' time
            bashCommand = "cd pulledRepo &" \
                          "git reset --hard {}".format(hashsha)
            process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            command_output = process.stdout.read().decode()
            print(command_output)
            # calculate the cyclomatic complexity using cmd commend radon cc,
            # -s means using figure to show the complexity, -a means average
            command_output = subprocess.check_output(["radon", "cc", "-s", "-a", "pulledRepo"]).decode()
            print(command_output)

            if command_output.find("ERROR") != -1:
                # possible error:[Errno 13] Permission denied   dont know why so just return 0
                # might be the problem that sometime the \\ shows in the dir
                r = requests.post("http://127.0.0.1:5000/cyc",
                                  json={'commit': hashsha, 'complexity': 0})
            elif command_output[command_output.rfind('(') + 1:-2] == "":
                print("NO RELEVENT FILES")
                r = requests.post("http://127.0.0.1:5000/cyc",
                                  json={'commit': hashsha, 'complexity': 0})
            else:
                averageCC = float(command_output[command_output.rfind("(") + 1:-2].strip(')'))
                r = requests.post("http://127.0.0.1:5000/cyc",
                                  json={'commit': hashsha, 'complexity': averageCC})
            numDone += 1
    print("\n\nCalculated the cyclomatic complexity for {} commits.\n\n".format(numDone))
