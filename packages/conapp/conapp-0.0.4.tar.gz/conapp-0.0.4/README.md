# conapp - The easy config applier

A simple project for applying config files from repos/tar files

#### Example command:
```
conapp apply -u drew887 -b
```

The above will:
  * download a tarball from drew887's config repo on bitbucket *(-b)*
  * take a backup of all the files that are listed in the tarball that you
    also have locally on your system
  * untar the repo into your home directory.
