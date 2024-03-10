import subprocess
import os
import shutil
import tarfile

def get_opt_dir():
    if os.name == 'nt':
        os.mkdir("/opt")
        return "/opt"
    else:
        return "/opt"

def qt6_build():
    subprocess.run(["python3", "setup.py", "build", "--parallel", str(os.cpu_count()), "bdist_wheel", "--limited-api", "yes"], check=True)
    dir_name = f'qfpa-py{os.environ["PYTHON_VERSION"]}-qt{os.environ["QT_VERSION"]}-64bit-release'
    archive_name = f'extra-{os.environ["PYTHON_PLATFORM"]}'
    with tarfile.open(f'/output/{archive_name}.tar.gz', 'w:gz') as tar:
        tar.add(f'./build/{dir_name}/install', arcname='.')
    shutil.copytree('./dist', '/output', dirs_exist_ok=True)

def qt5_build():
    print("Not implemented")
    exit(1)

def get_variables():
    result = subprocess.run(["python3", "-c", "from packaging.tags import sys_tags; print(next(sys_tags()).platform.lower().replace('-', '_').replace('.', '_').replace(' ', '_'))"], capture_output=True, text=True)
    os.environ["PYTHON_PLATFORM"] = result.stdout.strip()

def init():
    get_variables()

    os.makedirs('/output', exist_ok=True)

    os.chdir(get_opt_dir())
    subprocess.run(["git", "clone", "-b", os.environ["QT_VERSION"], "https://code.qt.io/pyside/pyside-setup.git"], check=True)
    os.chdir('pyside-setup')
    subprocess.run(["pip3", "install", "-r", "requirements.txt"], check=True)

def main():
    init()

    if os.environ["QT_VERSION"].startswith("6"):
        qt6_build()
    elif os.environ["QT_VERSION"].startswith("5"):
        qt5_build()
    else:
        print("Unsupported version of QT")
        exit(1)

if __name__ == "__main__":
    main()
