**Manticore Search** - это полнотекстовый поисковой сервер с открытым исходным кодом, который используется для быстрого и эффективного поиска по большим объемам данных. Это опенсорсная, горизонтально масштабируемая база данных на основе search engine, которая была разработана продолжением Sphinx Search, и появилась в 2017 году.

# История
Как было сказано, Manticore search - продолжение Sphinx search. Прежде всего, зачем был сделан форк? В конце 2016 работа над Sphinx search была приостановлена. Пользователи, которые пользовались продуктом и поддерживали развитие проекта волновались, так как:
баги не фиксились
новые фичи, которые были давно обещаны не производились
коммуникация с командой Sphinx была затруднена.
По прошествии нескольких месяцев ситуация не поменялась и в середине июня группа инициативных опытных пользователей и клиентов поддержки Sphinx собрались, и было принято решение попытаться сохранить продукт в виде форка, под именем Manticore Search. Удалось собрать большую часть команды Sphinx (а именно тех, кто занимался непосредственно разработкой и поддержкой пользователей), привлечь инвестиции и в короткие сроки восстановить полноценную работу над проектом.
В каком-то смысле manticore search можно назвать data-mining платформой, потому что на основе больших данных можно сделать выводы о паттернах в данных: можно попробовать найти самые популярные фразы, синтаксические конструкции благодаря встроенному анализатору текстов, который поддерживает многие языки, включая русский и английский. Но основной функционал - это, конечно, поисковая база данных

# Инструменты для взаимодействия
Manticore поддерживает http-протокол MySQL, а также json over http

# Язык запросов
Все запросы пишутся на SQL

# На каком языке написана БД
Manticore search написан на C++ 

# Пример использования
1. Запускаем контейнер
   1. `docker pull manticoresearch/manticore`
   2. `docker run -d --name manticore -v /Users/amirkhankhisamutdinov/mipt/6th/db/manticore/:/data -p 9306:9306 -p 9308:9308 -p 9312:9312 manticoresearch/manticore`
2. для обращения к серверу manticore поддерживает http-протокол mysql (пока нет поддержки аутентификации, но продукт активно развивается, но поддерживается mysql ssl encription), 
3. manticore поддерживает http-протокол MySQL, поэтому подключиться к нему можно так: `mysqlb -h0 -P9306 -p` (mysql-запросы слушаются на порту 9306, аутентификация не реализована, поэтому в качестве пароля можно вводить что угодно)
4. создаем простую табличку, по которой можно искать данные
   1. `create table products(title text, price float) morphology='stem_en';`
   2. `insert into products(title,price) values ('Crossbody Bag with Tassel', 19.85), ('microfiber sheet set', 19.99), ('Pet Hair Remover Glove', 7.99);`
   3. `select id, highlight(), price from products where match('remove hair');`
   4. Даже несмотря на то, что мы ввели "remove hair", он все равно нам выведет `Pet Hair Remover Glove`, потому что мы при создании таблицы ввели `morphology='stem_en'`
   5. `update products set price=18.5 where id = 1513686608316989452;`
   6. `delete from products where price < 10;`
5. Возможно также посмотреть план запроса следующим образом:
   1. `set profiling=1; select * from hn_small where match('dog|cat') limit 0; show plan;`

# Хранение данных
## Индексы
В Manticore search есть два типа индексов - real-time index и plain index
Real-time index в Manticore Search - это индекс, который автоматически обновляется в режиме реального времени при добавлении или изменении данных в базе данных. Это позволяет пользователям мгновенно получать результаты поиска, которые включают в себя самые последние данные. Индекс real-time может использоваться, к примеру, для мониторинга социальных сетей, финансовых данных, событийных логов и так далее.
Plain index - это индекс, который создается на основе существующих данных в базе данных. Обновление индекса происходит только при выполнении явных команд пересоздания индекса. Такой индекс может использоваться для поиска в архивных данных, для которых нет необходимости в автоматическом обновлении индекса.
Их отличия можно свести к следующим пунктам:
1. Обновление: Real-time индекс обновляется автоматически в реальном времени при изменении данных в базе данных, в то время как Plain индекс требует явного пересоздания для обновления.
2. Скорость: Real-time индекс обеспечивает более быстрый доступ к самым последним данным, так как он обновляется автоматически, что делает его идеальным для использования в режиме реального времени. Plain индекс может обеспечить лучшую производительность для статических данных, так как он не требует ресурсов на автоматическое обновление.
3. Потребление ресурсов: Real-time индекс потребляет больше ресурсов, чем Plain индекс, поскольку он постоянно обновляется, что может затруднить производительность при большом объеме данных и высокой частоте изменений. Plain индекс потребляет меньше ресурсов, так как он обновляется только при явном запросе на пересоздание.
4. Поддержка: Некоторые функции, такие как изменение схемы индекса, доступны только для Plain индекса, а не для Real-time индекса.

