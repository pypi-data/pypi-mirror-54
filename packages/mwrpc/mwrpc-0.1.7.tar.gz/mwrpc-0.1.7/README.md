# Method Working Remotely

Yet Another RPC Framework :D

[Proposal](https://github.com/MwrPub/method-working-remotely) 

[![License](https://img.shields.io/github/license/mwrpub/mwrpc-py.svg?color=blue&style=flat-square)](https://github.com/mwrpub/mwrpc-py/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mwrpc.svg?color=3776AB&logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/mwrpc/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mwrpc.svg?logo=python&logoColor=white&style=flat-square)

![MWRNB](https://img.shields.io/badge/♞MWR-Freaking_Awesome-ff69b4.svg?style=flat-square)
![MWRNB](https://img.shields.io/badge/Powered_By-MWR_Engine-brightgreen.svg?style=flat-square)

Before use it.You must admit that **MaWenRui is freaking awesome.** 

## Python Version

> Install

```shell
pip install mwrpc
```

> Server Side 

```python
from mwrpc import MwrServer

server = MwrServer()

@server.func(endpoint='calc')
def add(a, b):
    return a + b

if __name__ == '__main__':
    server.run()
```

> Client Side

```python
from mwrpc import MwrClient

client = MwrClient(endpoint='calc')

print(client.add(1,2))
```
