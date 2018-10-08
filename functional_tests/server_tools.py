from fabric.api import run
from fabric.context_managers import settings, shell_env

# TODO: Change the host to put the direction
def _get_manage_dot_py(host):
    return f'~/sites/{host}/venv/bin/python ~/sites/{host}/manage.py'

def reset_database(host, staging_ssh_port=None, staging_ssh_private_key=None):
    manage_dot_py = _get_manage_dot_py(host)
    if staging_ssh_port:
        with settings(
            host_string=f'vagrant@{host}:{staging_ssh_port}',
            private_key_filename=staging_ssh_private_key
            ):
            run(f'{manage_dot_py} flush --noinput')
    else:
        with settings(host_string=f'vagrant@{host}'):
            run(f'{manage_dot_py} flush --noinput')

def _get_server_env_vars(host):
    env_lines = run(f'cat ~/sites/{host}/.env').splitlines()
    return dict(l.split('=') for l in env_lines if l)

def _create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    env_vars = _get_server_env_vars(host)
    with shell_env(**env_vars):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()

def create_session_on_server(
                host, email, staging_ssh_port=None, staging_ssh_private_key=None
            ):
    if staging_ssh_port:
        with settings(
        host_string=f'vagrant@{host}:{staging_ssh_port}',
        private_key_filename=staging_ssh_private_key
        ):
            return _create_session_on_server(host, email)
    else:
        with settings(host_string=f'vagrant@{host}'):
            return _create_session_on_server(host, email)
