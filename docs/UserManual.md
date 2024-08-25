# User Manual for `apache-site-up.py`

## Overview

The `apache-site-up.py` script is a tool designed to manage Apache virtual hosts on a development system. It allows for the creation, enabling, disabling, deletion of sites, and updating the `/etc/hosts` file as needed.

## Configuration

Before using the script, you may need to adjust the following constants to fit your system setup:

### Constants

- `PROJECTS_DIR`: 
  - **Purpose:** Directory where site folders are created.
  - **Default Value:** `~/projects/web`
  - **Modification:** Change this to the directory where you want to store your site projects. For example, if your sites are located in `/srv/sites`, modify the line in the script:
    ```python
    PROJECTS_DIR = os.path.expanduser('/srv/sites')
    ```

- `VARWWW_DIR`: 
  - **Purpose:** Directory where symbolic links to site folders are created.
  - **Default Value:** `/var/www`
  - **Modification:** Change this if your symbolic links need to be placed in a different directory. For instance:
    ```python
    VARWWW_DIR = '/srv/www'
    ```

- `HOSTS_FILE`: 
  - **Purpose:** Path to the hosts file that maps local domains to IP addresses.
  - **Default Value:** `/etc/hosts`
  - **Modification:** If your system uses a different path for the hosts file, update it accordingly:
    ```python
    HOSTS_FILE = '/path/to/your/hosts/file'
    ```

- `APACHE_SITES_AVAILABLE`: 
  - **Purpose:** Directory where Apache site configuration files are stored.
  - **Default Value:** `/etc/apache2/sites-available`
  - **Modification:** Change this if your Apache configuration directory is different:
    ```python
    APACHE_SITES_AVAILABLE = '/etc/httpd/conf.d'
    ```

- `APACHE_SITES_ENABLED`: 
  - **Purpose:** Directory where enabled site configurations are linked.
  - **Default Value:** `/etc/apache2/sites-enabled`
  - **Modification:** Adjust this path if your system uses a different directory:
    ```python
    APACHE_SITES_ENABLED = '/etc/httpd/sites-enabled'
    ```

- `APACHE_CONF_TEMPLATE`: 
  - **Purpose:** Template for the Apache virtual host configuration.
  - **Modification:** Edit this string to fit your Apache configuration needs. You can adjust the log paths or other directives if required.

## Operations

### Create a Site

**Command:**

```bash
./apache-site-up.py <site_name> --create
```

**Description:**

This command creates the site folder and necessary files (`index.html` and `info.php`). It sets up the initial structure for the site but does not configure Apache or update `/etc/hosts`.

### Enable a Site

**Command:**

```bash
./apache-site-up.py <site_name> --hosts
```

**Description:**

This command creates a symbolic link for the site in `/var/www`, sets up Apache configurations, and updates the `/etc/hosts` file with the site's local domain name.

**When to Use `sudo`:**

- **Create Symbolic Link:** Requires `sudo` to create symbolic links in `/var/www`, a directory typically owned by the root user.
- **Update Apache Configurations:** Requires `sudo` to write configuration files in `/etc/apache2/sites-available` and enable sites with `a2ensite`.
- **Modify `/etc/hosts`:** Requires `sudo` to append entries to `/etc/hosts`.

**Example Command with `sudo`:**

```bash
sudo ./apache-site-up.py <site_name> --hosts
```

### Disable a Site

**Command:**

```bash
./apache-site-up.py <site_name> --disable --hosts
```

**Description:**

This command disables the site in Apache, removes the symbolic link, and optionally updates the `/etc/hosts` file.

**When to Use `sudo`:**

- **Remove Symbolic Link and Configuration:** Requires `sudo` to delete symbolic links in `/var/www` and configuration files in `/etc/apache2/sites-available`.
- **Update `/etc/hosts`:** Requires `sudo` to remove entries from `/etc/hosts`.

**Example Command with `sudo`:**

```bash
sudo ./apache-site-up.py <site_name> --disable --hosts
```

### Delete a Site

**Command:**

```bash
./apache-site-up.py <site_name> --remove
```

**Description:**

This command disables the site if it's enabled, removes the site folder and its contents, and updates the `/etc/hosts` file.

**When to Use `sudo`:**

- **Remove Site Folder and Configuration:** Requires `sudo` to remove files and directories owned by the root user in `/var/www` and `/etc/apache2/sites-available`.

**Example Command with `sudo`:**

```bash
sudo ./apache-site-up.py <site_name> --remove
```

### Remove Host Entry from `/etc/hosts`

**Command:**

```bash
./apache-site-up.py <site_name> --rm-host
```

**Description:**

This command removes the site entry from the `/etc/hosts` file without affecting Apache configurations or site files.

**When to Use `sudo`:**

- **Modify `/etc/hosts`:** Requires `sudo` to make changes to `/etc/hosts`.

**Example Command with `sudo`:**

```bash
sudo ./apache-site-up.py <site_name> --rm-host
```

## When to Use `sudo`

- **File Permissions:** Commands that modify system directories (like `/var/www` and `/etc/apache2`) or system files (like `/etc/hosts`) typically require `sudo` due to permissions restrictions.
- **Apache Configuration:** Enabling or disabling sites and modifying configuration files requires elevated privileges to write to system directories.

**Why Use `sudo`:**

- **Access Control:** Ensures that only users with administrative rights can make changes that affect the entire system or other users.
- **System Integrity:** Prevents unauthorized changes that could compromise the stability or security of the system.

**Avoid Using `sudo` When:**

- **Creating Site Folders and Files:** If you are only setting up files and directories within your user’s home directory, `sudo` is not necessary.
- **Testing Scripts:** When running tests or experimenting with script functionality, avoid `sudo` to prevent accidental system changes.

## Troubleshooting

- **Permission Issues:** Ensure you are running commands requiring `sudo` with appropriate privileges. Use `sudo` only when necessary.
- **File Exists Errors:** Check if the symbolic link or configuration file already exists before creating or modifying them. Use `sudo` to resolve permission issues when necessary.

## License

This script is licensed under the MIT License. For more details, refer to the LICENSE file.
```

This updated manual now includes a section on configuring the script for different systems and modifying constants as needed.
