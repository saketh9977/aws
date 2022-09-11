create external table if not exists data_hydra_46(
    `location_collection_method` string,
    `device_id` string,
    `ip_address` string,
    `device_os` string,
    `country_code` string,
    `latitude` float,
    `longitude` float,
    `horizontal_accuracy` float,
    `timestamp` bigint,
    `geohash` string
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
location 's3://quadrant-ftest2/saketh/in/'
TBLPROPERTIES ("skip.header.line.count"="1");