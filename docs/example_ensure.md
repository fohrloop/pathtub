# Using `pathtub.ensure` to add DLL to PATH

## Description of problem
- Want to use [pyusb](https://github.com/pyusb/pyusb), and need to ensure that it finds the [libusb-1.0.dll](https://github.com/libusb/libusb/releases).
- Therefore, a folder containing the `libusb-1.0.dll` must be added to the PATH.

### Trying without adding DLL folder

- `get_backend()` returns no backends, since `libusb-1.0.dll` is not in the PATH
```python
import usb.backend.libusb1

#True 
usb.backend.libusb1.get_backend() is None
```
- Also this throws a `LibraryNotFoundException`
```python
usb.backend.libusb1._load_library()
```

```
# ---------------------------------------------------------------------------
# LibraryNotFoundException                  Traceback (most recent call last)
# ...
# C:\Python\Python37\lib\site-packages\usb\libloader.py in load_locate_library(candidates, cygwin_lib, name, win_cls, cygwin_cls, others_cls, find_library, check_symbols)
#     171         else:
#     172             _LOGGER.error('%r could not be found', (name or candidates))
# --> 173             raise LibraryNotFoundException(name)
#     174     else:
#     175         raise NoLibraryCandidatesException(name)

# LibraryNotFoundException: Libusb 1

```

### Adding DLL folder to PATH (current process)

- Running now `pathtub.ensure` before calling the `usb.backend.libusb1` functions, and the `libusb-1.0.dll` is found correctly.
- It is safe to leave the `ensure` command to the script. Running it multiple times does not do any harm; it just checks the `os.environ['PATH']`.
```python
from pathtub import ensure
import usb.backend.libusb1

# Folder that contains libusb-1.0.dll 
dll_folder = r'C:\My favourite folder\libusb\dll'

ensure(dll_folder)

# <usb.backend.libusb1._LibUSB at 0x23abb47bb38>
usb.backend.libusb1.get_backend()

#<WinDLL 'C:\My favourite folder\libusb\dll\libusb-1.0.dll', handle 7fffe9240000 at 0x23abb05e470>
usb.backend.libusb1._load_library()

```


### Adding DLL folder to PATH (permanently)

- By default, the `ensure` adds the DLL folder to the Process PATH, which means *only current python process will be able to see it*. 
- To add the DLL folder to the `User PATH` (see: [Windows PATH variables](path_variables.md).), and make `libusb-1.0.dll` available for all processes spawned afterwards, we use the `permanent` parameter.
- It is safe to leave the `ensure(dll_folder, permanent=True)` command to the script. Running it multiple times does not do any harm; it just checks the `os.environ['PATH']`.

```python
from pathtub import ensure
import usb.backend.libusb1

# Folder that contains libusb-1.0.dll 
dll_folder = r'C:\My favourite folder\libusb\dll'

# Addition: permanent=True
ensure(dll_folder, permanent=True)

# <usb.backend.libusb1._LibUSB at 0x23abb47bb38>
usb.backend.libusb1.get_backend()

#<WinDLL 'C:\My favourite folder\libusb\dll\libusb-1.0.dll', handle 7fffe9240000 at 0x23abb05e470>
usb.backend.libusb1._load_library()

```
- **Note**: If you have the DLL_folder already in the Process PATH of the current process, then `ensure(dll_folder, permanent=True)` will skip adding it to the (permanent) User Path. You may also use
  - `ensure(dll_folder, permanent=True, force=True)` or
  - `pathtub.add_to_path(dll_folder, 'user')`
- Note also that forcing adding to the permanent path each time a script is ran is not recommended since it takes some time. Consider the above as one-time-script.

