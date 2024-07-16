<img src="https://github.com/sho96/Delta/blob/master/readmefiles/logo.png?raw=true" alt="LOGO">

# Delta [Python to C++ compiler](https://delta-lang.vercel.app)
<h3>The Python to C++ compiler</h3>
Delta lets you compile vanilla python code to C++. <br>
It also supports direct C++ implementation. <br>
Currently in development, so some features of Python may not work.

## Usage
```python compile.py sourcefile.dt``` (requires python 3.12+) <br>

## Using compiler executables
I've already made [executables for x64 on Windows & Mac](https://github.com/sho96/Delta/tree/master/compilers)<br>

If you want compiler executables on other platforms, you can easily do so by using [pyinstaller](https://pyinstaller.org/)<br>
### 1. Install pyinstaller
```pip install pyinstaller```
**Make sure to install pyinstaller for python 3.12+**
### 2. Compile
```pyinstaller --onefile compile.py```
The compiled executable will be in `dist/compile.exe`

