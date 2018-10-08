from fabric.api import run
from fabric.context_managers import settings, shell_env

# TODO: Change the host to put the direction
def _get_manage_dot_py(project_name):
    return f'~/sites/{project_name}/venv/bin/python ~/sites/{project_name}/manage.py'

def reset_database(project_name, staging_server):
    manage_dot_py = _get_manage_dot_py(project_name)
    if staging_server.ssh_port:
        with settings(
            host_string=f'vagrant@{staging_server.server}:{staging_server.ssh_port}',
            private_key_filename=staging_server.ssh_private_key
            ):
            run(f'{manage_dot_py} flush --noinput')
    else:
        with settings(host_string=f'vagrant@{staging_server.server}'):
            run(f'{manage_dot_py} flush --noinput')

def _get_server_env_vars(project_name):
    env_lines = run(f"grep -v '^#' ~/sites/{project_name}/.env").splitlines()
    return dict(l.split('=') for l in env_lines if l)

def _create_session_on_server(project_name, email):
    manage_dot_py = _get_manage_dot_py(project_name)
    env_vars = _get_server_env_vars(project_name)
    with shell_env(**env_vars):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()

def create_session_on_server(staging_server, project_name, email):
    if staging_server.ssh_port:
        with settings(
        host_string=f'vagrant@{staging_server.server}:{staging_server.ssh_port}',
        private_key_filename=staging_server.ssh_private_key
        ):
            return _create_session_on_server(project_name, email)
    else:
        with settings(host_string=f'vagrant@{staging_server.server}'):
            return _create_session_on_server(project_name, email)
