import argparse, os, json, tempfile
 
# добавляем аргументы в нужном порядке для парсера и производим парсинг строки
parser = argparse.ArgumentParser()
parser.add_argument("--key", type=str, required=True)
parser.add_argument("--val", type=str)
args = parser.parse_args()
 
# получаем путь до файла хранения key-value значений
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

# проверяем есть ли файл
if os.path.isfile(storage_path):
    if args.val: # если был передан val аргумент
        with open(str(storage_path), "r") as f: # открываем файл на чтение
            m = json.load(f) #считываем файл в формат json
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

else:
    d = {}
    with open(str(storage_path), "w") as f:
        if args.val:
            d = {args.key: [args.val]}
        json.dump(d, f)