## Способы хранить данные на серверах
Remote table и Distributed table - это два разных типа таблиц в Manticore Search, которые могут быть использованы для работы с данными, распределенными по нескольким серверам.

Remote table - это таблица, которая предоставляет доступ к данным, хранящимся на удаленном сервере через протокол MySQL. Таким образом, Remote table позволяет использовать данные, хранящиеся на других серверах, в качестве источника данных для Manticore Search. Например, можно использовать Remote table для доступа к данным, которые хранятся в MySQL или других базах данных, поддерживающих протокол MySQL.

Distributed table - это таблица, которая распределена на несколько серверов и представляет собой совокупность таблиц, хранящихся на разных серверах, объединенных в одну единую таблицу в Manticore Search. Данные на разных серверах могут быть разделены на основе хэша, диапазона или поискового запроса. Distributed table позволяет распределять нагрузку на несколько серверов и улучшать производительность запросов к большим объемам данных.

## Примеры
Создание индекса:
```
CREATE [RT] INDEX index_name
ON table_name(column_name[, column_name, ...])
[WITH (option='value'[, option='value', ...])]
```

По умолчанию используется plain index, но можно поставить RT, чтобы индекс был real-time

# Транзакции

Транзакции могут быть использованы только на таблицах с RT индексом. Чтобы начать использовать транзакции, надо поменять настройку rt_mem_limit в конфиге с 0 на ненулевое значение. Из-за этой настройки аллоцируется блок памяти для RT-indexing операций.
Транзакционность в мантикоре соответствует требованиям ACID. Любая транзакция начинается с BEGIN и заканчивается с COMMIT; Если во время транзакции что-то пошло не так, можно заиспользовать команду ROLLBACK;

Пример транзакции:
```
BEGIN;
UPDATE my_index SET my_field='new_value' WHERE my_id=123;
COMMIT;
```

# Методы восстановления
Восстановление данных в Manticore Search может быть выполнено в несколько этапов в зависимости от способа хранения данных и наличия резервных копий.

1. Создание резервной копии индекса: для начала восстановления необходимо иметь резервную копию индекса. Резервные копии могут быть созданы с помощью команды "INDEX FLUSH" или с использованием инструментов для резервного копирования.
2. Проверка целостности индекса: перед началом восстановления индекса необходимо проверить его целостность с помощью команды "INDEX VALIDATE". Эта команда проверяет, есть ли ошибки в структуре индекса, и может сообщить о проблемах, которые могут повлиять на процесс восстановления.
3. Восстановление индекса: для восстановления индекса необходимо использовать команду "INDEX REBUILD". Эта команда создает новый индекс на основе данных из резервной копии. В процессе восстановления может потребоваться временное хранилище для временных файлов, которые могут быть созданы в процессе восстановления.
4. Перезапуск службы: после восстановления данных может потребоваться перезапустить службу Manticore Search для применения изменений. Это может быть выполнено с помощью команды "searchd --stop" для остановки службы и "searchd" для ее перезапуска.

# Защита данных
На данный момент в Manticore search не поддерживается даже простая аутентификация - для доступа к базе не надо вводить логин и пароль. Для защиты от злоумышленников сейчас рекомендуется использовать сторонний middleware, но работа над этим пунктов идет, так как база активно развивается. Тем не менее, Manticore поддерживает ssl-протокол mysql для защиты данных.

# Сообщество
Manticore Search принадлежит компании Manticore Software Ltd. В ней работают многие бывшие разработчики Sphinx Search, а сама компания финансируется заинтересованными инвесторами, в том числе клиентами базы данных.