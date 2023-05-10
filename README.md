# cyDoomGeneric

Write doom ports in python!

Python bindings for [doomgeneric](https://github.com/ozkl/doomgeneric) with ease-of-use at heart.

To try it you will need a WAD file (game data). If you don't own the game, shareware version is freely available.

cyDoomGeneric should run on Linux, MacOS, and Windows.

## Porting

You must implement the `draw_frame` and `get_key` functions.

```
import cydoomgeneric as cdg

resx = 640
resy = 400

# Required functions
def draw_frame(pixels: np.ndarray) -> None:
def get_key() -> Optional[Tuple[int, int]]:

# Optional functions
def init() -> None:
def sleep_ms(ms: int) -> None:
def set_window_title(t: str) -> None:
def get_ticks_ms() -> int:

cdg.init(resx,
    resy,n
    draw_frame,
    get_key,
    init=init,
    sleep_ms=sleep_ms,
    get_ticks_ms=get_ticks_ms,
    set_window_title=set_window_title)
cdg.main()  # Optional parameter argv=[...]
```

 `get_key` should return `None` if all input has been processed, or a tuple `(pressed as 0 or 1, key)`. All possible keys are either members of the `Keys` enum, or the ascii value of the lowercase character `ord(c.lower())`.

Some additional documentation can be found in `cydoomgeneric/cydoomgeneric.pyx`.

## Building

The following python packages are required: `numpy cython`.

To build and install cydoomgeneric, run the following commands:

```
$ cd cydoomgeneric
$ python setup.py install
```

## Demo Screenshots

#### Pyplot
![pyplot](screenshots/pyplotdoom_1.png)

#### Libreoffice Calc
![calc](screenshots/calcdoom_0.png)

#### Minecraft: Pi Edition
![mcpi](screenshots/minepidoom_0.png)

## Running the Demo

###### Before running any demo, perform the build process mentioned above

#### Pyplot

Ensure that the `matplotlib` python package is installed.

```
$ cd cydoomgeneric
$ python demopyplot.py
```

#### Minecraft: Pi Edition

Ensure that the `mcpi scikit-image` packages are installed.

Before running the script, launch Minecraft: Pi Edition and join a world. The `scale` variable can be adjusted to change the display size. Currently the only way to quit the game is to kill the process (`C-z`).

To move, step on the appropriate block on the platform that the player is standing on. To press the fire, use, enter, or escape keys, hit (`RMB`) the appropriate block with the sword:
```
DIAMOND_BLOCK: FIRE
GOLD_BLOCK: USE
NETHER_REACTOR_CORE: ENTER
NETHER_REACTOR_CORE(active): ESCAPE
```

```
$ cd cydoomgeneric
$ python demominepi.py
```

#### LibreOffice Calc

Ensure that the libreoffice SDK (`libreoffice-dev` on Debian) is installed, and that you're using the system python installation instead of a virtual environment.

The `scale` variable can be adjusted in the range `[0,5]` to change the display size, idealy either 1 or 2. Lower scales will exponentially increase the setup time required prior to starting the game. Expect to wait a few minutes.

Sometimes the window will be tiny, so maximize it if neccessary. Also, you may experience unexpected issues while attempting to run this demo, and there's not much I can do because the UNO API has virtually no documentation and the code here has been pieced together from 10 year old forum posts for the Java or C++ version of the API.

Only run the following command once, unless the libreoffice process is killed:
```
$ libreoffice --nofirststartwizard --nologo --norestore --accept='socket,host=localhost,port=2002,tcpNoDelay=1;urp;StarOffice.ComponentContext' &
```

```
$ cd cydoomgeneric
$ python democalc.py
```

## TODO

- Windows build
- Fix segfault when closing game
- Implement sound
