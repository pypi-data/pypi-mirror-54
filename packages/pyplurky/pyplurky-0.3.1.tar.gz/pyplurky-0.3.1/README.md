# PyPlurky
![](https://img.shields.io/badge/Version-a2.0.0-blue.svg?longCache=true&style=popout) ![](https://img.shields.io/badge/python-v3.7-blue) ![](https://img.shields.io/github/issues/Dephilia/PyPlurky) ![](https://img.shields.io/github/forks/Dephilia/PyPlurky) ![](https://img.shields.io/github/stars/Dephilia/PyPlurky) ![](https://img.shields.io/github/license/Dephilia/PyPlurky)

The **best surface** between Plurk Oauth and python.

This is a project that try to connect plurk_oauth and python better.
Make it easier to use for python developer.

For more API information, please visit:

- [Plurk API](https://www.plurk.com/API)
- [plurk-oauth](https://github.com/Dephilia/plurk-oauth)


## Why you need it
This project is to make "bot develop" easier. For some reasons, we need a plurk bot, but everything is not prepared.
That is why we need it: A good dispatcher, handler, and easier function to call API.
A good error manager for developing more efficiency.
If you only want to develop plurk reader, it is also fine to ignore function like dispatcher.

## Installation

```shell
pip install pyplurky
```

Or get the latest version.

```shell
git clone https://github.com/Dephilia/PyPlurky.git
```



## Usage

Please check your `API.keys` file first. Key in your consumer key from [Plurk API page](https://www.plurk.com/PlurkApp/), if you already have access token, it's ok to key in.

First import module.

```python
from pyplurky import pyplurky
```



There are three mode can be used in pyplurky.

```python
pk=pyplurky(mode="BOT",key="API.keys")
# Bot mode

pk=pyplurky(mode="READING",key="API.keys")
# This will listen to your timeline but do nothing.

pk=pyplurky(mode="REPL",key="API.keys")
# Enter to REPL environment
```

The pyplurky parameter `mode` must be `BOT` or `REPL` or `READER`. Under REPL mode, you can test some code like:

`p.users.me()`

`p` is the abbreviation of plurk object.



More example is like the under code:

```python
from pyplurky import pyplurky,api

pk=pyplurky(mode="BOT",key="API.keys")

def hey():
    print("hey")

def addAllFriend(plurk):
    plurk.alerts.addAllAsFriends()

def sayHi(plurk,data):
    id=data.plurk_id
    plurk.responses.responseAdd(id,"Hi")

    
pk.job.every(5).minutes.do(hey)
pk.JobStart()

pk.addRepeatHandler(addAllFriend)

pk.addResponseHandler("Hi",sayHi)

pk.addPlurkHandler("Hi",sayHi)

if __name__=="__main__":
    pk.main()
```



`addResponseHandler`: Add key word that will post when a new plurk shows.

`addPlurkHandler`: Add key word that will post when a new response shows.



The job object use python [schedule module](https://schedule.readthedocs.io/en/stable/), for more usage, please check it.

## requirement

- plurk-ouath
- schedule

## Bugs in Plurk
Here shows some plurk bugs, not cause by module.

1. cliques.add/remove will always return true
2. No cliques delete
3. block.block/unblock will always return true
4. Comet Server instability



## Future Work

1. **Complete All API at test console** (not write on document)
2. Function Handler (Plurk/Response/Continue) (Done)
3. Routine Work
4. Event Setter
5. Use both getPlurk API and comet to prevent comet server problem.
6. Async handler
