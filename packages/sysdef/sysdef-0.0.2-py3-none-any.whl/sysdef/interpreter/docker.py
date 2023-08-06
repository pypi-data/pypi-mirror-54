import logging
import sysdef.util

"""
| step      | image | image need VM | boot | notes                                      |
| ---       | ---   | ---           | ---  | ---                                        |
| settings  | Y     | N             | Y    | restart docker in boot mode                |
| images    | Y     | Y             | Y    | image mode does docker pull if cache==true |
| run       | N     | N/A           | Y    |                                            |
:param data:
:param g:
:return: void
"""


# docker client API is available but we're not using it for
# simplicity since the API calls can be somewhat different to
# `docker run`

def process_1(data, g=None):
    root = ""
    changes = False
    etc_docker = root + "/etc/docker"
    etc_docker_daemon_yaml = etc_docker + "/daemon.json"

    daemon_json = data.get("daemon_json", {})
    if daemon_json:
        logging.info("saving /etc/docker/daemon.json...")
        changes |= sysdef.util.mkdir(etc_docker, g=g)
        changes |= sysdef.util.save_json(etc_docker_daemon_yaml, daemon_json, g=g)

    return changes


def process_2(data, ssh_session):
    cache = data.get("cache", True)

    # need to somehow look-ahead to the boot section and grab the images from
    # there
    if cache:
        boot_docker = sysdef.lookup("boot", "docker")
        docker_containers = boot_docker.get("containers", {})

        for name in docker_containers:
            # docker client API is available but we're not using it for
            # simplicity since the API calls are very different to `docker run`
            logging.info(f"downloading image: {name}")
            settings = docker_containers[name]
            image = settings['image']

            logging.info("waiting for docker service to start...")
            sysdef.emulator.command(
                ssh_session,
                'while [[ ! $(docker ps) ]] ; do echo wait; sleep 1 ; done'
                # systemctl reports active as soon as service is loading
                #'while [[ $(systemctl is -active docker) != "active"]]; do echo wait; done'
            )

            logging.info("pulling docker image: %s...", image)

            exit_status = sysdef.emulator.command(ssh_session, f"docker pull {image} 2>&1")
            if exit_status != 0:
                logging.error(f"...Exited with status {exit_status}")
    else:
        logging.info("not caching images - disabled")


def process(data):
    """
    runtime docker setup
    """
    logging.info("processing docker section...")
    if process_1(data):
        sysdef.util.run("systemctl daemon-reload")
        sysdef.util.run("systemctl restart docker")

    docker_containers = data.get("containers", {})

    for name in docker_containers:
        logging.info(f"processing {name}")
        settings = docker_containers[name]
        image = settings['image']
        docker_args = settings.get("run", "--restart unless-stopped --publish-all")
        container_args = settings.get("args", "")

        # check if container exists
        container_id = sysdef.util.run(f"docker ps -aq -f name={name}")
        if container_id:
            logging.info(f"{name} exists as {container_id}... moving on")
            # FIXME - see if we need to update run arguments
        else:
            logging.info(f"starting docker container for {name}...")
            docker_run_cmd = f"docker run --detach {docker_args} --name {name} {image} {container_args}"
            sysdef.util.run(docker_run_cmd)

    port_forwards = data.get("port_forwards", {})
    for host_port in port_forwards:
        settings = port_forwards[host_port]
        container_port = settings.get("container_port")
        protocols = settings.get("protocols",["tcp"])

        logging.info(f"port forward {host_port}/{protocols} -> container:{container_port}/{protocols}")

        for protocol in protocols:
            docker_ip = sysdef.util.run("docker network inspect -f '{{(index .IPAM.Config 0).Gateway}}' bridge")

            iptables_a = f"iptables -t nat -A PREROUTING -p {protocol} --dport {host_port} -j DNAT --to-destination {docker_ip}:{container_port}"
            iptables_b = f"iptables -A FORWARD -p {protocol} -d {docker_ip} --dport {host_port} -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT"

            logging.info("enabling docker port forward for %d/%s", host_port, protocol)

            sysdef.util.run(iptables_a)
            sysdef.util.run(iptables_b)
