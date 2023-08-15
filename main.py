from resource_creator import ResourceCreator
from definitions import definitions
rc = ResourceCreator()

def do_gen_tree():
    rc.copy_tree()

def do_backend_resources():
    rc.replace_content('apis.py')
    rc.rename_api_route('apis.py')
    rc.replace_content('business.py')
    rc.replace_content('events.py')
    rc.replace_content('forms.py')
    rc.replace_content('repos.py')
    rc.replace_content('requests.py')
    rc.replace_content('usecases.py')

def do_backend_tests():
    rc.replace_content('test_business.py')
    rc.replace_content('test_repos.py')
    rc.replace_content('test_usecases.py')

def do_core_globals():
    rc.rename_folder(f'{definitions["root_dir"]}/legacies/new_legacy/backend/core/resources')
    rc.replace_content('setup.py')
    rc.create_models()
    rc.create_entities()

def do_backend():
    do_backend_resources()
    do_backend_tests()
    do_core_globals()

def do_frontend_js():
    rc.replace_content('index.js')
    rc.replace_content('tab_name.js')
    rc.replace_content('routes.js')

def do_frontend_html():
    rc.replace_content('form.html')
    rc.replace_content('modal_audit.html')
    rc.replace_content('modal_delete.html')
    rc.replace_content('modal.html')
    rc.replace_content('tab_resources.html')
    rc.replace_content('index.html')
    # folder_name
    # tab_name

def do_frontend():
    rc.rename_folder(f'{definitions["root_dir"]}/legacies/new_legacy/backend/pabx-static/js/resources')
    do_frontend_js()
    do_frontend_html()

def do_infra():
    pass



