# taskwarrior_web

![screenshot](https://github.com/djotaku/taskwarrior_web/blob/main/taskwarrior_web/screenshots/Taskwarrior_web.png)

## Why this repo?

Taskwarrior_web is meant for use by one user to be able to access, create, modify, and complete their tasks from the web.

## Instructions for taskwarrior_web using taskwarrior 3.x

These instructions assume the user wants to access their tasks from the web. You would use taskwarrior as normal on your computer to interface with the tasks. Then you would sync using taskchampion-sync. Once the sync is complete, you can them access your tasks from the web.

If you wish to do so, you can run this locally. It would then function as a web interface to your taskwarrior instance. In that case, you don't need the sync server and you wouldn't want to use the container. Instead, clone the repo, change the replica disk location in the task.py file. Then run the app.py file.

### Setup

- Need taskwarrior 3.x installed on your personal computer if you're syncing with the web interface.
- Need the [taskchampion sync-server](https://github.com/GothenburgBitFactory/taskchampion-sync-server)
  - Currently, the easiest way to run the server is to clone the repo, build the container (with Docker or Buildah), and then run the server.  

Example, building with buildah:

```bash
buildah build \
  -t taskchampion-sync-server \
  -f Dockerfile-sqlite
# note: at the time I write this, I had to change the Dockerfile from the taskchampion sync server repo to point at Rust 1.88
```
Running with podman:

```bash
podman run -dt --name taskchampion -p 8080:8080 -v taskchampion_sync:/var/lib/taskchampion-sync-server/data localhost/taskchampion-sync-server
```
On the computer with your taskwarrior instance, run:

```bash
task config sync.encryption_secret <encryption_secret>
```
According to the official docs pwgen will give a good value for the encryption secret.

Then you need to run

```bash
task config sync.server.url               <url>
task config sync.server.client_id         <client_id>
```
The url must have http or https. If you are not running at port 80 or 443, specify the port. Client ID must be a valid UUID. (Use a UUID program to create a valid UUID)

- use create_new_password_hash() function in utility_functions.py
- create a file called secrets_config with:
- 
```json
{
  "SECRET_KEY":"some random letters",
  "user": {"username_you_want": 
  {"password": "output of create_new_password_hash()"}}
}
```
If you wish to run this web app as a container, the script I use to create the container with buildah is create_image_secure.sh. This is the one I push to Docker Hub. (In the future I may consider pushing to the github container registry if that doesn't cost money)

TODO: Add instructions for using running the container.

## Instructions for taskwarrior_web using taskwarrior 2.x

The final release for use with taskwarrior 2.x is taskwarrior_web v1.1.

###
Usage

- Need taskwarrior installed
- use create_new_password_hash() function in utility_functions.py
- need a file called secrets_config with:
- 
```json
{
  "SECRET_KEY":"some random letters",
  "user": {"username_you_want": 
  {"password": "output of create_new_password_hash()"}}
}
```

I used the taskd container at https://github.com/ogarcia/docker-taskd which I have forked just in case. 

You might set it up like this:

```shell
#! /bin/bash

podman run -d \
          --name=taskd \
            -e CERT_BITS=4096 \
              -e CERT_EXPIRATION_DAYS=365 \
                -e CERT_ORGANIZATION="Your Name" \
                  -e CERT_CN=yoururl.com \
                    -e CERT_COUNTRY=US \
                      -e CERT_STATE="YourState" \
                        -e CERT_LOCALITY="YourCity" \
                          -p 53589:53589 \
                            -v taskd:/var/taskd \
                              ghcr.io/connectical/taskd
```

After that, use the instructions at https://gothenburgbitfactory.github.io/taskserver-setup/ to get your user created, etc. I ran into an error at first where I had to go into the config file and change the server it was binding to, but then had to change it back to 0.0.0.0 after the certs were correctly created. I also had to change the request.limit to 0 to get my initial sync to work.

Keep going on those setup instructions to set up your local computer to sync. It will generate involve the .pem files.

You can then run this web app in a container like so:

```shell
podman run -d \
          --name=taskwarrior_web -e TZ=America/New_York -v ./taskrc:/root/.taskrc:Z \
                            -v taskwarrior_web:/taskwarrior_web -v taskwarrior_web_tasks:/root/.task \
                            -p 8000:8000  djotaku/taskwarrior_web:20240309
```

Go into your taskwarrior_web container (eg podman exec -ti taskwarrior_web /bin/sh) and run task to generate your .taskrc.

You should now be able to log in.

Copy your .pem files from the sync step over to the volume you mounted to /root/.task and run the same steps to setup the taskd. server as before. Run task sync.

To periodically sync the web interface with the server, you might want to set up this cron job whereever your containers are running:

```shell
* * * * * podman exec taskwarrior_web /usr/bin/task sync
```
That will run sync every minute.

### Updating cert

If you have the container running, and you need to regenerate the certificates or modify their parameters.

- Make sure that the container is running.
- Execute a shell in the running container.
  ```shell
  docker exec -t -i \
    <container-id> sh
  ```
- Go to `/var/taskd/pki` and delete all pem files, you should be left with
  only the generate scripts (`generate*`) and the `vars` file.
  ```shell
  rm *pem
  ```
- Run.
  ```shell
  export CERT_BITS=4096
  export CERT_EXPIRATION_DAYS=365
  export CERT_ORGANIZATION="Göteborg Bit Factory"
  export CERT_CN=localhost
  export CERT_COUNTRY=SE
  export CERT_STATE="Västra Götaland"
  export CERT_LOCALITY="Göteborg"
  ./generate
  ```

Then copy the client and ca certs to your computer.