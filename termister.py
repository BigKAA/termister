#! python3

import argparse
import glob
import os
import platform
import sys
import ruamel.yaml
import re


class Bcolors:
    """Набор цветов для вывода в консоли"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class THost:
    """Параметры хостов"""

    def __init__(self, host, port, user, description):
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.description = description

    def __iter__(self):
        for each in self.__dict__.values():
            yield each

class TGroup:
    """Группы хостов"""

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description
        self.hosts :list(THost) = []

    def __iter__(self):
        for each in self.__dict__.values():
            yield each


class Termister:
    """main class"""

    def __init__(self, config_file):
        super().__init__()
        self.config_file = config_file
        self.config_dir = ""
        self.groups :list(TGroup) = []
        self.load_config()

    def load_config(self):
        """Загружаем конфигурационный файл"""
        YAML = ruamel.yaml.YAML(typ="safe")
        try:
            with open(self.config_file) as file:
                data = YAML.load(file)
                if platform.system() == "Windows":
                    self.config_dir = (
                        os.path.dirname(self.config_file)
                        + "\\"
                        + data["configDirectory"]
                        + "\\"
                    )
                else:
                    self.config_dir = (
                        os.path.dirname(self.config_file)
                        + "/"
                        + data["configDirectory"]
                        + "/"
                    )
        except FileNotFoundError:
            print("No config file:" + self.config_file + "!", file=sys.stderr)
            sys.exit(10)

        # Получаем список yaml файлов в директории
        files = glob.glob(self.config_dir + "*.yaml")

        # если в директории нет *.yml фалов, завершаем работу программы
        if len(files) == 0:
            print("No *.yaml files in " + self.config_dir, file=sys.stderr)
            sys.exit(5)

        self.fill_groups(files, YAML)

    def fill_groups(self, files, yaml):
        """Заполняем данными внутренний список групп"""
        # Читаем файлы из директории
        for file in files:
            with open(file, "r") as file2:
                data = yaml.load(file2)
                for group in data["groups"]:
                    # Названия групп (ключи словаря, первый элемент.)
                    group_name = list(dict.keys(group))[0]
                    # Создадим объект группы
                    tgroup = TGroup(group_name, group[group_name]["description"])
                    self.groups.append(tgroup)
                    for host in group[group_name]["hosts"]:
                        # Добавляем объект хоста
                        thost = THost(
                            host=host["host"],
                            port=host["port"],
                            user=host["user"],
                            description=host["description"],
                        )
                        tgroup.hosts.append(thost)

    def list(self, search_string, search_group):
        """Выводим на экран список хостов разделённый по группам"""
        for group in self.groups:
            # Учитываем название группы при поиске
            if search_group is not None:
                if search_group != group.name:
                    continue
            print(
                f"{Bcolors.HEADER}"
                + group.name
                + "\t"
                + group.description
                + f"{Bcolors.ENDC}"
            )
            for host in group.hosts:
                # Учитываем название хоста при поиске
                if search_string != "":
                    regexp = re.compile(search_string)
                    if not regexp.match(host.host):
                        continue
                print(
                    f"\t{Bcolors.OKGREEN}Host: {Bcolors.ENDC}"
                    + host.host
                    + f"\t{Bcolors.OKBLUE}"
                    + host.description
                    + f"{Bcolors.ENDC}"
                    + f"\t{Bcolors.OKGREEN}Port: {Bcolors.ENDC}"
                    + str(host.port)
                    + f"\t{Bcolors.OKGREEN}User: {Bcolors.ENDC}"
                    + str(host.user)
                )

    def find_host(self, find_host):
        """Поиск хоста в группах"""
        result = ""
        for group in self.groups:
            for host in group.hosts:
                if host.host == find_host:
                    result = host
                    break
        return result

    def connect_to_host(self, host):
        """Подключение к хосту"""
        # Ищем хост в списке
        thost = self.find_host(host)
        if not isinstance(thost, THost):
            print(f"Can't find host {host} in configs", file=sys.stderr)
        # Хост найден, пытаемся к нему подключится.

        # Формируем команду на выполнение
        runcommand = "ssh"
        if thost.port != 22:
            runcommand = runcommand + " -p " + str(thost.port)
        runcommand = runcommand + " " + thost.user + "@" + thost.host
        print("Try connect to: " + runcommand)
        os.system(runcommand)


if __name__ == "__main__":
    # Разбор параметров программы
    parser = argparse.ArgumentParser(
        description="Run ssh connetction to host from list.",
        usage="%(prog)s list [HOSTNAME_REGEXP] | host HOSTNAME [-c CONFIGFILE] [-g GROUP]",
    )
    parser.add_argument("command", nargs="*")
    parser.add_argument("-g", "--group", help="show hosts from current group")
    parser.add_argument(
        "-c",
        "--configfile",
        help='if CONFIGFILE not set, use env variable TER_CONF. If env not set< default value "/etc/termister/termister.yaml"',
    )
    # parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args(sys.argv[1:])
    # Проверяем на наличие необходимой команды
    if len(args.command) == 0:
        print('No command. Set "list" or "host HOSTNAME"', file=sys.stderr)
        sys.exit(1)
    if args.command[0] != "list" and args.command[0] != "host":
        print(
            "Incorrect command: "
            + args.command[0]
            + '\tUse "list" or "host HOSTNAME" command',
            file=sys.stderr,
        )
        sys.exit(1)

    # Set config file
    # default value is
    conf_file = "/etc/termister/termister.yaml"
    if args.configfile:
        # command line argument have 1-st priority
        conf_file = args.configfile
    elif os.getenv("TER_CONF"):
        # take file fron env variable
        conf_file = os.getenv("TER_CONF")

    # Read configs ans set list of groups and hosts
    termister = Termister(config_file=conf_file)

    # select and run command
    if args.command[0] == "list":
        if len(args.command) == 1:
            termister.list("", args.group)
        elif len(args.command) == 2:
            termister.list(args.command[1], args.group)
        else:
            print('Invalid numbers of argument command "list"', file=sys.stderr)
            sys.exit(1)

    elif args.command[0] == "host":
        if len(args.command) != 2:
            print('Invalid numbers of argument command "host"', file=sys.stderr)
            sys.exit(1)
        termister.connect_to_host(args.command[1])
