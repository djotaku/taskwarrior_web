# taskwarrior_web

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

## About the dependency I'm using

For now I'm using the taskwarrior library developed by CoddingtonBear - the dev of Inthe.am. It can be found at https://github.com/coddingtonbear/python-taskwarrior - the link on pypi is broken. It looks like the pypi.org page points to the wrong repo. CoddingtonBear hasn't worked on it in a year, so it may break with newer versions of taskwarrior. For now I'm just going to go along with it. It looks like it (and also [taskw's](https://github.com/ralphbean/taskw) safe interface) just runs taskwarrior on the commandline and then grabs the output. I do something similar for [Snap-in-Time](https://github.com/djotaku/Snap-in-Time), so if I had to re-implement this in the future, I think I could do it, even if I had to write the library myself.

## ToDO

- create the flask app running on my local machine (or a test VM for safety purposes) and make sure it can interact correctly with a taskwarrior list
- figure out how to run taskserver and document (since their documentation is - ugh - a slideshow)
- create a docker/podman container to run the server and this flask app
- create sign-in page. Don't need a crazy login solution with a database or Oauth since it's meant to be single-user.
- use control flow to have the table changed from "Completed" to "Incomplete" on the Completed Tasks tab
- in parallel with various steps above, beautify with HTMX (so use fragments) and CSS framework - most likely bulma.io.
  - If I want to edit a task - send it up to the "Add Task" and change the button label to "modify task"
  - 