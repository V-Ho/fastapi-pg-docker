## Free Code Camp Python API course
https://www.youtube.com/watch?v=0sOvCWFmrtA

## Postgres DB

Run in docker
- uses the official docker postgres 13 image
- uses a named volume, my_dbdata, to store postgres data 
- -v /Users/[your_username]/Develop/postgres_data/13.2:
/var/lib/postgresql/data will bind that data folder inside the container volume (/var/lib/postgresql) to the local folder you created on your laptop in the previous step, so that data will persist if the container gets shut down and restarted for any reason.
- exposes port 54320 to the host using -p, binds postgres port of container to local machine port
- sets the container name to fcc_postgres
- uses the -d flag to run in the background
- sets the postgres superuser password to "pass_123" using -e and the POSTGRES_PASSWORD environment variable
```
docker run -d --name fcc_postgres -v my_dbdata:/var/lib/postgresql/data -p 54320:5432 -e POSTGRES_PASSWORD=pass_123 postgres:13

Open pgadmin UI http://localhost:5050/browser/
host: from  $docker inspect <postgres_container_id> | grep IPAddress
username: root
password: root

https://www.saltycrane.com/blog/2019/01/how-run-postgresql-docker-mac-local-development/

https://towardsdatascience.com/how-to-run-postgresql-and-pgadmin-using-docker-3a6a8ae918b5