from enum import IntEnum
from genericpath import exists
import subprocess
import wget
import os
import tarfile
from utils import text

environment_name = "OO_PS4_TOOLCHAIN"


class install_types (IntEnum):
    WSL = 1
    WINDOWS = 2
    LINUX = 3


print(text.clear)
print(text.blue + "Open Orbis Toolchain Setup\n" + text.reset)

# Get installation parameters
install_type = int(input(
                   "Set installation type (WSL = 1 | WINDOWS = 2 | LINUX = 3): "))


if install_type < 1 or install_type > 3:
    print("Installation type not supported")
    exit(-1)

print(text.clear)
if environment_name in os.environ:
    # Continue installation?
    conti = ""
    while conti != "Y" and conti != "N":
        conti = input(
            environment_name+" found in environment variables. Continue? (Y/N): ")
        print(conti)
    # Exit installer
    if conti == "N":
        print(text.clear)
        exit(-1)

print(text.clear)

# Download OpenOrbisToolchain
# Download dir == current dir
output_dir = os.getcwd()
install_dir = ""
if install_type == install_types.WSL or install_type == install_types.WINDOWS:
    print("Downloading Toolchain installer")
    toolchain_url = "https://github.com/OpenOrbis/OpenOrbis-PS4-Toolchain/releases/download/v0.5.1/OpenOrbis.PS4.Toolchain.v0.5.1.exe"
    filename = wget.download(toolchain_url, out=output_dir)

elif install_type == install_types.LINUX:
    print("Downloading Toolchain binaries")
    toolchain_url = "https://github.com/OpenOrbis/OpenOrbis-PS4-Toolchain/releases/download/v0.5.1/v0.5.1.tar.gz"
    filename = wget.download(toolchain_url, out=output_dir)


# Install Toolchain Windows
toolchain_dir = ""
if install_type == install_types.WSL or install_type == install_types.WINDOWS:
    # Launch installer
    install_process = subprocess.Popen(
        os.path.join(output_dir, filename), cwd=output_dir)
    # Wait for installation to finish
    return_code = install_process.wait()

    if return_code == 2:
        print("\nToolchain installation cancelled")
    elif return_code == 0:
        print(text.clear)
        toolchain_dir = "C:/OpenOrbis/PS4Toolchain"
        print("Toolchain installation successfull")
    else:
        print("\nCould not install toolchain error: " + str(return_code))

# Install Toolchain Linux
elif install_type == install_types.LINUX:
    home_dir = os.environ.get("HOME")
    toolchain_dir = os.path.join(home_dir, "OpenOrbis/PS4Toolchain/")
    print(text.clear)
    conti = input("Toolchain will be installed in '" +
                  toolchain_dir+"'. Continue? (Y/N): ")
    while conti != "Y" and conti != "N":
        conti = input("Toolchain will be installed in '" +
                      toolchain_dir+"'. Continue? (Y/N): ")
    if conti == "Y":
        file_path = os.path.join(output_dir, filename)
        file = tarfile.open(file_path)
        file.extractall(toolchain_dir)
        file.close()
    else:
        toolchain_dir = ""

# Clean installation files
print("Cleaning installation files")
installer_path = os.path.join(output_dir, filename)
if exists(installer_path):
    os.remove(installer_path)

# Download create-gp4
install_create_gp4 = input("Add 'create-gp4' to Toolchain? (Y/N): ")
while install_create_gp4 != "Y" and install_create_gp4 != "N":
    install_create_gp4 = input("Add 'create-gp4' to Toolchain? (Y/N): ")
if toolchain_dir != "":
    if install_create_gp4 == "Y":
        # Download create-gp4.tar.gz
        create_gp4_url = "https://github.com/OpenOrbis/create-gp4/releases/download/v1.0/binaries.tar.gz"
        filename = wget.download(create_gp4_url, out=output_dir)
        file_path = os.path.join(output_dir, filename)

        # Extract to toolchain dir
        file = tarfile.open(file_path)
        file.extractall(toolchain_dir)
        file.close()
        # Clean files
        if exists(file_path):
            os.remove(file_path)
else:
    print("Toolchain directory not found")
    exit(-1)

print(text.blue + "\nOpenOrbis Toolchain configured succesfully" + text.reset)
