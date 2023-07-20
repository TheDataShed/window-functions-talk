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

### Local DB

The `.gitpod.yml` outlines what is needed to set up an environment.
Or you can follow these commands:

Run postgres in Docker:

```shell
docker run -d \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  --name posty \
  -p 5432:5432 \
  postgres
```

Then set up the two tables:

```shell
psql -f sql/setup_db.sql
```

Then insert data into the tables:

```shell
psql -c "\copy website_visits from 'data/website_data.csv' DELIMITER ',' CSV HEADER"
psql -c "\copy employees from 'data/employees.csv' DELIMITER ',' CSV HEADER"
```

## Running a SQL File

If postgres is running, you can run SQL files using:

```console
psql -f sql/rank_employees.sql
```

## References

Employee sample data modified from [Sling Academy](https://www.slingacademy.com/article/employees-sample-data/)

[Window functions cheat sheet](https://learnsql.com/blog/sql-window-functions-cheat-sheet/)
