# bazel-workspaces-python
Generator of Bazel workspaces for installed Python modules.

## Motivation

There is a difference in how software is build in Linux distributions and in
projects using Bazel.

The most of software built by Bazel usually bundles Python libraries or installs
them with pip.

However, that approach doesn't work so well for Linux distributions. In distros
like (open)SUSE we need to ensure that updates or security fixes for the
particular library are applied only once to have the effect on all packages and
the whole operating system. That's why globally available libraries and
packaging of Python modules the best approach for us.

This project is used by us for generating Bazel workspaces for globally
installed Python modules.

## Example

Example usage of bazel-workspaces-python to generate a Bazel workspace for
markupsafe package is::

```
$ bazel-workspaces-python markupsafe
```

Which generates the Bazel workspace for markupsafe in
`~/bazel_py_modules/markupsafe`, where `~/bazel_py_modules` is a default
directory for storing workspaces.

That directory can be changed by the command line argument:

```
$ bazel-workspaces-python --main-directory ~/my_py_workspaces
```

Or by the environment variable `BAZEL_W_P_MAIN_DIRECTORY`:

```
$ export BAZEL_W_P_MAIN_DIRECTORY=$HOME/my_py_workspace
$ bazel-workspaces-python markupsafe
```

The main goal of bazel-workspaces-python is to build projects using Bazel using
Python dependencies installed in system, not from pip or as bundled tarballs.
For that purpose, an example of using bazel-workspaces-python in rpmspec is:

```
%prep
[...]
export BAZEL_W_P_MAIN_DIRECTORY=%{_sourcedir}/repos
bazel-workspaces-python markupsafe
[...]

%build
bazel build \
    --override_repository="markupsafe=%{_sourcedir}/repos/markupsafe" \
    //...
```

In future we might provide a set of macros for building Bazel projects which
will be built on top of bazel-workspaces-python and hide explicit usage of
bazel-workspace-python and `--override_repository` argument from packagers.

## Running tests

This project uses [tox](https://tox.readthedocs.io/en/latest/) for running tests
and linting code. After installing it, it's enough to execute in the simpliest
way:

```
tox
```
