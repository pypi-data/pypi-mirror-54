# sockio

A concurrency agnostic socket library on python.

So far implemented REQ-REP semantics with auto-reconnection facilites.

Implementations for:

* classic blocking API
* future based API
* asyncio

Join the party by bringing your own concurrency library with a PR!

I am looking in particular for implementations over trio and curio.

## Installation

From within your favourite python environment:

```console
pip install sockio
```


## Usage

*asyncio*

```python
import asyncio
from sockio.aio import Socket

async def main():
    sock = Socket('acme.example.com', 5000)
    # Assuming a SCPI complient on the other end we can ask for:
    reply = await sock.write_readline(b'*IDN?\n')
    print(reply)

asyncio.run(main())
```

*classic*

```python
from sockio.sio import Socket

sock = Socket('acme.example.com', 5000)
# Assuming a SCPI complient on the other end we can ask for:
reply = sock.write_readline(b'*IDN?\n')
print(reply)
```
