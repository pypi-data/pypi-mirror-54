# esphomeflasher

esphomeflasher is a utility app for the [esphomelib](https://esphomelib.com/esphomeyaml/index.html)
framework and is designed to make flashing ESPs with esphomelib as simple as possible by:

 * Having pre-built binaries for most operating systems.
 * Hiding all non-essential options for flashing. All necessary options for flashing
   (bootloader, flash mode) are automatically extracted from the binary.
   
This project was originally intended to be a simple command-line tool,
but then I decided that a GUI would be nice. As I don't like writing graphical
front end code, the GUI largely is based on the 
[NodeMCU PyFlasher](https://github.com/marcelstoer/nodemcu-pyflasher)
project.

The flashing process is done using the [esptool](https://github.com/espressif/esptool)
library by espressif.

## Installation

Es doesn't have to be installed, just double-click it and it'll start.
Check the [releases section](https://github.com/OttoWinter/esphomeflasher/releases)
for downloads for your platform.

## Installation Using `pip`

If you want to install this application from `pip`:

- Install Python 3.x
- Install [wxPython 4.x](https://wxpython.org/) manually or run `pip3 install wxpython`
- Install this project using `pip3 install esphomeflasher`
- Start the GUI using `esphomeflasher`. Alternatively, you can use the command line interface (
  type `esphomeflasher -h` for info)

## Build it yourself

If you want to build this application yourself you need to:

- Install Python 3.x
- Install [wxPython 4.x](https://wxpython.org/) manually or run `pip3 install wxpython`
- Download this project and run `pip3 install -e .` in the project's root.
- Start the GUI using `esphomeflasher`. Alternatively, you can use the command line interface (
  type `esphomeflasher -h` for info)

## License

[MIT](http://opensource.org/licenses/MIT) © Marcel Stör, Otto Winter
