import os
import shutil
from pprint import pprint

import cookiecutter

PROJECT_DIR = os.path.realpath(os.path.curdir)
SRC_DIR = os.path.join(PROJECT_DIR, "src")


def load_context():
    # noinspection PyUnresolvedReferences
    context = {
        "modules": {{cookiecutter.modules | tojson}},
        "project_slug": "{{ cookiecutter.project_slug }}",
        "include_sync_api": "{{ cookiecutter.include_sync_api }}",
        "include_async_api": "{{ cookiecutter.include_async_api }}",
    }
    return context


def replace_example_with_module(module_name):
    module_name = module_name.lower()

    layers = [
        os.path.join(SRC_DIR, "application"),
        os.path.join(SRC_DIR, "domain"),
    ]
    for layer in layers:
        example_path = os.path.join(layer, "example")
        if os.path.exists(example_path):
            target_path = os.path.join(layer, module_name)
            shutil.copytree(example_path, target_path)
            pprint(f"[+] Created {target_path}")

    presentation_v1 = os.path.join(SRC_DIR, "presentation", "api", "v1")
    example_controller = os.path.join(presentation_v1, "controllers", "healthcheck.py")
    if os.path.exists(example_controller):
        with open(example_controller) as f:
            content = f.read()
        new_controller_path = os.path.join(
            presentation_v1, "controllers", f"{module_name}.py"
        )
        with open(new_controller_path, "w") as f:
            f.write(content.replace("healthcheck", module_name))
        pprint(f"[+] Created controller: {new_controller_path}")


def remove_api_dirs(context):
    presentation_path = os.path.join(SRC_DIR, "presentation")

    if context["include_sync_api"] == "no":
        sync_api_path = os.path.join(presentation_path, "api")
        if os.path.exists(sync_api_path):
            shutil.rmtree(sync_api_path)
            pprint("[-] Removed sync API directory")

    if context["include_async_api"] == "no":
        async_api_path = os.path.join(presentation_path, "async_api")
        if os.path.exists(async_api_path):
            shutil.rmtree(async_api_path)
            pprint("[-] Removed async API directory")


def cleanup_example():
    for path in [
        os.path.join(SRC_DIR, "application", "example"),
        os.path.join(SRC_DIR, "domain", "example"),
    ]:
        if os.path.exists(path):
            shutil.rmtree(path)
            pprint(f"[-] Removed {path}")


def main():
    context = load_context()
    modules = context.get("modules", [])

    remove_api_dirs(context)

    if isinstance(modules, str):
        modules = [m.strip() for m in modules.split(",") if m.strip()]

    for module in modules:
        replace_example_with_module(module)

    cleanup_example()


if __name__ == "__main__":
    main()
