# Termister

Оболочка над ssh. Позволяет в конфигурационных файлах сохранить списки и параметры серверов,
разбитые на группы.

**Почему?** Не нашел на маке нормального бесплатного эмулятора терминала с возможностью сохранения
параметров соединений к ssh серверам. Наваять полноценную программу для мак я не смогу, знаний
нет. Как вариант использовать java... Решил не извращаться и написать оболочку для командной
строки.

## Команды
### list

Получение списка серверов.

```shell
./termister.py list
```

На экране получим что то типа:

```
moon    Moon servers
        Host: 192.168.10.5      Port: 22        User: root      Server for test 1
        Host: 192.168.10.8      Port: 22        User: root      Server for test 2
romb    Romb servers
        Host: 192.168.11.17     Port: 22        User: root      Server for test 3
        Host: 192.168.11.18     Port: 12332     User: root      Server for test 4
solar   Solar servers
        Host: 192.168.0.134     Port: 22        User: artur     Solar system
        Host: 192.168.0.8       Port: 22        User: root      Solar system  2
Beta    Beta servers
        Host: 192.168.0.17      Port: 22        User: root      Server for test 3
        Host: 192.168.0.18      Port: 12332     User: root      Server for test 4
```

В качестве дополнительного параметра можно указать регулярное выражение для поиска в именах хостов.

```bash
./termister.py list 192.168.10
```

На стандартном выводе:

```
moon    Moon servers
        Host: 192.168.10.5      Server for test 1       Port: 22        User: root
        Host: 192.168.10.8      Server for test 2       Port: 22        User: root
romb    Romb servers
solar   Solar servers
Beta    Beta servers
```

Параметр `-g group_name` ограничивает вывод списка серверов из одной группы.

```bash
./termister.py list -g moon
```

```
moon    Moon servers
        Host: 192.168.10.5      Server for test 1       Port: 22        User: root
        Host: 192.168.10.8      Server for test 2       Port: 22        User: root
```

### host

Подключение к серверу:

```shell
./termister.py host 192.168.11.18
```

Остальные параметры подключения будут взяты из конфигурационного файла.

## Config files

Расположение основного конфигурационного файла определяется параметром `-c` или `--configfile`.
Если параметр не определён, смотрится содержимое переменной среды окружения `TER_CONF`.
Если переменная не определена, используется значение по умолчанию `/etc/termister/termister.yaml`.

Формат файла:

```yaml
configDirectory: conf.d
```

* **configDirectory** - директория, в которой будут располагаться файлы содержащие описание серверов, к которым 
  будет происходить подключение.

###  Список серверов

Формат файла, в котором находится список (списки) серверов.

 ```yaml
 ---
description: For any case
group:
- solar:
    description: "solar servers"
    hosts:
    - host: 192.168.0.5
      port: 22
      user: root
      description: Server for test 1 on te solar group
    - host: 192.168.0.8
      port: 22
      user: root
      description: Server for test 2
- moon:
    description: "moon servers"
    hosts:
    - host: moon.server.net
      port: 22
      user: root
      description: Server for test 3 on the moon group
    - host: pluto.server.net
      port: 22
      user: root
      description: Server for test 4
 ```

## Дополнительные библиотеки

Для работы программы необходим Python3 и пара библиотек из файла `requirements.txt`.

```shell
pip3 install -r requirements.txt
```
