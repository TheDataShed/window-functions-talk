# Window Functions Talk

## Running in Gitpod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/TheDataShed/window-functions-talk)

## Running Locally

### Install

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements/test.txt
```

## Running a SQL File

If postgres is running, you can run SQL files using:

```console
psql -f sql/rank_employees.sql
```

## References

Employee sample data modified from [Sling Academy](https://www.slingacademy.com/article/employees-sample-data/)

[Window functions cheat sheet](https://learnsql.com/blog/sql-window-functions-cheat-sheet/)
