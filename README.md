# Termister

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