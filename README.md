# gr-toptek v1.0.0

This GNURadio OutOfTree module allows you to interface a TopTek amplifier using [this](https://github.com/eosti/toptek-control) controller (essentially a wrapper around that interface). This also provides a Push-To-Talk (PTT) block as well.

## Installation

First clone and build using cmake
```
git clone https://github.com/swarnavaghosh04/gr-toptek
cd gr-toptek
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

Then, continue running the following in the `build` directory after cmake for your system

### Debain Based
```
cpack -G DEB
sudo dpkg -i *.deb
```
### RPM Based
```
cpack -G RPM
sudo rpm -i *.rmp
```
### ArchLinux
```
makepkg -si
```
### MSYS2 (Windows)
```
makepkg-mingw -si
```