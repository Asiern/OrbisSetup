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
                   "Set installation type (WSL = 1 | WINDOWS =2 | LINUX = 3): "))


if install_type < 1 or install_type > 3:
    print("Installation not supported")
    exit(-1)


if install_type == install_types.WSL:
    None
elif install_type == install_types.WINDOWS:
    None
elif install_type == install_types.LINUX:
    None

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
    install_dir = input("Select Toolchain installation path (default:)")
    # TODO extract tar.gz to installation dir
    None

# Clean installation files
print("Cleaning installation files")
installer_path = os.path.join(output_dir, filename)
if exists(installer_path):
    os.remove(installer_path)

# Set Environment variable OO_PS4_TOOLCHAIN
set_env = ""
while set_env != "Y" and set_env != "N":
    set_env = input("Set environment variable 'OO_PS4_TOOLCHAIN' ? (Y/N): ")

# Set env WINDOWS
if set_env == "Y":
    if install_type == install_types.WINDOWS:
        # TODO set env windows
        None
    elif install_type == install_types.LINUX:
        # TODO set env linux
        None
    elif install_type == install_types.WSL:
        print("Cannot set env for wsl")

# Download create-gp4
install_create_gp4 = input("Add 'create-gp4' to Toolchain? (Y/N): ")
while install_create_gp4 != "Y" and install_create_gp4 != "N":
    install_create_gp4 = input(
        "Set environment variable 'OO_PS4_TOOLCHAIN' ? (Y/N): ")

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

print(text.blue + "OpenOrbis Toolchain configured succesfully" + text.reset)
