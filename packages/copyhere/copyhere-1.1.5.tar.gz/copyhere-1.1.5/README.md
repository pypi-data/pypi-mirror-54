# copyhere

A package to copy or unzip a file to cwd

Pypi: https://pypi.org/project/copyhere/

## install

pip install copyhere

## run

```bash
python -m copyhere
```

or

```python
import copyhere
copyhere.start()    # name=None (default) for using source file name
                    # name='' for user input a new name,
                    # name="any your new name"
```

to specify a folder to open in the selection window use `COPYHERE_SOURCEDIR` environment variable
