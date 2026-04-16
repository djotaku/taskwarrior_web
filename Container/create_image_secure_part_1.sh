#! /bin/bash

echo "Build from dhi.io/python:3.13"
ctr=$(buildah from dhi.io/python:3.13-debian13-dev)

echo "Upgrade pip"
buildah run $ctr /bin/bash -c 'pip install -U pip'

echo "Turn on Backports to get newer taskwarrior"
buildah copy $ctr 'debian-backports.sources' '/etc/apt/sources.list.d/debian-backports.sources'

echo "Install taskwarrior, git, and m"
buildah run $ctr /bin/bash -c 'apt update'
buildah run $ctr /bin/bash -c 'apt install git gcc -y'
buildah run $ctr /bin/bash -c 'apt install taskwarrior/trixie-backports'

echo "commit the image"
buildah commit $ctr tw_p1