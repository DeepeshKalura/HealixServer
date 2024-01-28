import subprocess


newBranchName = input("Enter the branch name: ")
subprocess.run(["git", "checkout", "-b", "learn"+newBranchName])
subprocess.run(["pip", "install", "jupyter", "notebook"])
subprocess.run(["touch", newBranchName+".ipynb"])