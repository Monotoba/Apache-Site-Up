#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse

PROJECTS_DIR = os.path.expanduser('~/projects/web')
VARWWW_DIR = '/var/www'
HOSTS_FILE = '/etc/hosts'
APACHE_SITES_AVAILABLE = '/etc/apache2/sites-available'
APACHE_SITES_ENABLED = '/etc/apache2/sites-enabled'
APACHE_LOG_DIR = '/var/log/apache2'  # Define the log directory here

APACHE_CONF_TEMPLATE = """
<VirtualHost *:80>
    ServerName {site_name}
    DocumentRoot {document_root}

    <Directory {document_root}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog {log_dir}/{site_name}_error.log
    CustomLog {log_dir}/{site_name}_access.log combined
</VirtualHost>
"""

def run_command(command, check=True):
    print(f"Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, command)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(e.returncode)

def create_site_folder(site_name):
    site_path = os.path.join(PROJECTS_DIR, site_name)
    if not os.path.exists(site_path):
        os.makedirs(site_path)
        print(f"Created site directory: {site_path}")

        # Create index.html
        index_html_path = os.path.join(site_path, 'index.html')
        index_html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_name}</title>
</head>
<body>
    <h1>Welcome to {site_name}</h1>
    <p>This site is currently under development.</p>
    <p>For more information, visit <a href="info.php">info.php</a>.</p>
</body>
</html>
"""
        with open(index_html_path, 'w') as f:
            f.write(index_html_content)
        print(f"Created index.html at: {index_html_path}")

        # Create info.php
        info_php_path = os.path.join(site_path, 'info.php')
        info_php_content = """<?php
phpinfo();
?>
"""
        with open(info_php_path, 'w') as f:
            f.write(info_php_content)
        print(f"Created info.php at: {info_php_path}")

def enable_site(site_name, update_hosts):
    site_folder = os.path.join(PROJECTS_DIR, site_name)
    if not os.path.exists(site_folder):
        print(f"Site folder does not exist: {site_folder}")
        sys.exit(1)

    # Create symbolic link
    symlink_path = os.path.join(VARWWW_DIR, site_name)
    if os.path.exists(symlink_path):
        print(f"Symbolic link already exists: {symlink_path}")
    else:
        os.symlink(site_folder, symlink_path)
        print(f"Created symbolic link: {symlink_path}")

    # Create Apache configuration file
    conf_file = os.path.join(APACHE_SITES_AVAILABLE, f"{site_name}.conf")
    if not os.path.exists(conf_file):
        with open(conf_file, 'w') as f:
            f.write(APACHE_CONF_TEMPLATE.format(
                site_name=site_name,
                document_root=site_folder,
                log_dir=APACHE_LOG_DIR
            ))

    # Enable site
    run_command(f"sudo a2ensite {site_name}.conf")
    run_command("sudo systemctl reload apache2")

    if update_hosts:
        # Update /etc/hosts
        run_command(f"sudo bash -c 'echo \"127.0.0.1 {site_name}\" >> {HOSTS_FILE}'")
        print(f"Added {site_name} to {HOSTS_FILE}")

    print(f"Enabled site: {site_name}")

def disable_site(site_name, update_hosts):
    conf_file = os.path.join(APACHE_SITES_AVAILABLE, f"{site_name}.conf")
    if not os.path.exists(conf_file):
        print(f"Apache configuration file does not exist: {conf_file}")
        return

    # Disable site
    run_command(f"sudo a2dissite {site_name}.conf")
    run_command("sudo systemctl reload apache2")

    # Remove symbolic link
    symlink_path = os.path.join(VARWWW_DIR, site_name)
    if os.path.exists(symlink_path):
        os.remove(symlink_path)
        print(f"Removed symbolic link: {symlink_path}")

    # Remove Apache configuration file
    if os.path.exists(conf_file):
        os.remove(conf_file)
        print(f"Removed Apache configuration file: {conf_file}")

    if update_hosts:
        # Remove entry from /etc/hosts
        run_command(f"sudo sed -i '/{site_name}/d' {HOSTS_FILE}")
        print(f"Removed {site_name} from {HOSTS_FILE}")

    print(f"Disabled site: {site_name}")

def remove_host(site_name):
    # Remove entry from /etc/hosts
    run_command(f"sudo sed -i '/{site_name}/d' {HOSTS_FILE}")
    print(f"Removed {site_name} from {HOSTS_FILE}")

def delete_site(site_name):
    # Confirm deletion
    confirm = input(f"Are you sure you want to completely delete all files, folders, and configurations for site '{site_name}'? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Deletion canceled.")
        return

    # Disable the site if it's enabled
    disable_site(site_name, update_hosts=False)

    # Remove site folder
    site_folder = os.path.join(PROJECTS_DIR, site_name)
    if os.path.exists(site_folder):
        subprocess.run(f"rm -rf {site_folder}", shell=True, check=True)
        print(f"Removed site directory: {site_folder}")

def main():
    parser = argparse.ArgumentParser(description='Manage Apache virtual hosts.')
    parser.add_argument('site_name', type=str, help='The name of the site to manage.')
    parser.add_argument('--create', '-c', action='store_true', help='Create the site folder if it does not exist.')
    parser.add_argument('--disable', '-d', action='store_true', help='Disable the site.')
    parser.add_argument('--remove', '-rm', action='store_true', help='Completely remove the site and all associated files and configurations.')
    parser.add_argument('--rm-host', '-rh', action='store_true', help='Remove the site name from the /etc/hosts file.')
    parser.add_argument('--hosts', action='store_true', help='Update the /etc/hosts file with the site name.')
    args = parser.parse_args()

    if args.create:
        create_site_folder(args.site_name)
    elif args.disable:
        disable_site(args.site_name, update_hosts=args.hosts)
    elif args.remove:
        delete_site(args.site_name)
    elif args.rm_host:
        remove_host(args.site_name)
    else:
        enable_site(args.site_name, update_hosts=args.hosts)

if __name__ == '__main__':
    main()
