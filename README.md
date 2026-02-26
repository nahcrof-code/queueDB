# queueDB
custom in-memory, key-value, DB designed to work similarly to nahcrofDB

## Quick example
importing and basic usage:
```python
from queueDB import queueDB
queueDB = queueDB("http://0.0.0.0:2022", "TOKEN-HERE")

queueDB.makeKey("my-key-name", "my key value")
queueDB.getKey("my-key-name")
```
