# What is it?

teampulls lists all of the pull requests for a list of users and repositories. On top of that every pull requests that is older than 14 days is printed in red.

# Getting started

## Installation

```
pip install teampulls
```

## Edit the settings file

Please copy the [`teampulls.toml`](https://github.com/brejoc/teampulls/blob/master/teampulls.toml) either to `/etc/teampulls.toml` or to `~/.teampulls.toml`. Now you'll have to add the users and repositories you are interested in. You also need a Github API token, that can either be set in the settings file or via the environment variable `GITHUB_TOKEN_GALAXY`.

## Get the pull requests

To get the list of pull requests you can execute `teampulls`.

<img src="https://raw.githubusercontent.com/brejoc/teampulls/master/doc/screenshot1.png" />
