# taskwarrior_web

![screenshot](https://github.com/djotaku/taskwarrior_web/blob/main/taskwarrior_web/screenshots/Taskwarrior_web.png)

## Why this repo?

With the demise of Inthe.am later this year and FreeCinc last year, there aren't any web interfaces for taskwarrior left. It turns out that taskserver, as written, doesn't really scale well for multiple users. So I'm going to write this UI for my needs. Feel free to use it if it works for you.

##
Usage

- Need taskwarrior installed
- need a file called secrets_config with:

```json
{
  "SECRET_KEY":"some random letters"
}
```
- use create_new_password_hash() function in utility_functions.py

I used the taskd container at https://github.com/ogarcia/docker-taskd which I have forked just in case. After that, just use the instructions at https://gothenburgbitfactory.github.io/taskserver-setup/ to get your user created, etc. I ran into an error at first where I had to go into the config file and change the server it was binding to, but then had to change it back to 0.0.0.0 after the certs were correctly created. I also had to change the request.limit to 0 to get my initial sync to work.

Go into your taskwarrior_web container (eg podman exec -ti taskwarrior_web /bin/sh) and run task to generate your .taskrc.

You should now be able to log in.

Copy your .pem files from the sync step over to the volume you mounted to /root/.task and run the same steps to setup the taskd. server as before. Run task sync.



## About the dependency I'm using

For now I'm using the taskwarrior library developed by CoddingtonBear - the dev of Inthe.am. It can be found at https://github.com/coddingtonbear/python-taskwarrior - the link on pypi is broken. It looks like the pypi.org page points to the wrong repo. CoddingtonBear hasn't worked on it in a year, so it may break with newer versions of taskwarrior. For now I'm just going to go along with it. It looks like it (and also [taskw's](https://github.com/ralphbean/taskw) safe interface) just runs taskwarrior on the commandline and then grabs the output. I do something similar for [Snap-in-Time](https://github.com/djotaku/Snap-in-Time), so if I had to re-implement this in the future, I think I could do it, even if I had to write the library myself.

## ToDO

- add button to sync tasks
