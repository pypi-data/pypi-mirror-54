# Mail Relay [![CircleCI](https://circleci.com/gh/samantehrani/mail-relay.svg?style=shield&circle-token=3af48550b9a47883ad9f13b1060ddf6a3fa1ac41)](https://circleci.com/gh/samantehrani/mail-relay) [![PyPI version](https://badge.fury.io/py/mail-relay.svg)](https://badge.fury.io/py/mail-relay)

Mail Relay is a python tool that
*   uses **Export Group** of an organization to **decrypt** PreVeil encrypted emails
*   and **relays** them to a configurable IMAP or SMTP destination.



## Usage

Mail relay exposes a command line interface relay, with which you can configure your relay setup.

```shell
> relay start # start relay process
> relay status # check relay status
> relay config # configure your relay setup
```

See full [usage](./docs/usage.md).



## Release

**mail-relay** package is publish on https://pypi.org.
We also maintain versioned runtime container images of the tool on https://hub.docker.com.
You can check out version updates at [release notes](./docs/release_notes.md).



## Development

Check out our [development guide](./docs/development.md). Feel free to submit issues, or pull request to contibute.



## Deployment

Deployment and usage of relay tool is fairly trivial, due to the inherent simplicity of tool. That said, administrators need to be very cautious about security of this tool and their deployment. There is no single deployment setup that fits all, there few sample [deployment and usage](./docs/deployment.md) guidelines that we demonstrate the bare minimum requirements of relay tool.