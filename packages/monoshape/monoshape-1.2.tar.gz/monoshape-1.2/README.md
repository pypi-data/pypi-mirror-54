# monoshape

This program takes an image that has well differentiated light and dark tones and extracts its monochromatic shape in the desired colour with a transparent background.

![Use demonstration](docs/demo.png?raw=true "Use demonstration")

This sofware can be used as final TUI app or as Python library.


## To set up

You can use Homebrew to install this program via my tap repository:

```sh
brew install glezseoane/homebrew-tap/monoshape
```

You also can use PyPI to install this program:

```sh
pip install monoshape
```

Alternative, clone and go to this repository home directory, and then run:

```sh
python setup.py install
```

Both methods install last **monoshape** stable version on your machine.


## Use as final app

Simple use:

```sh
monoshape image.png desired_shape.png
```

Draw a red shape:

```sh
monoshape image.png desired_shape.png -rgb 255 0 0
```

Explore the man page to know all possible functionalities.


## Use as library

Simply import main module and use export function:

```python
import monoshape.__main__ as monoshape

drawn = monoshape.extract_shape(path=source,
                                black_background=False,
                                white_shape=False,
                                rgb_shape=False,
                                red=None,
                                green=None,
                                blue=None)
```


<br>

Read the man of this tool to known more about its use.

> Note about man pages: if you use `pip` method to install this program, assert that man directories of your python environment are added to your `MANPATH` to can get this program's man pages with the `man` command. Python might install man pages in default machine level directories.

