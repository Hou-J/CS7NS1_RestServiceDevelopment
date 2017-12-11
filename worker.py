import json, requests, subprocess

if __name__ == "__main__":
    r = requests.get("http://127.0.0.1:5000/repo",
                     json={'pullStatus': False})
    json_data = json.loads(r.text)
    repoUrl = json_data['repo']
    print(repoUrl)
    bashCommand = "cd pulledRepo &" \
                  "rm -rf .git/ &" \
                  "git init &" \
                  "git remote add origin {} &" \
                  "git branch --set-upstream-to=origin/<branch> master & " \
                  "git pull".format(repoUrl)

    process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    command_output = process.stdout.read().decode()
    print(command_output)

    print("Repository pulled completed")
    r = requests.get("http://127.0.0.1:5000/repo",
                     json={'pullStatus': True})

    numDone = 0
    nextCommit = True
    while nextCommit:
        r = requests.get("http://127.0.0.1:5000/cyc")
        print(r)
        print(json.loads(r.text))
        json_data = json.loads(r.text)
        print(json_data)
        hashsha = json_data['sha']
        print("Received: {}".format(hashsha))
        if hashsha == -2:
            print("Waiting for enough workers...")
        else:
            if hashsha == -1:
                print("No commit left")
                break

            bashCommand = "cd pulledRepo &" \
                          "git reset --hard {}".format(hashsha)
            process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            command_output = process.stdout.read().decode()
            print(command_output)

            command_output = subprocess.check_output(["radon", "cc", "-s", "-a", "pulledRepo"]).decode()
            print(command_output)

            if command_output.find("ERROR") != -1:
                # possinle error:[Errno 13] Permission denied   dont know why so just return 0
                r = requests.post("http://127.0.0.1:5000/cyc",
                                  json={'commit': hashsha, 'complexity': 0})
            elif command_output[command_output.rfind('(') + 1:-2] == "":
                print("NO RELEVENT FILES")
                r = requests.post("http://127.0.0.1:5000/cyc",
                                  json={'commit': hashsha, 'complexity': -1})
            else:
                averageCC = float(command_output[command_output.rfind("(") + 1:-2].strip(')'))
                r = requests.post("http://127.0.0.1:5000/cyc",
                                  json={'commit': hashsha, 'complexity': averageCC})
            numDone += 1
    print("\n\nCalculated the cyclomatic complexity for {} commits.\n\n".format(numDone))
