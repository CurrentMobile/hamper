Hamper
====
A CLI for the iOS Provisioning Portal. Fix the broken part of your iOS development workflow.

The end goal for hamper is to have one command line utlity to manage your certificates, provisioning profiles and app IDs. It's a work in progress...

### Under the hood
Hamper uses [Selenium (with Python bindings)](http://selenium-python.readthedocs.org/installation.html) and [PhantomJS](http://phantomjs.org/) to go through the provisioning portal and execute requests. We're also using [docopt](http://docopt.org/) to build the actual CLI. Thus, these three libraries are required for running Hamper. I'll add a requirements.txt for the v1.0 release.