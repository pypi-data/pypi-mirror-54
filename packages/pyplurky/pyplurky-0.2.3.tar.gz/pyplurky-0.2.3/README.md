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

`pip install pyplurky`

Or get the latest version.

```shell
git clone https://github.com/Dephilia/PyPlurky.git
```



## Usage

Please check your `API.keys` file first.

```python
from pyplurky import pyplurky,api

pk=pyplurky(mode="BOT",key="API.keys")

def addAllFriend(plurk):
    plurk.alerts.addAllAsFriends()

def sayHi(plurk,data):
    id=data.plurk_id
    plurk.responses.responseAdd(id,"Hi")


pk.addRepeatHandler(addAllFriend)

pk.addResponseHandler("Hi",sayHi)

pk.addPlurkHandler("Hi",sayHi)

if __name__=="__main__":
    pk.main()
```

The pyplurky parameter `mode` must be `BOT` or `REPL`. Under REPL mode, you can test some code like:

`p.users.me()`

addResponseHandler: Add key word that will post when a new plurk shows.

addPlurkHandler: Add key word that will post when a new response shows.



## requirement

- plurk-ouath (Please install dev version, cause there is some bugs in pip version)

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
