# Setup the docker file

1. Run Python Image (any version you need)
2. Install the packages as needed (eg: Pandas)
3. Set your working directory (eg: /app) and copy the pipeline file
4. Set up an entry-point for taking in arguments (eg: ENTRYPOINT [ "python", "pipeline.py" ])

# Pipeline Basic
This is where we will implement the pipeline logic (eg. ETL).

```python
# verify the pandas import
import pandas as pd
import sys

# play with arguments
filename = sys.argv[0]
date = sys.argv[1]

print(f"Hello from {filename}! on {date}")
```

# Postgres in Docker:

Setup the connection using the docker command

```bash
docker run -it \  
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ./data:/var/lib/postgresql/data \
  -p 5432:5432 \
postgres:13
```

**Note:**
If you have run Postgres before, the same ports might not be available. Kill them first with this cmds:

```bash
sudo lsof -i :5432 
sudo kill -9 <process_id>
```

1. The first command lists all the active port listening and find the active process_id(pid)
2. Use the later command to kill/delete the process.

# Download the data

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

# Follow the Jupyter Notebook

[workwithDB Notebook](https://github.com/being-invincible/Intro-to-docker-and-postgres/blob/main/workwithDB.ipynb)

# Setup PgAdmin Client

You can visit this website to find the PgAdmin image from the Docker.
[PgAdmin Docker Container](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html)

You have to provide a few connection details as shown below to make it work!

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

Head to http://localhost:8080/

![PgAdmin Client](https://github.com/user-attachments/assets/a496a9f1-2fac-47b2-b5dd-c9f3083f205a)

But there is a small problem, we won't be able to connect the client with the local database. For this purpose, we need to create a docker network for them to communicate. You can find more about it here - [Docker Networking](https://docs.docker.com/engine/network/).

Let us create a new network using the following command:
```bash
docker network create pg-network
```

After creating the network, link it with the database by specifying the network and the name. Run the Postgres image in the network.
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ./data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```
**NOTE:** No spaces after the "\"

Now run the pgAdmin Client in the same network created above (pg-network).
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

Once, you have completed the ingestion script with arguments in a Python file. Test the script by passing arguments into it.
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
```
```bash
python ingestData.py
--user=root
--password=root \
--host=localhost \
--port=5432\
--db=ny_taxi \
--table_name=green_taxi_data \
--url=${URL}
```
