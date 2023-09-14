import asyncio
import httpx
import importlib
import json
import pkgutil

from concurrent.futures import ThreadPoolExecutor
from types import ModuleType

from flask import Blueprint
from flask import Response
from flask import request

blueprint = Blueprint("holehe_blueprint", __name__)
extra_data = [
    'name',
    'emailrecovery',
    'phoneNumber',
    'others'
]


def get_functions() -> list:
    """
    Returns all the registered Holehe modules in a list
    """
    websites = []
    modules = import_submodules('holehe.modules')

    for module in modules:
        if len(module.split(".")) > 3:
            modu = modules[module]
            site = module.split(".")[-1]
            websites.append(modu.__dict__[site])

    return websites


def import_submodules(package, recursive=True) -> dict[str, ModuleType]:
    """
    Imports all the submodules from the package parameter
    """

    package = importlib.import_module(package)
    results = {}

    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)

        if recursive and is_pkg:
            results.update(import_submodules(full_name))

    return results


def create_new_event_loop_and_run(function, *params) -> None:
    """
    Creates a new event loop and runs the provided async function
    """
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(function(*params))

async def handle(loop, email) -> list[dict]:
    """
    Executes all loaded modules with the provided email address
    """

    executor = ThreadPoolExecutor(max_workers=len(functions))
    output = []

    for function in functions:
        loop.run_in_executor(executor, create_new_event_loop_and_run, function, email, httpx.AsyncClient(timeout=2), output)

    executor.shutdown(wait=True, cancel_futures=False)

    return output


# Caching to optimize performance, so functions don't have to be loaded every time
functions = get_functions()


def clean_output(data: list[dict]) -> dict[str, dict[str, str]]:
    output_data = {}

    for entry in data:
        if not entry['exists']:
            continue

        important_fields = {}

        for data_entry in entry:
            value = entry[data_entry]

            if value is not None and value is not False and data_entry in extra_data:
                important_fields[data_entry] = value

        output_data[entry['name']] = important_fields

    return output_data


@blueprint.route('/open-source/holehe')
def find_email():
    query = request.args.to_dict()

    if 'email' not in query:
        return Response(json.dumps({
            'status': 'failed',
            'message': 'Missing email parameters!'
        }))

    email = query['email']

    asyncio_loop = asyncio.new_event_loop()
    output = clean_output(asyncio_loop.run_until_complete(handle(asyncio_loop, email)))

    return json.dumps({
        'status': 'success',
        'data': output
    })

