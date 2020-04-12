![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/np-8/pathtub)&nbsp;![PyPI](https://img.shields.io/pypi/v/pathtub)&nbsp;![PyPI - Downloads](https://img.shields.io/pypi/dm/pathtub)&nbsp;![GitHub](https://img.shields.io/github/license/np-8/pathtub)

## 🛁 pathtub

Reading and editing [Windows PATH variables](docs/path_variables.md) and ensuring python finds your DLLs.


   &nbsp;&nbsp;&nbsp;&nbsp;✅ **Ensuring** that a folder exists in Path. <br>
   &nbsp;&nbsp;&nbsp;&nbsp;🔗 **Ensuring** that DLL(s) are found by python. <br>
   &nbsp;&nbsp;&nbsp;&nbsp;🧽 **Cleaning** the PATH (duplicates, removed folders, sorting) <br>
   &nbsp;&nbsp;&nbsp;&nbsp;✏️ **Adding** or **removing** folders to/from Path (temporary or permanently) <br>



## Installing
```
pip install pathtub
```


## Usage

- [Ensuring folder is in PATH](#-ensuring-folder-is-in-path)
- [Ensuring that DLL(s) are found](#-ensuring-that-dlls-are-found)
- [Cleaning PATH](#-cleaning-path)
- [Rest of the docs](#rest-of-the-docs)
  - [Getting path variables](docs/rest_of_the_docs.md#getting-path-variables)
  - [Adding permanently to PATH](docs/rest_of_the_docs.md#adding-permanently-to-path-user)
  - [Removing permanently from PATH](docs/rest_of_the_docs.md#removing-permanently-from-path-user)
  - [Checking if folder is in PATH](docs/rest_of_the_docs.md#checking-if-folder-is-in-path)
  


### ✅ Ensuring folder is in PATH
```python
from pathtub import ensure
folder_to_add = r'C:\something to add to path\folder'
# 1) Check Process PATH
# 2) Add to Process PATH if not found
# 3) Add also to User PATH (permanent), if 2) happens
ensure(folder_to_add, permanent=True)
```
#### What is ensure()?
`ensure(folder)`  checks if `folder` is in Process PATH<br>
- If `folder` is in Process PATH, does nothing
- If `folder` is not in Process PATH, adds it to Process PATH
- If `folder` is not in Process PATH **and** `permanent=True`, adds *also* to the User PATH or System PATH, depending on the `permanent_mode`. 
  
⚠️ If you want to ensure a *DLL folder* is visible to python, use `ensure_dll` instead. 


### 🔗 **Ensuring** that DLL(s) are found 
```python
from pathtub import ensure_dll
dll_folder = r'C:\path to\libusb-1.0.21\MS32\dll'
ensure_dll(dll_folder)
```
- `ensure_dll()` is for making sure that python finds needed DLL's (and the DLL's find their dependencies, if any.)
- You may use `ensure_dll` and `forget_dll` for adding and removing dll folder to/from search path.
- See also: [Example of using ensure_dll and forget_dll](docs/dll_paths.md)




### 🧽 Cleaning PATH
```python
from pathtub import clean
# Default parameter values shown
clean(sort=True, remove_non_existent=True, remove_user_duplicates=True)
```
### What does it do
- Removes duplicates and empty entries (`;;`) from the "User PATH" and "System PATH" (trailing backslash neglected when comparing two folders). Editing "System PATH" needs that python is executed with Admin rights.
- Sorts PATH(s) alphabetically (optional, enabled by default). Controlled with the `sort` parameter.
- Removes folders from PATH(s) that do not exist on the filesystem (optional, enabled by default). Controlled with the `remove_non_existent` -parameter.
- Removing from "User PATH" the entries that are in the "System PATH" (optional, enabled by default). Controlled with the `remove_user_duplicates`-parameter.

#### Screenshots of User PATH before and after clean:
   ![User PATH](img/user-before-after-clean.png)  


- For more detailed example, see [Full example of pathtub.clean](docs/example_clean.md)
- Full documentation of `clean()` is in the source code ([pathtools.py](pathtub/pathtools.py)).

### Rest of the docs
Did not find what you were looking for? See the [Rest of the docs](docs/rest_of_the_docs.md).
