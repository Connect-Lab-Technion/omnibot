#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/connect/catkin_ws/src/rosserial/rosserial_python"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/connect/catkin_ws/install_isolated/lib/python3.8/site-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/connect/catkin_ws/install_isolated/lib/python3.8/site-packages:/home/connect/catkin_ws/build_isolated/rosserial_python/lib/python3.8/site-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/connect/catkin_ws/build_isolated/rosserial_python" \
    "/usr/bin/python3" \
    "/home/connect/catkin_ws/src/rosserial/rosserial_python/setup.py" \
     \
    build --build-base "/home/connect/catkin_ws/build_isolated/rosserial_python" \
    install \
    --root="${DESTDIR-/}" \
     --prefix="/home/connect/catkin_ws/install_isolated" --install-scripts="/home/connect/catkin_ws/install_isolated/bin"
