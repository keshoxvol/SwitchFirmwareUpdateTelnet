


import telnetlib
import time

file_of_ip = open("ip.txt", "r")
file_of_error_ip = open("ip_error.txt", "w")
file_of_error_ip_step_2 = open("ip_error_step_2.txt", "w")
file_win_ip = open("ip_win.txt", "w")

file_of_error_ip_step_2.close()
file_of_error_ip.close()
file_win_ip.close()
name_file = ""



successfully_authorization = str(b'****\r\n\r\r\n\r\nconsole#')
successfully_authorization1 = "#'"



def pars_config():
    iter_pars_conf = 0
    global name_file, delay, ip_tftp, username, password, time_sleep_download
    file_conf = open("config.txt")

    while iter_pars_conf < 9:
        str_conf = file_conf.readline()

        if "\n" in str_conf:
            str_conf = str_conf.replace("\n", "")
        if " " in str_conf:
            str_conf = str_conf.replace(" ", "")

        if str_conf.rfind("username") == 0:
            x, username = str_conf.split("=")
        elif str_conf.rfind("password") == 0:
            x, password = str_conf.split("=")
        elif str_conf.rfind("delay") == 0:
            x, delay = str_conf.split("=")
            delay = float(delay)
        elif str_conf.rfind("ip_tftp") == 0:
            x, ip_tftp = str_conf.split("=")
        elif str_conf.rfind("name_file") == 0:
            x, name_file = str_conf.split("=")
        elif str_conf.rfind("time_sleep_download") == 0:
            x, time_sleep_download = str_conf.split("=")



        iter_pars_conf += 1



def tellnet(ip_adress):
    global tel
    tel = telnetlib.Telnet(ip_adress, port=23)

def authorization():
    tel.read_until(b"User Name:", timeout=1)
    tel.write(username.encode("ascii") + b"\n")
    tel.read_until(b"Password:", timeout=1)
    tel.write(password.encode("ascii") + b"\n")
    time.sleep(1)


def send_command(command):
    if command == "enable":

        enable = "enable"
        tel.write(enable.encode("ascii") + b"\n")

    elif command == "configure":

        configure = "configure"
        tel.write(configure.encode("ascii") + b"\n")

    elif command == "boot system inactive-image":

        boot_sys_inact = "boot system inactive-image"
        tel.write(boot_sys_inact.encode("ascii") + b"\n")

    elif command == "show bootvar":

        sh_bootvar = "show bootvar"
        tel.write(sh_bootvar.encode("ascii") + b"\n")

    elif command == "write":

        vwriter = "write"
        tel.write(vwriter.encode("ascii") + b"\n")

    elif command == "y":

        yes = "y"
        tel.write(yes.encode("ascii") + b"\n")

    elif command == "reload":

        reload = "reload"
        tel.write(reload.encode("ascii") + b"\n")

    elif command == "show version":

        sh_version = "show version"
        tel.write(sh_version.encode("ascii") + b"\n")


def copy_from_tftp(ip_tftp, name_file):

    copy_file_of_tftp = "copy tftp://" + ip_tftp + "/" + name_file + " image"
    tel.write(copy_file_of_tftp.encode("ascii") + b"\n")


def main():
    pars_config()

    while True:
        ip_adress = file_of_ip.readline()
        if ip_adress == "":
            print("\n---------\n")
            break

        if "\n" in ip_adress:
            ip_adress = ip_adress.replace("\n", "")

        print("\n---------\n" + "\nРабота с " + ip_adress)
        try:
            tellnet(ip_adress)
        except:
            print("Коммутатор недоступен")
            file_of_error_ip = open("ip_error.txt", "a")
            file_of_error_ip.write(ip_adress + ": Коммутатор недоступен\n")
            file_of_error_ip.close()
            continue
        authorization()
        time.sleep(delay)
        returned = str(tel.read_very_eager()) #смотрим что вернет комод после строки с паролем

        if returned.endswith(successfully_authorization1) == False: #!= successfully_authorization:
            print("Ошибка авторизации")
            file_of_error_ip = open("ip_error.txt", "a")
            file_of_error_ip.write(ip_adress + "Ошибка авторизации")
            file_of_error_ip.close()
            continue
        elif returned.endswith(successfully_authorization1) == True: #== successfully_authorization:
            print("Успешная авторизация")
            file_win_ip = open("ip_win.txt", "a")
            file_win_ip.write(ip_adress + "\n")
            file_win_ip.close()


        send_command("enable")
        time.sleep(delay)
        print("Скачивание прошивки")
        copy_from_tftp(ip_tftp, name_file)
        time.sleep(int(time_sleep_download))
        returned = str(tel.read_very_eager())
        x, returned = returned.split("#")
        print(returned)
    input("Продолжить?   Если прошивка еще не скачалась на коммутатор, то будет ошибка")
    file_win_ip = open("ip_win.txt", "r")


    while True:
        ip_adress = file_win_ip.readline()
        if ip_adress == "":
            break

        if "\n" in ip_adress:
            ip_adress = ip_adress.replace("\n", "")
        print("\nРабота с " + ip_adress + "\n")
        try:
            tellnet(ip_adress)
        except:
            print("Что то пошло не так")
            file_of_error_ip_step_2 = open("ip_error_step_2.txt", "a")
            file_of_error_ip_step_2.write(ip_adress + ": Коммутатор недоступен\n")
            continue
        authorization()
        time.sleep(delay)
        returned = str(tel.read_very_eager())  # смотрим что вернет комод после строки с паролем

        if returned.endswith(successfully_authorization1) == False: #!= successfully_authorization:
            print("Ошибка авторизации")
            file_of_error_ip = open("ip_error_step_2.txt", "a")
            file_of_error_ip.write(ip_adress + "Ошибка авторизации")
            file_of_error_ip.close()
            continue
        elif returned.endswith(successfully_authorization1) == True: #== successfully_authorization:
            print("Успешная авторизация")

        send_command("enable")
        time.sleep(delay)
        send_command("boot system inactive-image")
        print("Поставлена загрузка с неактивного образа")
        time.sleep(delay)
        send_command("show bootvar")
        time.sleep(delay)
        returned = str(tel.read_very_eager())

        if "\n" in returned:
            returned = returned.replace("\n", "")
        if " " in returned:
            returned = returned.replace(" ", "")
        if "-" in returned:
            returned = returned.replace("-", "")
        n_letter_1image = returned.find("1image")
        returned = returned[n_letter_1image:]
        print(returned)

        input("Продолжить?")

        send_command("write")
        time.sleep(delay)
        send_command("y")
        time.sleep(delay)
        tel.read_until(b"Copy succeeded")
        print("Настройки сохранены")
        time.sleep(delay)
        send_command("reload")
        time.sleep(delay)
        send_command("y")
        print("Отправлено в перезагрузку")


    file_win_ip.close()




main()
input("Нажмите Enter")

