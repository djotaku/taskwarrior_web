#! /bin/bash

echo "Build from localhost/tw_p1"
ctr=$(buildah from localhost/tw_p1)

buildah run $ctr /bin/sh -c 'git clone https://github.com/djotaku/taskwarrior_web.git'

buildah run $ctr /bin/sh -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'

buildah run $ctr /bin/sh -c '/root/.local/bin/uv python install 3.13'



echo "Set the volumes"
buildah config --volume /taskwarrior_web/ $ctr
buildah config --volume /root/.task/ $ctr
buildah config --volume /root/.taskrc $ctr

echo "set the timezone"
buildah run $ctr /bin/bash -c 'ln -snf /usr/share/zoneinfo/America/New_York /etc/localtime && echo America/New_York > /etc/timezone'

echo "set the command to run"
buildah config --cmd "gunicorn --chdir taskwarrior_web/src/ -b 0.0.0.0:8000 app:app --reload" $ctr

echo "commit the image"
buildah commit $ctr taskwarrior_web