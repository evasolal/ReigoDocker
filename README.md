## Reigo
## API to get informations about addresses

## Requirements :

selenium==3.141.0 

Flask==1.1.2 

numpy==1.18.5 

regex 

sqlite3

## Running
```shell
docker build -t evaso .
docker run -v  PATH:/server -p 5000:5000 -d -t --restart always evaso
```
Then go to localhost:5000 and enter your address.

All the new entries will be saved in the database addresses.db
