# stdlogpj
python logging done my way

home: https://github.com/prjemian/stdlogpj

INSTALL

    pip install stdlogpj

USAGE:

    import stdlogpj
    logger = stdlogpj.standard_logging_setup("demo")
    logger.info("hello")

DEMO:

```python
#!/usr/bin/env python

import stdlogpj

logger = stdlogpj.standard_logging_setup("stdlogpj-demo")


def thing1(i):
    logger.info(f"something #{i+1}")


def main():
    logger.info("hello")
    for i in range(5):
        logger.debug("calling thing1()")
        thing1(i)
    logger.critical("complete")


if __name__ == "__main__":
    logger.warning("before main()")
    main()
    logger.error("after main(): no error, really")
```

## Rotate files and limit size

Using features of the [*RotatingFileHandler*](https://docs.python.org/3/library/logging.handlers.html?highlight=rotatingfilehandler#logging.handlers.RotatingFileHandler), 
it is possible to limit the size of the files by switching to a new log file,
saving the old log file(s) by appending a number.  Lower numbers are more recent.

Use this instead to limit logs to 1 MB and no more than 5 numbered (previous) log files:

```
logger = stdlogpj.standard_logging_setup("stdlogpj-demo", maxBytes=1024*1024, backupCount=5)
```
