##Отчет

1. Запускаем контейнер с редисом:
   
   `docker run -d --name redis1 --net redisnet -v /Users/amirkhankhisamutdinov/mipt/6th/db/redis/redis-cluster/redis1:/data -p 6379:6379 redis redis-server /data/redis.conf`

   Мы запускаем его с внутренней докер-сетью redisnet - в дальнейшем к этой сети мы подключим остальные контейнеры, чтобы образовать кластер. 
2. в репозитории лежит json, который мы сохраним. Также лежит код для сохранения этого json-а в базу.
   Результаты:
    saving json as string took 1.563175916671753s
    saving json as zset took 1.0660738945007324s
    saving json as list took 1.5780580043792725s
    saving json as hset took 2.2522518634796143s
3. скорость чтения будем тестировать через redis-benchmark:
   `redis-benchmark -t get -n 1000000`
   Получаем вывод:
   1000000 requests completed in 6.71 seconds
4. Создаем redis-кластер:
   1. Запускаем оставшиеся два контейнера:
      1. `docker run -d --name redis2 --net redisnet -v /Users/amirkhankhisamutdinov/mipt/6th/db/redis/redis-cluster/redis2:/data -p 6380:6379 redis redis-server /data/redis.conf`
      2. `docker run -d --name redis1 --net redisnet -v /Users/amirkhankhisamutdinov/mipt/6th/db/redis/redis-cluster/redis1:/data -p 6381:6379 redis redis-server /data/redis.conf`
      3. В конфиге лежат такие настройки:
   
            port 6379

            cluster-enabled yes

            cluster-config-file nodes.conf

            cluster-node-timeout 5000

            appendonly yes
   2. Они будут слушать на портах 6380 и 6381
   3. Объединяем их в кластер:
   4. `docker exec redis1 redis-cli --cluster create 172.21.0.2:6379 172.21.0.3:6380 172.21.0.4:6381 --cluster-replicas 0`
   5. Эти айпи адреса - внутренние для докер-сети redisnet.
