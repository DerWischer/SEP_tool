The tool makes use of [code-mat](https://github.com/adamtornhill/code-maat) developed by Adam Tornhill. A standalone jar is included in the repository in the folder "code-maat".
# Installation
1. Install [graphviz](https://www.graphviz.org/) and add it to your PATH.

2. Install the python3 package [graphviz](https://pypi.python.org/pypi/graphviz).
        
        pip3 install graphviz

If step 1 and step 2 are not executed correctly, you won't be able to generate the graph. Make sure to set up everything as described.
# Usage
Run the tool with the following command

    python3 tool.py <path to repository> <min_degree>

The path to the repository is mandatory. The minimum degree of coupling between files is optional.