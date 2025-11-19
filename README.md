# Introduction

An inventory management terminal user-interface (TUI).

## Philosophy

The overall goal of this project is to keep the elements native to the Python standard library, limiting the reliance on
third-party libraries.
Why?
Think about the scenario when the third-party library becomes deprecated/archived and/or maintaining dependencies
require extensive support.

- Lightweight/Minimal
- Portable
- Maintainable/Scalable

## Tech Stack

- Python
- SQLite
- Textual
- Docker

<img src="./docs/2025nov12_inv_mgnt_design.png" alt="Design & architecture"></img>

## Install Guide

Prerequisite:  
_NOTE:_ This project assumes you're using a Linux or Darwin system.

- Python installed and/or version; verify using:  
  `which python` or `python --version`

1. Create or navigate to your working directory:

```
# create working directory (can name it whatever you want.)
mkdir capy_tui

# navigate to the working directory
cd <working_directory>
EX: cd capy_tui
```

2. Create a virtual environment:

```
WHY? Isolates your working directory from system files and dependencies. => creates a sandbox

# navigate into the working directory if you haven't already...
# create a virtual environment (can be named whatever you want.)
python -m venv <name_of_virtual_environment>

```

3. Activate the virtual environment:  
   `source <name_of_virtual_environment>/bin/activate`  
    _NOTE:_ If done correctly, then you should see the name of your virtual environment beside your prompt of your terminal console.  
    _NOTE:_ You can deactivate the virtual environment by executing the command `deactivate`
4. Install dependencies: `pip install -r requirements.txt`  
   _NOTE:_ If done correctly, you should be able to execute certain binaries (Textual framework) within the virtual environment but not outside of the environment.
5. Run program: `textual run main.py`

Please refer to the [Troubleshooting Guide](#troubleshooting-guide) for common issues.

## User Guide

## Troubleshooting Guide

## License

Please refer to [LICENSE](./LICENSE) for more details.

## Contribution & Support

Please follow the [CONTRIBUTING](./CONTRIBUTING.md) guide. Any support is much appreciated!

@Author: capy
