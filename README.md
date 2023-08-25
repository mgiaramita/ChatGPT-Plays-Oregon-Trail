[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://black.readthedocs.io/en/stable/_static/license.svg)](https://github.com/psf/black/blob/main/LICENSE)

# ChatGPT Plays Oregon Trail

```
   ____ _           _    ____ ____ _____                
  / ___| |__   __ _| |_ / ___|  _ \_   _|               
 | |   | '_ \ / _` | __| |  _| |_) || |                 
 | |___| | | | (_| | |_| |_| |  __/ | |                 
  \____|_| |_|\__,_|\__|\____|_|    |_|                 
 |  _ \| | __ _ _   _ ___                               
 | |_) | |/ _` | | | / __|                              
 |  __/| | (_| | |_| \__ \                              
 |_|__ |_|\__,_|\__, |___/           _____          _ _ 
  / _ \ _ __ ___|___/_  ___  _ __   |_   _| __ __ _(_) |
 | | | | '__/ _ \/ _` |/ _ \| '_ \    | || '__/ _` | | |
 | |_| | | |  __/ (_| | (_) | | | |   | || | | (_| | | |
  \___/|_|  \___|\__, |\___/|_| |_|   |_||_|  \__,_|_|_|
                 |___/                                  
``` 
##### ChatGPT attempts to play through the 1978 version of Oregon Trail.

## <sub> What is it?

* Another command line tool for the [OpenAI API - Docs](https://platform.openai.com/docs/introduction).
* Allows ChatGPT to play through the classic game [Oregon Trail (1978)](https://en.wikipedia.org/wiki/The_Oregon_Trail_(1971_video_game)).
* It will try its best to play through the game. You can continue or stop the game at each step in execution.

![1](imgs/1.png)
![2](imgs/2.png)
![3](imgs/3.png)
![4](imgs/4.png)

## <sub> How to install.

* Install the latest version of [Python 3](https://www.python.org/downloads).
* Install the OpenAI [Python package](https://pypi.org/project/openai).
* Install [pexpect](https://pypi.org/project/pexpect) to control the Zork process. 
* Clone the repo.
* Oregon Trail can be installed in a number of ways and it depends on your system.
  * The original [BASIC source](https://archive.org/details/creativecomputing-1978-05/page/n143/mode/2up) was made public in 1978 and implementations of that can be found online ([example1](https://github.com/fortran-gaming/oregon-trail-1975), [example2](https://github.com/topherPedersen/OregonTrail1978)).
  * I found it easy to use [this Python 3 implementation](https://github.com/philjonas/oregon-trail-1978-python) of the code. Just install (download) the repo onto your system and then edit the config accordingly.
  * It is important that the version you choose runs in the terminal without any graphical interface. ChatGPT needs to be able to read the program's output after all.

## <sub> How to use.

* Add your OpenAI API key to <b>config.ini</b>.
* Ensure Oregon Trail command in <b>config.ini</b> is correct or update it for your specific install.
  * If Installed with the Python link from above it will work with the default (Just ensure the path is correct for your install location).
* python3 chatgpt_plays_ot.py
  * Run default application.
* python3 chatgpt_plays_ot.py -h
  * Display help message.
* python3 chatgpt_plays_ot.py -m "gpt-4"
  * Use model "gpt-4".
