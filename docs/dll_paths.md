# Adding & Removing DLL Search Paths in Python

Ensuring that DLLs can be found be python (and DLLs loaded by the process) may need to be solved differently depending on<br> 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(a) Python version<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) The DLL loading logic implemented in the package(s) using DLLS. 

Therefore, simple functions called `ensure_dll` and `forget_dll` were created to handle the different cases in a simple way.

## Example of using `ensure_dll` and `forget_dll`

```python
from pathtub import ensure_dll, forget_dll
import usb.backend.libusb1

#try loading library without adding the dlls to search path -> LibraryNotFoundException
usb.backend.libusb1._load_library()

dll_folder32 = r'C:\path to\libusb-1.0.21\MS32\dll'
ensure_dll(dll_folder32)

usb.backend.libusb1._load_library()
# <WinDLL 'C:\path to\libusb-1.0.21\MS32\dll\libusb-1.0.dll', handle 62690000 at 0x7297580>
```
- Now, if for some reason we want to forget a DLL path, we can use

```
forget_dll(dll_folder32)

# -> LibraryNotFoundException
usb.backend.libusb1._load_library()
```
- Note that `ensure_dll` always adds DLL folder just for the duration of the Process, and therefore "forgetting" is not needed. 
- There might be some special cases (for example, wanting different versions of DLL with same name to be loaded), where forget_dll is needed 

## Appendix
### DLL search Python 3.8 onwards

- On Python 3.8+ searching for DLLs is done [a bit differently](https://docs.python.org/3.8/whatsnew/3.8.html#bpo-36085-whatsnew).
  - PATH and current working directory ***are not used***.
- New function called [os.add_dll_directory](https://docs.python.org/3.8/library/os.html#os.add_dll_directory)  was added.
- Seems that it is *not the case* always, even in Python 3.8 (depends on python package dll inclusion logic). See, for example https://github.com/np-8/pathtub/issues/2. 
### DLL Search Prior Python 3.8
- Could just add DLL folder to Process PATH and DLL's would be loaded.