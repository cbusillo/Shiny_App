"""Connect to RingCentral API"""
import os
from subprocess import Popen, PIPE
from shiny_api.modules import load_config as config

print(f"Importing {os.path.basename(__file__)}...")


def get_user_from_host(hostname: str) -> tuple[str, str]:
    """return user and hostname from current remote ip"""
    host_to_user = {"chris-mbp": "cbusillo",
                    "localhost": "cbusillo",
                    "secureerase": "tech",
                    "cornerwhinymac2": "home",
                    "countershinymac": "home"}

    username = host_to_user[hostname.lower()]
    print(hostname)
    return hostname, username


def send_message_ssh(phone_number: str, message: str, ip_address: str):
    """Run Applescript to open RingCentral serach for phone number and load message"""
    with open(
            f"{config.SCRIPT_DIR}/applescript/rc_search_by_number.applescript", encoding="utf8") as file:
        script_source: str = file.read()

    script_source = script_source.replace("{phone_number}", phone_number)
    script_source = script_source.replace("{message}", message)
    hostname, username = get_user_from_host(ip_address)

    with Popen(['ssh', f'{username}@{hostname}', 'osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE) as popen:
        print(popen.communicate(bytes(script_source, encoding="utf8")))


if __name__ == "__main__":
    send_message_ssh("7578181657", "Test message", "localhost")
