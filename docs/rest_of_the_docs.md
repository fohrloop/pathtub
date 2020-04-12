
# Rest of the docs
## See also
  - For basic usage, please see the [front page](../README.md).
  - Deeper dive on [Windows PATH variables](path_variables.md).
### Details on underlying function calls
- For ***temporary*** (Process) Path get/set, the Python `os.environ['PATH']` is used.
-  For ***permanent*** (User/System) Path get/set, pathtub uses Powershell commands under the hood. 
   -  [`[Environment]::GetEnvironmentVariable(...)`](https://docs.microsoft.com/en-us/dotnet/api/system.environment.getenvironmentvariable)
   -  [`[Environment]::SetEnvironmentVariable(...)`](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable)


  
## Advanced usage topics
- [Getting path variables](#getting-path-variables)
- [Adding permanently to PATH (User)](#adding-permanently-to-path-user)
- [Adding permanently to PATH (System/Machine)](#adding-permanently-to-path-systemmachine)
- [Removing permanently from PATH (User)](#removing-permanently-from-path-user)
- [Removing permanently from PATH  (System/Machine)](#removing-permanently-from-path-systemmachine)
- [Checking if folder is in PATH](#checking-if-folder-is-in-path)

  



### Getting path variables
```python
from pathtub import get_path

# Reads os.environ['PATH'], which is same as PATH (cmd) or $Env:Path (powershell)
path = get_path() # same as get_path('process')
# Reads [Environment]::GetEnvironmentVariable('Path', 'User')
path_user = get_path("user")
# Reads [Environment]::GetEnvironmentVariable('Path', 'Machine')
path_machine = get_path("machine")
```
#### Example output
```
In [1]: print(get_path('user')) # returns a str
C:\Python\Python37\Scripts\;C:\Python\Python37\;C:\Python\Python37-32\Scripts\;C:\Python\Python37-32\;C:\Users\USER\AppData\Roaming\npm;C:\Users\USER\AppData\Local\Microsoft\WindowsApps;C:\Program Files\Microsoft VS Code\bin;C:\Programs;C:\Programs\fciv;C:\texlive\2018\bin\win32;C:\Programs\apache-maven-3.6.2\bin;C:\Program Files\Java\jdk-13.0.1\bin;C:\Program Files (x86)\Common Files\Oracle\Java\javapath;C:\Programs\cloc;C:\Users\USER\AppData\Local\Programs\Microsoft VS Code\bin;
``` 

  
### Adding permanently to PATH (User)

- Setting PATH (User) variable will make *permanent* changes to PATH variable (of course the changes can be reverted by [removing the item from the PATH](#removing-path-user-variables).)
- Adding a folder to PATH

```python
In [1]: from pathtub import add_to_path

In [2]: added = add_to_path(r'C:\My new folder\added to user PATH','user')

In [3]: added
Out[3]: True

# There is protection against adding duplicate entries
In [4]: added = add_to_path(r'C:\My new folder\added to user PATH', 'user')

In [5]: added
Out[5]: False
```

- User PATH  [before](img/before-setting-user.png) and  [after](img/after-setting-user.png) running the code above.



### Adding permanently to PATH (System/Machine)
- Similar to setting User PATH variables
- Setting PATH (System/Machine) variable will make *permanent* changes to PATH variable (of course the changes can be reverted by [removing the item from the PATH](#removing-path-systemmachine-variables).)
- Change mode to "machine" and *Run the script with Admin rights*.

```
from pathtub import add_to_path
added = add_to_path(r'C:\My new folder\added to machine PATH', mode='machine')
```

### Removing permanently from PATH (User) 

```python
In [1]: from pathtub import remove_from_path

In [2]: removed = remove_from_path(r'C:\My new folder\added to user PATH', 'user')

In [3]: removed
Out[3]: True

# Can only remove once. Safe to call multiple times.
In [4]: removed = remove_from_path(r'C:\My new folder\added to user PATH', 'user')

In [5]: removed
Out[5]: False
``` 

### Removing permanently from PATH  (System/Machine) 

- Similar to removing User PATH variables
- Change mode to "machine" and *Run the script with Admin rights*.

```
from pathtub import add_to_path
removed = remove_from_path(r'C:\My new folder\added to machine PATH', mode='machine')
```
### Checking if folder is in PATH
- **Note**: You don't have to worry if the saved PATH item ends with a backslash or not; both cases are checked.
```python
# Check the os.environ['PATH'] / PATH (cmd) / $Env:Path (Powershell) 
found = is_in_path() # same as is_in_path("process") 

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