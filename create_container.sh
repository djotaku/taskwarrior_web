#! /bin/bash

echo "Build from dhi.io/python:3.13"
ctr=$(buildah from docker.io/python:3.13-slim)

echo "Upgrade pip"
buildah run $ctr /bin/bash -c 'pip install -U pip'

echo "Install taskwarrior, git, and m"
buildah run $ctr /bin/bash -c 'apt update'
buildah run $ctr /bin/bash -c 'apt install taskwarrior git gcc -y'

buildah run $ctr /bin/sh -c 'git clone https://github.com/djotaku/taskwarrior_web.git'

echo "Create the virtual environment"
buildah run $ctr /bin/sh -c 'python -m venv /taskwarrior_web/venv'

echo "Activate the virtual environment"
buildah run $ctr /bin/bash -c 'source /taskwarrior_web/venv/bin/activate'

echo "Install the requirements and Gunicorn"
buildah run $ctr /bin/sh -c 'pip install -r /taskwarrior_web/requirements.txt'
buildah run $ctr /bin/sh -c 'pip install gunicorn'

echo "Set the volumes"
buildah config --volume /taskwarrior_web/ $ctr
buildah config --volume /root/.task/ $ctr
buildah config --volume /root/.taskrc $ctr

echo "set the timezone"
buildah run $ctr /bin/bash -c 'ln -snf /usr/share/zoneinfo/America/New_York /etc/localtime && echo America/New_York > /etc/timezone'

echo "set the command to run"
buildah config --cmd "gunicorn --chdir taskwarrior_web/taskwarrior_web -b 0.0.0.0:8000 app:app --reload" $ctr
buildah config --cmd "python -m taskwarrior_web.app" $ctr

echo "commit the image"
buildah commit $ctr taskwarrior_web