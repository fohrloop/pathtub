## pathtub

Simple python functions for reading and editing Windows PATH.




### Features
-  Uses Powershell commands under the hood
   -  `$Env:Path`
   -  `[Environment]::GetEnvironmentVariable(...)`
   -  `[Environment]::SetEnvironmentVariable(...)`
-   Is not limited by the [1024 character limit](https://superuser.com/questions/387619/overcoming-the-1024-character-limit-with-setx).



## Installing
### Option A: Install from PyPi
```
pip install pathtub
```

### Option B: Install from GitHub
- Download this package and run
```
pip install <this_folder_path>
```
where `<this_folder_path>` refers to the folder with the `setup.py`. 


# Usage
- [Getting path variables](#getting-path-variables)
- [Setting PATH (User) variables](#setting-path-user-variables)
- [Setting PATH (System/Machine) variables](#setting-path-systemmachine-variables)
- [Removing PATH (User) variables](#removing-path-user-variables)
- [Removing PATH (System/Machine) variables](#removing-path-systemmachine-variables)
 - [Checking if folder is in PATH](#checking-if-folder-is-in-path)
  

### Getting path variables
```python
from pathtub import get_path

# Reads $Env:Path
path = get_path()
# Reads [Environment]::GetEnvironmentVariable('Path', 'User')
path_user = get_path("user")
# Reads [Environment]::GetEnvironmentVariable('Path', 'Machine')
path_machine = get_path("machine")
```
#### Example output
```python
In [1]: print(get_path('user')) # returns a str
C:\Python\Python37\Scripts\;C:\Python\Python37\;C:\Python\Python37-32\Scripts\;C:\Python\Python37-32\;C:\Users\USER\AppData\Roaming\npm;C:\Users\USER\AppData\Local\Microsoft\WindowsApps;C:\Program Files\Microsoft VS Code\bin;C:\Programs;C:\Programs\fciv;C:\texlive\2018\bin\win32;C:\Programs\apache-maven-3.6.2\bin;C:\Program Files\Java\jdk-13.0.1\bin;C:\Program Files (x86)\Common Files\Oracle\Java\javapath;C:\Programs\cloc;C:\Users\USER\AppData\Local\Programs\Microsoft VS Code\bin;
``` 
- **Note**: For some reason, the `$Env:Path` does not always update instantly (without reboot/relogin), even if the `[Environment]::GetEnvironmentVariable('Path', ...)` are updated. 
  
### Setting PATH (User) variables

- User PATH before edits: [Screenshot](img/before-setting-user.png)
- Adding a folder to PATH
  
```python
In [1]: from pathtub import add_to_path

In [2]: added = add_to_path(r'C:\My new folder\added to user PATH')

In [3]: added
Out[3]: True

# There is protection against adding duplicate entries
In [4]: added = add_to_path(r'C:\My new folder\added to user PATH')

In [5]: added
Out[5]: False
```

- User PATH after edits: [Screenshot](img/after-setting-user.png)



### Setting PATH (System/Machine) variables
- Similar to setting User PATH variables
- Change mode to "machine" and *Run the script with Admin rights*.

```
from pathtub import add_to_path
added = add_to_path(r'C:\My new folder\added to machine PATH', mode='machine')
```

### Removing PATH (User) variables

```python
In [1]: from pathtub import remove_from_path

In [2]: removed = remove_from_path(r'C:\My new folder\added to user PATH')

In [3]: removed
Out[3]: True

# Can only remove once. Safe to call multiple times.
In [4]: removed = remove_from_path(r'C:\My new folder\added to user PATH')

In [5]: removed
Out[5]: False
``` 


### Removing PATH (System/Machine) variables
- Similar to removing User PATH variables
- Change mode to "machine" and *Run the script with Admin rights*.

```
from pathtub import add_to_path
removed = remove_from_path(r'C:\My new folder\added to machine PATH', mode='machine')
```
### Checking if folder is in PATH
- **Note**: You don't have to worry if the saved PATH item ends with a backslash or not; both cases are checked.
```python
# Check the `$Env:Path` (Powershell) / `PATH` (cmd) variable
found = is_in_path() # same as is_in_path("path") 

# Checks the `[Environment]::GetEnvironmentVariable('Path','User')`; The "User PATH"
found_user = is_in_path("user")

# Checks the `[Environment]::GetEnvironmentVariable('Path','Machine')`; The "System PATH"
found = is_in_path("machine")
```
#### Example
```python
In [1]: from pathtub import is_in_path

In [2]: found = is_in_path('C:\\Python\\Python37\\', 'user')

In [3]: found
Out[3]: True

# It does not matter if the seach folder or the folder saved
# to PATH has "\" as the last character.
In [4]: found = is_in_path(r'C:\Python\Python37', 'user')

In [5]: found
Out[5]: True

In [6]: found = is_in_path(r'C:\Nonexistent\path', 'user')

In [7]: found
Out[7]: False
```