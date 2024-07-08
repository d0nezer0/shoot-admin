import sys
sys.path.append('./db_data_bak1128/daba.db')

from models.terminal_information_table import TerminalInformation


def add_device(device_code, device_number):
    TerminalInformation.create(device_code=device_code,
                               device_number=device_number)


def get_devices():
    for device in TerminalInformation.select():
        print(device.device_code, "--", device.device_number)


if __name__ == "__main__":
    # TerminalInformation.create_table()
    # add_device("test001", 1)
    # add_device("test002", 2)
    # add_device("test003", 3)
    # add_device("test004", 4)
    # add_device("test005", 5)
    # add_device("test006", 6)
    # add_device("test007", 7)
    # add_device("test008", 8)
    # add_device("test009", 9)
    # add_device("test0010", 10)
    get_devices()
