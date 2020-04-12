### ✅ Ensuring folder is in PATH
#### What is ensure()?
`ensure(folder)`  checks if `folder` is in Process PATH<br>
- If `folder` is in Process PATH, does nothing
- If `folder` is not in Process PATH, adds it to Process PATH
- If `folder` is not in Process PATH **and** `permanent=True`, adds *also* to the User PATH or System PATH, depending on the `permanent_mode`. 


#### Example code for ensure()
- It is safe to call `ensure()` every time you load your script, for example. It only does something if `folder` is not found in your process `PATH`.
- The last "trailing" backslash of `folder` (if any) is ignored when comparing to any other folders.

```python
from pathtub import ensure
folder_to_add = r'C:\something to add to path\folder'
# 1) Check Process PATH, i.e. os.environ['PATH']
# 2) Add to Process PATH (temporary) if not found
ensure(folder_to_add)
```
#### Example code for ensure() with permanent addition
- You may also make the addition permanent (& visible to other processes). 
- Also this is safe to call every time script is starting. 
```python
from pathtub import ensure
folder_to_add = r'C:\something to add to path\folder'
# 1) Check Process PATH
# 2) Add to Process PATH if not found
# 3) Add also to User PATH (permanent), if 2) happens
ensure(folder_to_add, permanent=True)
```
- The Process PATH is initiated by copying it from parent process or taking copy of union of the permanent (User/System) PATH when process is started. For more info, see: [Windows PATH variables](path_variables.md).
- Full documentation of `ensure()` is in the source code ([pathtools.py](../pathtub/pathtools.py)).