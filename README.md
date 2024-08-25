# Apache Site Up Script

## Overview

The `apache-site-up.py` script is designed to manage Apache virtual hosts on a development system. It provides commands for creating, enabling, disabling, deleting sites, and updating the `/etc/hosts` file. This script is useful for automating the setup and teardown of Apache virtual hosts during development.

## Features

- **Create a Site:** Initializes site folder and files.
- **Enable a Site:** Sets up Apache configurations and updates the `/etc/hosts` file.
- **Disable a Site:** Disables the site in Apache and optionally updates the `/etc/hosts` file.
- **Delete a Site:** Removes the site folder, configuration, and updates `/etc/hosts`.
- **Remove Host Entry:** Removes the site entry from `/etc/hosts` without affecting Apache configurations or site files.

## Installation

### Prerequisites

- Python 3.x installed on your system.
- Apache web server installed and configured.
- Sufficient permissions to modify Apache configurations and `/etc/hosts` (use `sudo` as needed).

### Configuration

The script contains several constants that may need to be configured based on your system setup. These constants are defined at the top of the script:

1. **`PROJECTS_DIR`**: Directory where site folders are created.
   - **Default:** `os.path.expanduser('~/projects/web')`
   - **Modification:** Set this to the directory where you want to manage your site folders.

2. **`VARWWW_DIR`**: Directory where symbolic links to site folders are created.
   - **Default:** `/var/www`
   - **Modification:** Change this if your symbolic links should be placed in a different directory.

3. **`HOSTS_FILE`**: Path to the `/etc/hosts` file.
   - **Default:** `/etc/hosts`
   - **Modification:** Change this if your hosts file is located elsewhere.

4. **`APACHE_SITES_AVAILABLE`**: Directory for Apache site configurations.
   - **Default:** `/etc/apache2/sites-available`
   - **Modification:** Update this if your Apache configuration files are stored in a different location.

5. **`APACHE_SITES_ENABLED`**: Directory for enabled Apache sites.
   - **Default:** `/etc/apache2/sites-enabled`
   - **Modification:** Change this if your enabled sites directory is different.

### Installation Steps

1. **Download the Script**

   Save the `apache-site-up.py` script to your local machine.

2. **Configure the Script**

   Open `apache-site-up.py` in a text editor and update the constants as needed to match your system configuration.

3. **Make the Script Executable**

   ```bash
   chmod +x apache-site-up.py
   ```

4. **Run the Script**

   Use the script with the appropriate flags to manage your Apache virtual hosts. For example:

   - **Create a Site:**

     ```bash
     ./apache-site-up.py <site_name> --create
     ```

   - **Enable a Site:**

     ```bash
     sudo ./apache-site-up.py <site_name> --hosts
     ```

   - **Disable a Site:**

     ```bash
     sudo ./apache-site-up.py <site_name> --disable --hosts
     ```

   - **Delete a Site:**

     ```bash
     sudo ./apache-site-up.py <site_name> --remove
     ```

   - **Remove Host Entry:**

     ```bash
     sudo ./apache-site-up.py <site_name> --rm-host
     ```

## Usage

### Create a Site

**Command:**

```bash
./apache-site-up.py <site_name> --create
```

Creates the site folder and necessary files (`index.html` and `info.php`), but does not configure Apache or update `/etc/hosts`.

### Enable a Site

**Command:**

```bash
sudo ./apache-site-up.py <site_name> --hosts
```

Creates a symbolic link for the site in `/var/www`, sets up Apache configurations, and updates `/etc/hosts`.

### Disable a Site

**Command:**

```bash
sudo ./apache-site-up.py <site_name> --disable --hosts
```

Disables the site in Apache, removes the symbolic link, and optionally updates `/etc/hosts`.

### Delete a Site

**Command:**

```bash
sudo ./apache-site-up.py <site_name> --remove
```

Disables the site if enabled, removes the site folder and its contents, and updates `/etc/hosts`.

### Remove Host Entry from `/etc/hosts`

**Command:**

```bash
sudo ./apache-site-up.py <site_name> --rm-host
```

Removes the site entry from `/etc/hosts` without affecting Apache configurations or site files.

## When to Use `sudo`

- **Create Symbolic Link:** `sudo` is required to create symbolic links in `/var/www`.
- **Update Apache Configurations:** `sudo` is required to write to `/etc/apache2/sites-available` and enable sites with `a2ensite`.
- **Modify `/etc/hosts`:** `sudo` is required to append or remove entries from `/etc/hosts`.

**Why Use `sudo`:**

- **Access Control:** Ensures that only users with administrative rights can make system-wide changes.
- **System Integrity:** Prevents unauthorized changes that could affect system stability or security.

**Avoid Using `sudo` When:**

- **Creating Site Folders and Files:** No need for `sudo` if working in a user directory.
- **Testing Scripts:** Avoid `sudo` to prevent accidental system changes.

## Troubleshooting

- **Permission Issues:** Ensure you have appropriate permissions. Use `sudo` where necessary.
- **File Exists Errors:** Check for existing files or symbolic links before creating or modifying them.

## License

This script is licensed under the MIT License. For more details, refer to the [LICENSE.md](LICENSE.md) file.
