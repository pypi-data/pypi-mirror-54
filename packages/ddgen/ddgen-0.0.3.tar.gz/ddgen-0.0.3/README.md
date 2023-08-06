# ddgen
Library of Python utilities that I needed so many times in the past


## Select RefSeq transcript with the highest priority

RefSeq transcripts have following categories: 
- `NM_`, `XM_`, `NR_`, `XR_`

If we have transcripts from multiple sources, we want to select the one coming from the source with highest priority.
> E.g. `NM_` has higher priority than `XM_`.

If we have multiple transcripts from a single source, we want to select the one with smaller integer.
> E.g. `NM_123.4` has higher priority than `NM_124.4`.

```python
from ddgen.utils import txs

# tx will be `NM_123.4`
tx = txs.prioritize_refseq_transcripts(['NM_123.4', 'NM_124.4', 'XM_100.1'])
```

## Connect to H2 database

The H2 database is a pure Java SQL database, hence it is primarily meant to be used with Java.
We can connect to the database from Python, if:

- Java is installed on the local machine
- the local machine runs UNIX-like OS (sorry, Windows users)

In that case:
```python
from ddgen.db import H2DbManager

with H2DbManager("path/to/sv_database.mv.db", 
                 user="sa", 
                 password="sa") as h2:
    with h2.get_connection() as conn:
        with conn.cursor() as cur:
            # do whatever you want
            cur.execute('SELECT * FROM PBGA.CLINGEN_TRIPLOSENSITIVITY;')
            for i, x in zip(range(5), cur.fetchall()):
                # print first 5 lines 
                print(x)
```
