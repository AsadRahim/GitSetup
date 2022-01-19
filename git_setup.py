import sys
import os
from Crypto.PublicKey import RSA
HOME_DIR = os.path.expanduser("~")
PREFIX = ''
REPO = {
    'github': 'github.com',
    'gitlab': 'gitlab.com',
    'bikbucket': 'bitbucket.org'
}
GLOBAL_CONFIG = """
[includeIf "gitdir:~/{project_name}"]
    path = ~/.gitconfigs/.gitconfig-{project_name}
"""
PROJECT_CONFIG = """
[core]
    compression = 0
[http]
    postBuffer = 1048576000
[user]
    name = {username}
    email = {email}
"""
SSH_CONFIG = """
Host {project_name}.{repo_host}
    HostName {repo_host}
    User git
    IdentityFile ~/.ssh/id_rsa_{project_name}
"""
def main():
    repo = input("Enter repo (github/gitlab/bitbucket): ")
    project_name = input("Enter project name: ")
    username = input("Enter username: ")
    email = input("Enter email: ")
    repo_host = REPO[repo]
    # Global Config
    if os.path.exists(os.path.join(HOME_DIR, PREFIX, ".gitconfig")):
        with open(os.path.join(HOME_DIR, PREFIX, ".gitconfig"), 'a', encoding='utf-8') as file:
            file.write(GLOBAL_CONFIG.format(project_name=project_name))
    else:
        with open(os.path.join(HOME_DIR, PREFIX, ".gitconfig"), 'w', encoding='utf-8') as file:
            file.write(GLOBAL_CONFIG.format(project_name=project_name))
        os.chmod(os.path.join(HOME_DIR, PREFIX, ".gitconfig"), 644)
    # Project Config
    if os.path.exists(os.path.join(HOME_DIR, PREFIX, ".gitconfigs")):
        with open(os.path.join(HOME_DIR, PREFIX, f".gitconfigs/.gitconfig-{project_name}"), 'w', encoding='utf-8') as file:
            file.write(PROJECT_CONFIG.format(username=username,email=email))
        os.chmod(os.path.join(
            HOME_DIR, PREFIX, f".gitconfigs/.gitconfig-{project_name}"), 644)
    else:
        os.mkdir(os.path.join(HOME_DIR, PREFIX, ".gitconfigs"))
        with open(os.path.join(HOME_DIR, PREFIX, f".gitconfigs/.gitconfig-{project_name}"), 'w', encoding='utf-8') as file:
            file.write(PROJECT_CONFIG.format(username=username,email=email))
        os.chmod(os.path.join(
            HOME_DIR, PREFIX, f".gitconfigs/.gitconfig-{project_name}"), 644)
    # SSH Config
    if os.path.exists(os.path.join(HOME_DIR, PREFIX, ".ssh/config")):
        with open(os.path.join(HOME_DIR, PREFIX, ".ssh/config"), 'a', encoding='utf-8') as file:
            file.write(SSH_CONFIG.format(project_name=project_name,repo_host=repo_host))
    else:
        with open(os.path.join(HOME_DIR, PREFIX, ".ssh/config"), 'w', encoding='utf-8') as file:
            file.write(SSH_CONFIG.format(project_name=project_name,repo_host=repo_host))
    # Generate RSA Keys
    key = RSA.generate(2048)
    with open(os.path.join(HOME_DIR, PREFIX, f".ssh/id_rsa_{project_name}"), 'wb') as content_file:
        os.chmod(os.path.join(
            HOME_DIR, PREFIX, f".ssh/id_rsa_{project_name}"), 600)
        content_file.write(key.exportKey('PEM'))
    pubkey = key.publickey()
    with open(os.path.join(HOME_DIR, PREFIX, f".ssh/id_rsa_{project_name}.pub"), 'wb') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))
    print('Id RSA public Key\n', pubkey.exportKey('OpenSSH'))
if __name__ == "__main__":
    main()
