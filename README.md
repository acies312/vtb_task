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
    Так же работу скрипта в keepalived, для проверки работы haproxy, не удалось продемонстрировать используя docker, т.к. haproxy имел PPID=1, что мешало выключить его и проинформировать скрипт, что haproxy больше не запущен (скрипт проверял pgrep haproxy)
    
    </aside>
    
    ![восстановление работы loadbalancer1](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%206.png)
    
    восстановление работы loadbalancer1
    
    **Задание 2.2(усложненное)**
    
    Написать роль на Ansible по развёртыванию стенда из Задание 2.1. Должен быть описан файл инвентори с серверами по примеру:
    
    ```
    [loadbalancers]
    ha1 ansible_host=10.10.1.1
    ha2 ansible_host=10.10.1.2
    [webservers]
    web1 ansible_host=10.10.1.1
    web2 ansible_host=10.10.1.2
    ```
    
    Можно написать 1 большую роль, либо 3 роли и потом вызвать их поочёрдно.
    Роль Nginx – устанавливает и конфигурирует Nginx на группе хостов [webservers].
    Роль HA Proxy – устанавливает и конфигурирует HA Proxy на группе хостов [loadbalancers].
    Роль Keepalived – устанавливает и конфигурирует Keepalived на группе хостов [loadbalancers].
    Конфиги nginx, HA proxy, keepalived оформить, используя шаблоны Jinja2(язык шаблонов).
    Пример использования шаблонов Jinja2:
    В каталоге /roles/nginx/templates создаётся конфиг nginx.conf, далее в роле мы используем данный конфиг
    
    ```yaml
    name: Add nginx config
    template:
    	src=template/nginx.conf
    	dest=/etc/nginx/nginx.conf
    ```
    
    Итоговый playbook объединяющий три роли может выглядеть следующим образом.
    
    ```yaml
    hosts: webservers
    become: yes
    roles:
    nginx
    hosts: loadbalancers
    become: yes
    roles:
    ha-proxy
    hosts: loadbalancers
    become: yes
    roles:
    keepalived
    ```
    
    Запуск итогового playbook примерно выглядит так
    Ansible-playbook –i <inventory_file> nginx_haproxy_ha.yml
    
    <aside>
    💬 здесь для определения в конфиге для keepalived в инветори файле у хостов определены соответствующие переменные.
    
    </aside>
    
    ![подготовленные файлы ansible](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/Untitled%207.png)
    
    подготовленные файлы ansible
    
    ![корректно отработанный playbook](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/%25D1%2580%25D0%25B0%25D0%25B1%25D0%25BE%25D1%2582%25D0%25B0_%25D0%25BF%25D0%25BB%25D0%25B5%25D0%25B9%25D0%25B1%25D1%2583%25D0%25BA%25D0%25B0.png)
    
    корректно отработанный playbook
    
    <aside>
    💬 Ниже представлена балансировка roundrobin на haproxy через виртуальный ip, определенный для keepalived
    
    </aside>
    
    ![работа балансировки HAproxy](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/%25D1%2580%25D0%25B0%25D0%25B1%25D0%25BE%25D1%2582%25D0%25B0_haproxy_%25D0%25BD%25D0%25B0_%25D0%25B2%25D0%25B8%25D1%2580%25D1%2582%25D1%2583%25D0%25B0%25D0%25BB%25D1%258C%25D0%25BD%25D0%25BE%25D0%25BC_ip.png)
    
    работа балансировки HAproxy
    
    <aside>
    💬 слева BACKUP сервер, а справа MASTER сервер. на данном скриншоте состояние всех узлов нормальное
    
    </aside>
    
    ![нормальная работа keepalived](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/%25D1%2580%25D0%25B0%25D0%25B1%25D0%25BE%25D1%2582%25D0%25B0_keepalived_%25D1%2581%25D1%2582%25D0%25B0%25D1%2580%25D1%2582%25D0%25BE%25D0%25B2%25D0%25BE_%25D1%2581%25D0%25BE%25D1%2581%25D1%2582%25D0%25BE%25D1%258F%25D0%25BD%25D0%25B8%25D0%25B5.png)
    
    нормальная работа keepalived
    
    <aside>
    💬 После остановки HAproxy на MASTER сервере роль MASTER взял на себя второй узел - скрипт отработал, keepalived отработал.
    
    </aside>
    
    ![остановка HAproxy на MASTER узле](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/keepalive_%25D0%25BF%25D0%25BE%25D1%2581%25D0%25BB%25D0%25B5_%25D0%25BE%25D1%2582%25D1%2581%25D0%25B0%25D0%25BD%25D0%25BE%25D0%25B2%25D0%25BA%25D0%25B8_%25D1%2585%25D0%25B0%25D0%25BF%25D1%2580%25D0%25BE%25D0%25BA%25D1%2581%25D0%25B8.png)
    
    остановка HAproxy на MASTER узле
    
    <aside>
    💬 После восстановления работы HAproxy на первом узле роль MASTER вернулась ему, а второй узел перешел в BACKUP роль.
    
    </aside>
    
    ![восстановление сервиса HAproxy на первом узле](%D0%BE%D1%82%D1%87%D0%B5%D1%82%20ebcf9f0275e343adabb1d3cd4fb8a1a1/%25D0%25B2%25D0%25B5%25D1%2580%25D0%25BD%25D1%2583%25D0%25BB_%25D1%2585%25D0%25B0%25D0%25BF%25D1%2580%25D0%25BE%25D0%25BA%25D1%2581%25D0%25B8.png)
    
    восстановление сервиса HAproxy на первом узле
