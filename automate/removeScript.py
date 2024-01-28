import os
import subprocess

currentBranch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()

if(currentBranch == "production"):
    print("You are in production branch. Please switch to learn branch")
    exit()

if("learn" in currentBranch):
    currentBranch = currentBranch[5:]

print("Current Branch: ", currentBranch)


subprocess.run(["pip", "uninstall", "jupyter", "notebook"])

# delete the currentBranch.ipynb file
subprocess.run(["rm", currentBranch+".ipynb"])
subprocess.run(["git", "checkout", "production"])
subprocess.run(["git", "pull", "origin", "production"])

result = subprocess.run(["git", "merge", "learn"+currentBranch])


print("End of the automation script:    ")


