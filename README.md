Docker Hub CLI
========
[![PyPI version](https://badge.fury.io/py/docker-hub.svg)](https://badge.fury.io/py/docker-hub)
[![Build Status](https://travis-ci.org/amalfra/docker-hub.svg?branch=master)](https://travis-ci.org/amalfra/docker-hub)
[![Coverage Status](https://coveralls.io/repos/github/amalfra/docker-hub/badge.svg?branch=master)](https://coveralls.io/github/amalfra/docker-hub?branch=master)

[![asciicast](https://asciinema.org/a/89901.png)](https://asciinema.org/a/89901)

A CLI tool to access Docker Hub from your terminal.

## Installation
You should have pip installed in your system.
```sh
pip install docker-hub
```
python 3 users can do
```sh
pip3 install docker-hub
```

## Usage
##### 1. Authenticate with Docker Hub
If you are already loggedin using `docker login` command, then the token in docker engine config will be used. Otherwise you will be prompted to enter username and password.

##### 2. Querying an organization for repositories
To query repositories in an organization use `repos` argument. The organization to query can be passed as `--orgname` or `-o` parameter.
eg: Get repos in organization named "docker"
```sh
docker-hub repos --orgname docker
```

##### 3. Querying the tags of a repository
To query tags of a repository use `tags` argument. The organization of repository can be passed as `--orgname` or `-o` parameter. The repository to query can be passed as `--reponame` or `-r` parameter.
eg: Get tags of repository "ucp" in organization named "docker"
```sh
docker-hub tags --orgname docker --reponame ucp
```

##### 4. Querying a user profile
To query a user profile use `users` argument. The username to query can be passed as `--username` or `-u` parameter.
eg: Get profile of user named "docker"
```sh
docker-hub users --username docker
```

##### 5. Querying the auto-builds of a repository
To query auto-builds of a repository use `builds` argument. The organization of repository can be passed as `--orgname` or `-o` parameter. The repository to query can be passed as `--reponame` or `-r` parameter.
eg: Get build of repository "ucp" in organization named "docker"
```sh
docker-hub builds --orgname docker --reponame ucp
```

##### 6. Querying an organization for auto-build queue
To query the auto-build repositories with pending builds use the `queue` argument. The organization to query can be passed as `--orgname` or `-o` parameter.
eg: Get the building queue for organization named "docker"
```sh
docker-hub queue --orgname docker
```

##### Notes:
* Only 15 results will be displayed at once. You can fetch remaining pages by passing `--page` or `-p` parameter.

  eg: Get 3rd page
  ```sh
  docker-hub repos --orgname docker --page 3
  ```
* The results can be displayed in 2 formats:
  1. json - Displays result as JSON string.
  2. table - Displays results as nicely formatted table.

  `--format` or `-f` parameter can be used to specify the format in which result must be displayed.

  eg:
  * Display in json format
  ```sh
  docker-hub repos --orgname docker --format json
  ```

  * Display in table format
  ```sh
  docker-hub repos --orgname docker --format table
  ```

## Development
Questions, problems or suggestions? Please post them on the [issue tracker](https://github.com/amalfra/docker-hub/issues).

You can contribute changes by forking the project and submitting a pull request. Feel free to contribute :heart_eyes:

UNDER MIT LICENSE
=================
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
