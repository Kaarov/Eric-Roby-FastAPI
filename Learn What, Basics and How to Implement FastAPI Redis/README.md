
### For install redis on Mac:
```shell
brew install redis
```
#### Check redis
```shell
redis-server
```
#### To run redis CLI
```shell
redis-cli  # 127.0.0.1:6379> 
```
#### Operations
```shell
set name Eric  # OK
get name  # "Eric"
del name  # (integer) 1

exists name  # (integer) 1
exists os  # (integer) 0

keys *  # To get all keys

expire name 10  # The key name will be expired after 10 seconds
setex name 10 Eric  # For 10 seconds the name will be available
```
