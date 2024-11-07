# Contributing to AppBuilder

Thanks for your interest in contributing to AppBuilder!  Please follow these guidelines to make the contribution process easy and effective for everyone involved.


## Contributing Guide for python SDK

### Development

Clone the source code from Github

```
git clone https://github.com/baidubce/app-builder.git
```

Use `pip` to install from source

```shell
cd appbuilder
pip install -e .
```

`-e` means "editable mode" in pip. With "editable mode" all changes to python code will immediately become effective in the current environment.

### Testing

We highly recommend writing tests for new features or bug fixes and ensure all tests passing before submitting a PR.

AppBuilder uses [unittest](https://docs.python.org/3/library/unittest.html) as the test framework, requires no 3rd party dependencies to install.

Before running tests, make sure add the following environment variables:

```shell
export TEST_CASE=CPU_PARALLEL
export APPBUILDER_TOKEN=<your_token>
```


To run all existing test cases together, run

```
pip install -e .[all]
sh appbuilder/tests/run_python_test.sh
```

If you only want to run specific test file, e.g.:

```
python appbuilder/tests/test_playground.py
```


To debug tests in vs code update .env file to roo folder of the project:
```
APPBUILDER_TOKEN=<your-token>
APPBUILDER_TOKEN_V2=<your-token>
TEST_CASE=CPU_SERIAL
```

and add/update `.vscode/settings.json` file with the following content:

```
{
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./appbuilder",
        "-p",
        "test*.py"
    ],
    "python.testing.unittestEnabled": true,
    "python.envFile": "${workspaceFolder}/.env"
}
```

