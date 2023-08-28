#!/bin/bash

qt6_build()
{
    python3 setup.py build --parallel "$(nproc)" bdist_wheel --limited-api yes
    export dir_name=qfpa-py${PYTHON_VERSION}-qt${QT_VERSION}-64bit-release
    export archive_name=extra-${PYTHON_PLATFORM}
    tar czvf "/output/$dir_name.tar.gz" -C "./build/$dir_name/install" .
    cp ./dist/* /output
}

qt5_build()
{
    echo "Not implemented"
    exit 1
}

get_variables()
{
    export PYTHON_PLATFORM=$(python3 -c "from packaging.tags import sys_tags; print(next(sys_tags()).platform.lower().replace(\"-\", \"_\").replace(\".\", \"_\").replace(\" \", \"_\"))")
}

init()
{
    get_variables

    mkdir -p /output

    cd /opt \
        && git clone -b ${QT_VERSION} https://code.qt.io/pyside/pyside-setup.git \
        && cd pyside-setup \
        && pip3 install -r requirements.txt
}

main()
{
    init

    case $QT_VERSION in 
        6*)
            qt6_build
        ;;
        5*)
            qt5_build
        ;;
        *)
            echo "Unsupported version of QT"
            exit 1
        ;;
    esac
}


