#Redis Labs (formerly Garantia Data) CSV memcached populator
This utility populates a memcached server from the keys, values and metadata available in Redis Labs exported CSV files.

#CSV file format
Each row in the CSV represents a single key-value pair. The CSV has 4 columns in the following order:

1. Key - C style encoded string
2. Value - C style encoded string
3. Flags - the memcached flags value for this key - a hexadecimal integer.
4. Expiry time - either 0 for no expiry or the unixtime expiry value - an unsigned decimal integer.

Example of a line in the CSV:
```
key_name,some text including some binary data:\xff\x00,1F,292161600
```
Note that if the key or value include any commas, forward slashes or non printable chars they need to be escaped.

[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/c14e0491029f2718c7050da355f93164 "githalytics.com")](http://githalytics.com/RedisLabs/memcache_populator)
