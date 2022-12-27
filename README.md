# Termister

Оболочка над ssh. Позволяет в конфигурационныйх файлах сохранить списки и параметры серверов,
разбитые на группы.

**Почему?** Не нашел на маке нормального бесплатного эмулятора терминала с возможностью сохранения
параметров соединений к ssh серверам. Наваять полноценную программу для мак я не смогу, знаний
нет. Как вариант использовать java... Решил не извращаться и написать оболочку для командной
строкию.

Получение списка серверов:

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

Подключение к серверу:

```shell
./termister.py host 192.168.11.18
```

Остальные параметры подключения будут взяты из конфигурационного файла.

Для работы программы необходим Python3 и пара библиотек из файла `requirements.txt`.

```shell
pip3 install -r requirements.txt
```

## Config files

Расположение основного конфигурационного файла определяется параметром `-c` или `--configfile`.
Если параметр не определён, смотрится содержимое переменной среды окружения `TER_CONF`.
Если переменная не определена, используется значение по умолчаниб `/etc/termister/termister.yaml`.

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
organization: My organization
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
    - host: 192.168.0.17
      port: 22
      user: root
      description: Server for test 3 on the moon group
    - host: 192.168.0.18
      port: 22
      user: root
      description: Server for test 4
 ```