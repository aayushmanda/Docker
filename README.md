## Usage

This is part of Assignment-04 for DA5402 MLOps

After starting docker daemon run the following command first in `Problem1` directory and then `Problem2` directory
```bash
docker compose up
```

You can configure "feedurl" from `Problem2_3/rss_script.py`. 

Run in Problem1 dir will result in  
* my_docker_db (Container)
* problem1-postgres (Image)

Similarly after running the command in Problem2_3 dir in
* problem2-app (Image)

You can run below commands to view the table and data in it:
```bash
docker exec -it <postgres container-id> psql -U aayus -d aayus
```

```sql
SELECT id, title, links, tags FROM rss_table;
```