# **Documentation File for ELK Stack Assignment**

### Explanation Video
Watch the explanation video here:  [Explanation Video](https://drive.google.com/file/d/1x5PsIuJY_tG-2mtxuQiIVzL7utYFjvmc/view?usp=drive_link)

### *Docker Setup*

### 1. Create a New Docker Network
To create a new Docker network named `elastic`, run the following command:
    
```bash
    docker network create elastic
```

To pull elastic and kibana Docker images, run the following command:
    
```bash
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.17.0
    
    docker pull docker.elastic.co/kibana/kibana:8.17.0
```

To run elastic and kibana Docker containers, run the following command:
    
```bash
    docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.17.0
    
    docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.17.0
```

To make sure elastic and kibana Docker containers running, run the following command:
    
```bash
    docker ps
```

### *Elastic and Kibana Setup*

### 2. Create a New Password and Enrollment key

To change elastic and kibana passwords and enrollment key, run the following command:
    
```bash
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
    docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    export ELASTIC_PASSWORD="your_password"
    docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
```

To make sure elastic is working properly, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
```

### *Elastic and Kibana Setup*

### 3. Create a New Index and Ingest Json Data

To create the index, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD -X PUT https://localhost:9200/annotate_pics_flattened -H "Content-Type: application/json" -d '{"mappings":{"properties":{"filename":{"type":"keyword"},"width":{"type":"integer"},"height":{"type":"integer"},"class":{"type":"keyword"},"xmin":{"type":"integer"},"ymin":{"type":"integer"},"xmax":{"type":"integer"},"ymax":{"type":"integer"},"date":{"type":"date","format":"yyyy-MM-dd"},"year":{"type":"integer"},"month":{"type":"integer"},"day":{"type":"integer"}}}}'
```
I got these fields from roboflow file and then added date, year, month and day to help me in creating more powerful visuals. Also, the data types depends on the input type if it is numeric then integer else keyword.


To check the index's health, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:wDpKP3SI8GuK1=aIOsqA -X GET "https://localhost:9200/_cat/indices?v"
```

To make the index's health green, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:wDpKP3SI8GuK1=aIOsqA -X PUT "https://localhost:9200/annotate_pics_flattened/_settings" -H "Content-Type: application/json" -d '{
  "index": {
    "number_of_replicas": 0
        }
    }'
```


To bulk ingest the index, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD -X POST https://localhost:9200/annotate_pics_flattened/_bulk -H "Content-Type: application/json" --data-binary @flattened.json
```
I inserted the data after getting the csv from roboflow then converted it to the json structure, but this structre can't work with indexes of elastic search it has to be modified. I wrote a script to modify it and added date, month, year, and day to help in creating insightful visuals.

To make sure the date ingest properly in the index, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:wDpKP3SI8GuK1=aIOsqA -X GET "https://localhost:9200/annotate_pics_flattened/_count"
```


To make show samples of the date ingested in the index, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:wDpKP3SI8GuK1=aIOsqA -X GET "https://localhost:9200/annotate_pics_flattened/_search?pretty="true""
```

To delete the index, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:wDpKP3SI8GuK1=aIOsqA -X DELETE "https://localhost:9200/annotate_pics_flattened"
```


To delete the index's docs, run the following command:
    
```bash
    curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD -X POST "https://localhost:9200/annotate_pics_flattened/_delete_by_query" -H "Content-Type: application/json" -d'
    {
    "query": {
        "match_all": {}
        }
    }'
```

The queries main purpose is to  help in creating the index and makeing sure that it aligns with the data that will be ingested. The queries differs from each other, one delete the index, the other delete the docs if there was a mistake and the other check the index health and showcase some of it's content and count.

To enter the kibana, run the following command in the browser:
    
```bash
    localhost:5601
```

I tried to visualize the classes because they are the main part. Also, I created some visuals that depends on the images and it's frequency per week over the time constructed. The visuals was class distribution, label frequency and each of them were made per month too, I made a trends over time and the number of files per year, month and day.

They are relvant because it showcases some hidden pattern in the labeled data and make a small amount of images insightful and meaningful, imagine have much more data to play with and more fields to asscocaite.
