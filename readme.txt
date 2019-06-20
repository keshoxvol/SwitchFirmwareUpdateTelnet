The program updates the firmware at Eltex switches

Run the file "" only in the folder with all the .txt files listed below.
config.txt - startup configuration file
ip.txt - file with initial ip addresses
ip_error.txt - file with ip addresses, during connection with which an error occurred during the firmware download step
ip_error_step_2.txt - the file with ip addresses, during connection with which an error occurred during the update step
ip_win.txt - file with ip addresses, access to which did not encounter errors in the first step

Startup procedure:
fill in the ip.txt file with ip addresses requiring updates
fill in the file config.txt
put the firmware in the directory / Tftpd64 / sys
run tftpd64
select the directory with the firmware file
run the switch.exe file


Программа обновляет прошивки у коммутаторов Eltex

Запускать файл "" только в папке со всеми .txt файлами, перечислеными ниже
config.txt - файл с конфигурацией запуска
ip.txt - файл с начальными ip адресами
ip_error.txt - файл с ip адресами, при соединении с которыми возникла ошибка на шаге скачивания прошивки
ip_error_step_2.txt - файл с ip адресами, при соединении с которыми возникла ошибка на шаге обновления
ip_win.txt - файл с ip адресами , при доступе к которыми не возникло ошибок на первом шаге

Процедура запуска:
заполнить файл ip.txt ip адресами требующими обновления
заполнить файл config.txt
положить прошивку в дирректорию /Tftpd64/sys
запустить tftpd64
выбрать директорию с файлом прошивки
запустить файл switch.exe


