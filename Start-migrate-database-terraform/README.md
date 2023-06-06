# Data engineering project for database migration

When playing the project, remember the following things:

Run the following commands in our project directory.

```shell
# Local run & test
make up 
make ci # Runs auto formatting, lint checks, & all the test files under ./tests


make tf-init 
make infra-up 

make cloud-airflow 

make cloud-metabase 
```

**Data infrastructure**
![DE Infra](./assets/images/infra.png)


Database migrations can be created as shown below.

```shell
make db-migration 
make warehouse-migration # to run the new migration on our warehouse
```

### Tear down infra

After you are done, make sure to destroy your cloud infrastructure.

```shell
make down 
make infra-down 
```
