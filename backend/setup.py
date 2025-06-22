import subprocess
import sys
import os
import platform

VENV_DIR = "venv"
REQUIRED_PACKAGES = ["starlite", "bcrypt", "itsdangerous", "uvicorn"]


def create_virtualenv():
    if not os.path.isdir(VENV_DIR):
        print("🔧 Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print("✅ Virtual environment already exists.")


def get_pip_path():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")


def install_packages():
    pip = get_pip_path()
    subprocess.check_call([pip, "install", "--upgrade", "pip"])
    subprocess.check_call([pip, "install"] + REQUIRED_PACKAGES)


def freeze_requirements():
    pip = get_pip_path()
    with open("requirements.txt", "w") as f:
        subprocess.check_call([pip, "freeze"], stdout=f)


def print_activation_help():
    print("\n✅ Setup complete.")
    if platform.system() == "Windows":
        print("👉 To activate the virtual environment:\n    venv\\Scripts\\activate")
    else:
        print("👉 To activate the virtual environment:\n    source venv/bin/activate")


if __name__ == "__main__":
    create_virtualenv()
    install_packages()
    freeze_requirements()
    print_activation_help()
