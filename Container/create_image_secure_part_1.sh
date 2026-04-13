#! /bin/bash

echo "Build from dhi.io/python:3.13"
ctr=$(buildah from dhi.io/python:3.13-debian13-dev)

echo "Upgrade pip"
buildah run $ctr /bin/bash -c 'pip install -U pip'

echo "Install taskwarrior, git, and m"
buildah run $ctr /bin/bash -c 'apt update'
buildah run $ctr /bin/bash -c 'apt install taskwarrior git gcc -y'

echo "commit the image"
buildah commit $ctr tw_p1