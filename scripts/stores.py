import glob
import importlib.util
import inspect
import json

import sys

def create_json(branch: str):
    from localstack.services.stores import BaseStore

    path = "localstack"

    model_files = glob.glob(path + '**/models.py', recursive=True)

    # store_name, dict
    hash_map: dict[str, dict[str, str]] = dict()

    for file in model_files:
        spec = importlib.util.spec_from_file_location("model", file)
        foo = importlib.util.module_from_spec(spec)
        sys.modules["model"] = foo
        spec.loader.exec_module(foo)
        imported_stores = [cls for cls in BaseStore.__subclasses__()]
        for store in imported_stores:
            store_name = store.__name__
            if store_name in hash_map:
                continue
            attributes = inspect.getmembers(store, lambda a: not (inspect.isroutine(a)))
            good_attrs = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
            hash_map[store_name] = {a: b.__class__.__name__ for a, b in good_attrs}

    with open(f'scripts/{branch}.json', 'w') as out_file:
        dump = json.dumps(hash_map, sort_keys=True)


if __name__ == '__main__':
    if len(sys.argv) > 0:
        branch_name = sys.argv[1]
        create_json(branch=branch_name)
