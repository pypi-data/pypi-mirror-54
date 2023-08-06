# Docker Compose

This is a very simple docker compose setup that demonstrates usage and deployment of `mail-relay` tool daemon process.

Compose file provisions a single service `relay` built from `relay:${VERSION}` docker image.
You can either build this package locally `cd ${repo-root} && make build-docker-runtime` or fetch your desired version from https://hub.docker.com.



You can bring up relay daemon service using:

```shell
> cd ${repo-root}/deployments
> docker-compose up -d
```

If you are willing provision specific version of `mail-relay`, You can set `VERSION` environment variable or configure default `.env` to your desired version.



`relay` daemon process works with a persistent data store, provided to it via `relay --store-path ${PATH}`. For demonstration purposes this compose setup mounts `${repo-root}/deployment/store ` to `relay` container. You should conifgure volume mapping, configuration, backup and ... to fit your specific requirements and security considerations. **Note that provisioned volume will contain a sqlite database which holds connection credentials, exporter/approver private keys as well as relay application state. Therefore, its security and peristency is vital.**



#### Configuration

You would need to configure `relay` tool to use appropriate configurations. You can configure your relay setup by bringing up ephemral containers to configure the designated store. Following command creates an ephemeral container with which you can configure your setup. This can be down while the daemon `relay` service is up and running.

```shell
> docker-compose run --rm relay --help
```

On a fresh deployment, you need to configure relay daemon with credentials, preveil server info, smtp/imap credentials and lastly your organization export group.

###### configure relay tool to use your designated configuration. configs is also mounted to relay container in this compose setup.

```shell
> docker-compose run --rm relay config --config-file ./config/sample.yml
```

###### configure relay exporter and approvers

```shell
> docker-compose run --rm relay config exporter ${exporter-user-id}
> docker-compose run --rm relay config approver ${approver-user-id}
> ...
```

 Upon successful configuration, relay service should automatically pick up the information and start relaying mails.



#####  Other configuration, tuning or status checks

Using the same ephemeral container, you can monitor status of relay service and more:

```shell
> docker-compose run --rm relay status
> docker-compose run --rm relay --help
```











