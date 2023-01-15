#! python3

import glob
import os
import platform
import re
import sys

import ruamel.yaml

"""
termister v0.0.3
"""

conf_file = "/etc/termister/termister.yaml"


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
        self.hosts: list(THost) = []

    def __iter__(self):
        for each in self.__dict__.values():
            yield each


def print_host(host: THost):
    print(f"\t{Bcolors.OKGREEN}Host: {Bcolors.ENDC}"
          + host.host
          + f"\t{Bcolors.OKBLUE}"
          + host.description
          + f"{Bcolors.ENDC}"
          + f"\t{Bcolors.OKGREEN}Port: {Bcolors.ENDC}"
          + str(host.port)
          + f"\t{Bcolors.OKGREEN}User: {Bcolors.ENDC}"
          + str(host.user))


class Termister:
    """main class"""

    def __init__(self, config_file):
        super().__init__()
        self.config_file = config_file
        self.config_dir = ""
        self.groups: list(TGroup) = []
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

    def print_group(self, group: TGroup):
        print(f"{Bcolors.HEADER} {group.name} \t {group.description}{Bcolors.ENDC}")

    def print_host(self, host: THost):
        print(f"\t{Bcolors.OKGREEN}Host: {Bcolors.ENDC}"
              + host.host
              + f"\t{Bcolors.OKBLUE}"
              + host.description
              + f"{Bcolors.ENDC}"
              + f"\t{Bcolors.OKGREEN}Port: {Bcolors.ENDC}"
              + str(host.port)
              + f"\t{Bcolors.OKGREEN}User: {Bcolors.ENDC}"
              + str(host.user))

    def list(self, list_groups: list):
        """
        Выводим на экран список хостов разделённый по группам

        Parameters:
            list_groups - список групп, хосты которых необходимо показывать.
            Если он пустой, показываем все группы
        """
        # Перебираем список групп, загруженных из конфиг файла
        for group in self.groups:
            # Учитываем название группы при поиске
            if len(list_groups) != 0:
                if group.name not in list_groups:
                    continue
            self.print_group(group)
            for host in group.hosts:
                self.print_host(host)

    def search(self, f_host):
        """
        Поиск хоста в группах по полному и неполному имени или IP адресу

         Parameters:
             host - имя, IP адрес или их часть.

        """
        for group in self.groups:
            self.print_group(group)
            for host in group.hosts:
                if host != "":
                    regexp = re.compile(str(f_host))
                    if regexp.search(host.host) is None:
                        if regexp.search(host.description) is None:
                            continue
                    self.print_host(host)

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


def usage() -> None:
    print("termister [-c config_file.yaml]\nCommands:\n\tlist|l [group ...]\n\tsearch|s regexp \n\thost_name_or_IP")



def run_app(commands: list) -> None:
    match commands:
        case ["list" | "l", *group]:
            termister = Termister(config_file=conf_file)
            termister.list(group)
        case ["search" | "s", host]:
            termister = Termister(config_file=conf_file)
            termister.search(host)
        case [host]:
            termister = Termister(config_file=conf_file)
            termister.connect_to_host(host)
        case _:
            print(f"Unknown command: {' '.join(commands)}")
            usage()


if __name__ == "__main__":
    if os.getenv("TER_CONF"):
        conf_file = os.getenv("TER_CONF")

    # Разбор параметров программы
    match sys.argv[1:]:
        case ['-c', c_file, *commands]:
            conf_file = c_file
            run_app(commands)
        case [*commands]:
            run_app(commands)
        case _:
            usage()
