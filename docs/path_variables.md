## Windows PATH variables 
- There are three different sets of environment variables
  - Process (temporary)
  - User (permanent)
  - Machine (aka. system, permanent) 
- Windows `Path` is an Windows environment variable with the name `Path`.

## How the PATH variables are inherited & copied

```
    User PATH      Machine/System PATH 
            \                  / 
             \                / 
              v              v  
    +-----------------------------------------------------+
    | MainProcess                                         |
    |                                                     |
    |  PATH = Process PATH                                |
    |    (initially copy of User and Machine PATH)        |
    |                                                     |
    +-----------------------------------------------------+
                        |                                  
                        |                                  
                        v                                  
    +-----------------------------------------------------+
    | ChildProcess                                        |
    |                                                     |
    |   PATH = Process PATH                               |
    |     (initially copy of MainProcess PATH)            |
    +-----------------------------------------------------+
```
*Thanks for the diagram tool,* [*textik.com*](https://textik.com/)
### 1) Process environment variables
- These are used for setting **temporary** environment variables. They are destroyed when the process terminates.
- When process starts, it gets either (a) Copy of the Process PATH from its parent or (b) Copy of union of User and System PATH.
#### 1.1) Getting Process environment variables
- In Python, just read `os.environ['PATH']`.
- This is the same as reading value of `$Env:Path` (powershell) or `PATH` (cmd).
#### 1.2) Setting Process environment variables
- In Python, just edit `os.environ['PATH']`.

  
### 2) User environment variables
- These values are **permanent**.
- When process starts, the Process PATH receives all items from User PATH.
#### 2.1) Getting User environment variables
When   [`[Environment]::GetEnvironmentVariable(...)`](https://docs.microsoft.com/en-us/dotnet/api/system.environment.getenvironmentvariable) is called with [`EnvironmentVariableTarget.User`](https://docs.microsoft.com/en-us/dotnet/api/system.environmentvariabletarget#fields) as the target, then ([source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable))
 - Variable is retrieved from the `HKEY_CURRENT_USER\Environment` key of the local computer's registry
#### 2.2) Setting User environment variables
When   [`[Environment]::SetEnvironmentVariable(...)`](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable) is called with [`EnvironmentVariableTarget.User`](https://docs.microsoft.com/en-us/dotnet/api/system.environmentvariabletarget#fields) as the target, then
 - Variable is stored in the `HKEY_CURRENT_USER\Environment` key of the local computer's registry. This means that the environment variable is stored **permanently**. ([source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable))
 - Other applications are notified of the set operation by a Windows [`WM_SETTINGCHANGE`](https://docs.microsoft.com/en-us/windows/win32/winmsg/wm-settingchange) message. ([source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable))
 - Variable is copied to instances of File Explorer that are running as the current user
 - Environment variable is then inherited by any new processes that the user launches from File Explorer.
 - Microsoft recommends that the length is kept under 2048 characters. The hard limit is 32766 characters. ([source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable)) 
- **Note**: Setting User environment variable does not necessarily update the Process environment variables.

### 3) System/Machine environment variables
- These values are **permanent**.
- When process starts, the Process PATH receives all items from System/Machine PATH.
- Need admin rights to edit these.
#### 3.1) Getting System/Machine environment variables
When   [`[Environment]::GetEnvironmentVariable(...)`](https://docs.microsoft.com/en-us/dotnet/api/system.environment.getenvironmentvariable) is called with [`EnvironmentVariableTarget.Machine`](https://docs.microsoft.com/en-us/dotnet/api/system.environmentvariabletarget#fields) as the target, then 
 - Variable is retrieved  from the `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment`[*1]  key of the local computer's registry. 
#### 3.2) Setting System/Machine environment variables
When   [`[Environment]::SetEnvironmentVariable(...)`](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable) is called with [`EnvironmentVariableTarget.Machine`](https://docs.microsoft.com/en-us/dotnet/api/system.environmentvariabletarget#fields) as the target, then 
 - Variable is stored to the `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment`[*1]  key of the local computer's registry. This means that the environment variable is stored **permanently**. ([source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable))
 - Other applications are notified of the set operation by a Windows [`WM_SETTINGCHANGE`](https://docs.microsoft.com/en-us/windows/win32/winmsg/wm-settingchange) message. ([source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable))
 - Variable is copied to instances of File Explorer that are running as the current user
 - Environment variable is then inherited by any new processes that the user launches from File Explorer.
 - Microsoft recommends that the length is kept under 2048 characters. The hard limit is 32766 characters. ([source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable))
 - **Note**: Setting Sytem/Machine environment variable does not necessarily update the Process environment variables.
  
  #### footnotes
  [*1] `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment` according to this [source](https://docs.microsoft.com/en-us/dotnet/api/system.environmentvariabletarge), `HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment` according to this [source](https://docs.microsoft.com/en-us/dotnet/api/system.environment.setenvironmentvariable). These might be the same thing.