"""Module with useful netowrking functions"""
import logging
import subprocess
import paramiko


def is_host_available(host: str) -> bool:
    """Test if ping is successful"""
    command = ["ping", "-c", "1", host]
    try:
        response = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, timeout=2)
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False
    if "1 packets received" in response:
        return True
    return False


def scp_file_from_host(hostname: str, filename: str) -> bytes | None:
    """Get file from remote.  Must have keys set up."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname)
        # Read remote file contents as binary data
        sftp = ssh.open_sftp()

        # execute acl command to grant access to user on file
        acl_command = f"sudo chmod +a 'cbusillo allow read,write,execute' '{filename}'"
        ssh.exec_command(acl_command)

        remote_file = sftp.open(filename, mode="rb")
        file_contents = remote_file.read()
        remote_file.close()
        sftp.close()
        ssh.close()
        return file_contents

    except paramiko.AuthenticationException:
        logging.error("Authentication failed. Please check your username and password.")
    except paramiko.SSHException as ssh_error:
        logging.error("SSH error: %s", ssh_error)
    finally:
        ssh.close()
    return None
