# Setup the docker file

1. Run Python Image (any version you need)
2. Install the packages as needed (eg: Pandas)
3. Set your working directory (eg: /app) and copy the pipeline file
4. Set up an entry-point for taking in arguments (eg: ENTRYPOINT [ "python", "pipeline.py" ])

# Pipeline Basic
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

```docker
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
(List of ports)
```
sudo lsof -i :5432 
sudo kill -9 <process_id>
```

# Download the data

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
