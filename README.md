The tool makes use of [code-mat](https://github.com/adamtornhill/code-maat) developed by Adam Tornhill. A standalone jar is included in the repository in the folder "code-maat".
# Installation
1. Install [graphviz](https://www.graphviz.org/) and add it to your PATH.

2. Install the python3 package [graphviz](https://pypi.python.org/pypi/graphviz).
        
        pip3 install graphviz
# Usage
Follow the three steps described below.
## Step 1
Generate the git log for the repository you want to analyse. Go into the git repository you want to analyse and run the following command:
    
    git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > <file_step_1>

	
	If on Windows
	git log --all --numstat --date=short --pretty=format:"--%h--%ad--%aN" --no-renames > file_step_1
	
## Step 2
Next, use code-maat to anaylse the log you generated in step one. In the repository you'll find a runnable jar file of code-maat. Go into the tool's repository and enter the folder "code-maat". Execute the following command:
    
    java -jar code-maat.jar -l <file_step_1> -c git2 -a coupling > <file_step_2>
    
## Step 3
Go into the tool's repositoy and run the tool with the following command:
    
    python3 tool.py <file_step_2>

The rendered diagram is found in the folder "rendered". If you set up a default pdf viewer, it should open automatically.
