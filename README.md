Hamper
====
A CLI for the iOS Provisioning Portal. Fix the broken part of your iOS development workflow.

The end goal for hamper is to have one command line utlity to manage your certificates, provisioning profiles and app IDs. It's a work in progress...

Requirements
===

Hamper requires [PhantomJS](http://phantomjs.org/), [Selenium](http://selenium-python.readthedocs.org/installation.html), [docopt](http://docopt.org/), [keyring](https://pypi.python.org/pypi/keyring) and [termcolor](https://pypi.python.org/pypi/termcolor). The latter four are automatically installed automatically by Pypi (the recommended installation method). 

You will need to install PhantomJS yourself. We recommend Homebrew:

```
brew install phantomjs
```

Installation
===
Hamper is distributed via [pip](https://pypi.python.org/pypi)! So, once you have PhantomJS installed, all you need do is:

```
sudo pip install hampercli
```

Usage
===

## Authentication
```
hamper auth login --email you@email.com --password your_pass
```
Your login details will then be saved to the keychain. Once you've logged, Hamper will use the saved credentials for subsequent requests.

## Certificates
Generate development, distribution and push notification certificates.

```
hamper cert create CERT_TYPE --csr_path /path/to/csr/file --cert_path /path/where/cert/is/saved --bundle_id app_ID
```

CERT_TYPE is the type of certificate to be generated. The available options are:

* development
* distribution
* development_push
* distribution_push

Generating push certificates requires the optional ```bundle_id``` argument.

## Identifiers
Generate app IDs with any combination of enabled services.

```
hamper identifier create --app_name my_app --bundle_id com.kp.my_app --enabled_services push
```

```enabled_services``` is an optional parameter used to add services to the app. The available options are:

* app_groups
* accociated_domains
* data_protection
* health_kit
* home_kit
* wireless_accessory_config
* icloud
* inter_app_audio
* passbook

## Profiles
Generate a provisioning profile for an app ID registered on your account.

### Development

```
hamper profile create development --name my_dev_profile --bundle_id com.kp.my_app --profile_path /my/destination/path.mobileprovision
```

### Ad Hoc

Ad Hoc profiles need to be signed with one specifc distribution certificate (whereas development profiles can select all). To pick the certificate to sign with, pass the `exp_day`, `exp_month`, and `exp_year` arguments for the date of the certificate you want to pick.

```
hamper profile create ad_hoc --name my_adhoc_profile --bundle_id com.kp.my_app --profile_path /my/destination/path.mobileprovision --exp_day= 20 --exp_month 04 --exp_year 2015
```

### App Store

App Store profiles need to be signed with one specifc distribution certificate (whereas development profiles can select all). To pick the certificate to sign with, pass the `exp_day`, `exp_month`, and `exp_year` arguments for the date of the certificate you want to pick.

```
hamper profile create app_store --name my_appstore_profile --bundle_id com.kp.my_app --profile_path /my/destination/path.mobileprovision --exp_day= 20 --exp_month 04 --exp_year 2015
```
