# aio_ormsql
Simple asynchronous MySQL ORM class.

## Easy install
`pip3 install aio_ormsql`

## Required
- `pip3 install asyncio aiomysql`  
- Python 3.6+

## Example usage
1. Do imports:
```python3
from aio_ormsql import DataBase, Table, Column, WHERE
```
Where:
- `DataBase` - class for working with MySQL
- `Table` - class for creating a new table
- `Column` - class for creating a columns
- `WHERE` - class for creating where statements
2. Follow examples ans see their output:

## Examples
### Creating table
```python3
tbl = Table(
    'tests',
    Column('id', int),
    Column('tname', str)
)
```
### Connection to database
```python3
db = DataBase('admin', 'admin', 'tests')
await db.connect()
```
### Simple WHERE statement
```python3
where = WHERE(
    tbl.tname == 'admin'
)
print(where)

# Output:
# WHERE `tname`='admin'
```
### Another WHERE statement
```python3
where2 = WHERE(
    (tbl.id >= 20) | (tbl.tname == 'admin')
)
print(where2)

# Output:
# WHERE `id`>=20 OR `tname`='admin'
```
### SELECT example
```python3
statement = await db.select(
    [tbl.id, tbl.tname], where=where, table=tbl, back=True
)
print(statement)

# Output:
# SELECT DISTINCT `id`, `tname` FROM `tests` WHERE `tname`='admin'
```
### SELECT example 2
```python3
statement2 = await db.select(
    [tbl.id, tbl.tname], False, where2, table=tbl, back=True
)
print(statement2)

# Output:
# SELECT`id`, `tname` FROM `tests` WHERE `id`>=20 OR `tname`='admin'
```
### INSERT example
```python3
statement3 = await db.insert(
    {
        tbl.id: 123,
        tbl.tname: 'Johan'
    },
    tbl,
    back=True
)
print(statement3)

# Output:
# INSERT INTO `tests` (`id`, `tname`) VALUES (123, 'Johan')
```
### INSERT example 2
```python3
statement4 = await db.update(
    {
        tbl.id: '123',
        tbl.tname: 'Admin'
    },
    WHERE(tbl.tname == 'Johan'),
    tbl,
    back=True
)
print(statement4)

# Output:
# UPDATE `tests` SET `id`=123, `tname`='Admin' WHERE `tname`='Johan'
```
### Working with large DB
```python3
array = db.fetch_gen(await db.select(
    [tbl.id, tbl.tname], back=True
))

async for item in array:
    print('New pair:', item)
    # And you can see row-by-row output
```
###  Closing connection and wait for completing tasks
```python3
await db.close()
```
