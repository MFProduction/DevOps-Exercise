# DevOps Exercise
## Docker compose
For demonstration use docker-compose if installed. By deafult it runs the (1) production task with --verbose option.
From root directory run:
```bash
docker-compose up --build
```
container:
image: postgres:9.5, name: postgres
image: devopsexercise_api_service_tools, name api_service_tools

##  Manual setup
### Database
 initial script: init-db/init-data-db.sh
#### ENVS
* POSTGRES_USER
* POSTGRES_PASSWORD
#### Setup and running
run demo database container:
```bash
docker run -p 5432:5432 --name postgres -v $PWD/db-init:/docker-entrypoint-initdb.d -e POSTGRES_USER=psql -e POSTGRES_PASSWORD=totallylongandsavepassword -d postgres:9.5
```
### API service tools
#### ENVS
* DB_HOST eg. 192.168.1.4 (demo psql runs on host ip)
* DB_PASSWORD
* DB_USER

#### Setup and running
build api service tools container:
consistent with docker-compose:
```bash
docker build -t devopsexercise_api_service_tools .
```
or standalone:
```bash
docker build -t api_service_tools .
```
run api service tools container
```bash
docker run -ti -e DB_HOST=192.168.1.101 -e DB_USER=psql -e DB_PASSWORD=totallylongandsavepassword api_service_tools
```
#### Usage
* -v --verbose:    show updated outputs (dafault flag)
* -d --dry_run:    only check for missing hours and returns the total number of missing hours in database
* -s --start_date: set start date (01-10-2016)
* -e --end_date:   set_end date   (01-10-2016)
* -h
* test: run testing task (2a)
```bash
docker run -ti -e DB_HOST=192.168.1.101 -e DB_USER=psql -e DB_PASSWORD=totallylongandsavepassword api-service-tools test


To test if database tables are really full for all hours between 2016-10-01 00:00 and 2016-10-13 23:00 (2b)run:
```bash
docker run -ti -e DB_HOST=192.168.1.101 -e DB_USER=psql -e DB_PASSWORD=totallylongandsavepassword api_service_tools --dry_run --start_date 01-10-2016 --end_date 13-10-2016
