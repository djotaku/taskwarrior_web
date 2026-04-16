#! /bin/bash

echo "Build from docker.io/fedora:43"
ctr=$(buildah from docker.io/fedora:43)

echo "Install taskwarrior, git, python, gcc"
buildah run $ctr /bin/bash -c 'dnf update -y'
buildah run $ctr /bin/bash -c 'dnf install git gcc -y'
buildah run $ctr /bin/bash -c 'dnf install task -y'

echo "commit the image"
buildah commit $ctr tw_p1