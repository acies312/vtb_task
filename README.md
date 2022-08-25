# отчет

**Задание 1.1**

- Установить VirtualBox (или VMware workstation player), разобраться как создать виртуальную машину и создать новую vm на базе дистрибутива Centos (Centos это параллельная open source ветка rhel)
    
    ![Untitled](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled.png)
    
- Подключиться к созданной vm по ssh через любой клиент.
    
    ![Untitled](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%201.png)
    
- Установить Python на созданной vm
    
    ![Untitled](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%202.png)
    
- В домашней директорий пользователя создать папку task; реализовать собственное key-values хранилище на Python. Данные будут сохраняться в файле storage.data(в формате JSON, можно использовать библиотеку tempfile, для хранения данных во временных файлах). Добавление новых данных в хранилище и получение текущих значений осуществляется с помощью утилиты командной строки storage.py. Пример работы утилиты:
    
    Сохранение данных
    
    `$ storage.py --key key_name --val value`
    
    Получение данных
    
    `$ storage.py --key key_name`
    
    Обратите внимание, что значения по одному ключу не перезаписываются, а добавляются к уже сохраненным. Другими словами - по одному ключу могут храниться несколько значений. При выводе на печать, значения выводятся в порядке их добавления в хранилище (Пример ввода "test_value,test_value2,test_value3" ). Формат вывода на печать для нескольких значений через запятую. Если значений по ключу не было найдено, выведите пустую строку или None. Сделать обработку исключений, если они будут возникать при тестировании. Скрипт должен работать в разных ОС.
    
    ![Untitled](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%203.png)
    
    ```python
    import argparse, os, jso**n, tempfile
     
    # добавляем аргумен**ты в нужном порядке для парсера и производим парсинг строки
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str, required=True)
    parser.add_argument("--val", type=str)
    args = parser.parse_args()
     
    # получаем путь до файла хранения key-value значений
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    
    # проверяем есть ли файл
    if os.path.isfile(storage_path):
        if args.val: # если был передан val аргумент
            with open(str(storage_path), "r") as f:
                m = json.load(f)
                if args.key in m: #если ключ уже записан в файле добавлем к нему переданное значени val
                    m[args.key] = m[args.key] + [args.val]
                else:
                    m.update({args.key: [args.val]})
            with open(str(storage_path), "w") as f:
                json.dump(m, f)
        # на чтение по ключу
        else:
            with open(str(storage_path), "r") as f:
                m = json.load(f)
                if args.key in m.keys():
                    if len(m[args.key]) > 1:
                        print(', '.join(m.get(args.key)))
                    else:
                        print(*m.get(args.key))
                else:
                    raise Exception('no such key in dict')
    # для инициализации файла
    else:
        d = {}
        with open(str(storage_path), "w") as f:
            if args.val:
                d = {args.key: [args.val]}
            json.dump(d, f)
    ```
**Задание 1.2 (усложненное)**

****Написать сервис API на Python к key-values хранилищу из задания 1. Самый простой фреймворк для реализации flask и дополнительный модуль flaskRESTful. Хранить данные можно так же во временных файлах в файле storage.data(в формате JSON, можно использовать библиотеку tempfile). Сервис должен уметь отвечать на запросы POST и GET. Требования к выводу можно взять из задания 1. Ниже в скриншотах есть демонстрация основных запросов и их вывода. На главной странице сервиса ‘/’ сделать описание возможностей сервиса API.

<aside>
💬 Данное задание выполнено лишь частично. API написан, но в запросах выдает ошибку. Контейнер собирается и запускается, сам сервис тоже стартует удачно.
Приложил что успел сделать.

</aside>

**Задание 2.1**

- Создать 2 WEB сервера с выводом страницы «Hello, World! \n Server 1» (аналогично для второго Server 2). Сделать балансировку нагрузки (HA + keepalived), чтобы при обновлении страницы мы попадали на любой из WEB серверов(Для балансировки можно сделать 2 отдельных сервера, в сумме 4).
    
    Будет плюсом использование Docker.
    
    ![работа HAproxy](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%204.png)
    
    работа HAproxy
    
    <aside>
    💬 *Здесь в левом окне браузера видно, что после остановки первого loadbalancer’а показывает уже интерфейс статистики со второго инстанса loadbalancer2*
    
    </aside>
    
    ![Работа Keepalived](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%205.png)
    
    Работа Keepalived
    
    <aside>
    💬 после возвращения в работу первого балансировщика он получил виртуальный ip и продолжил работу как MASTER узел keepalived. 
    Однако при повторном старте контейнера приходилось вручную запускать сервис keepalived. Не удалось выяснить почему сервис не получалось запускать ни из Dockerfile, ни из скрипта переданного в ENTRYPOINT.
    Так же работа скрипта в keepalived для проверки работы haproxy не удалось продемонстрировать используя docker, т.к. haproxy имел PPID=1, что мешало выключить его проинформировать скрипт, что haproxy больше не имеет PID (скрипт проверял pgrep haproxy)
    
    </aside>
    
    ![восстановление работы loadbalancer1](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%206.png)
    
    восстановление работы loadbalancer1
