import socket
import time
import threading
import sys
import subprocess
import os
import sysdef.util
import logging
try:
    import ssh2.session
except ImportError:
    logging.warn("SSH not available - you will not be able to control VMs")

try:
    import colorama
except ImportError:
    logging.warn("colorama not available - no pretty colours")

this = sys.modules[__name__]
#
# host_ssh_port = 6666
this.qemu_daemon_thread = None

host_ssh_port = 6666


def msg(msg):
    print(colorama.Style.RESET_ALL + msg)


def ssh_session():
    host = 'localhost'
    user = "root"

    i = 0
    connected = False
    session = None
    sock = None
    while not connected and i < 300 and this.qemu_daemon_thread.is_alive():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, host_ssh_port))
            msg("connected!")
            session = ssh2.session.Session()
            session.set_timeout(2000)
            session.handshake(sock)
            msg("handshake ok, ssh up")
            connected = True
        except Exception as e:
            pass
            i += 1
            time.sleep(1)
            msg(f"waiting for ssh... {e}")
            sock.close()

    if not connected:
        raise RuntimeError(f"Timeout: SSH to {host}:{host_ssh_port}")
    msg("We're in...")
    # time.sleep(120)
    # msg("make a new socket and start again")
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((host, host_ssh_port))
    # session = ssh2.session.Session()
    # ses.set_timeout(SSH_COMMAND_TIMEOUT)
    # msg("handshake...")
    # session.handshake(sock)

    # root no password oh yea ;-)
    msg("login...")
    session.userauth_password(user, '')

    session.set_timeout(0)
    return session

# def sd_image():
#     this.qemu_daemon_thread = threading.Thread(target=start_qemu, args=[False])
#     this.qemu_daemon_thread.start()
#     ssh_session()
#     this.qemu_daemon_thread.join()


def start_qemu(image_file, temp_overlay_image=None, interactive=False, rootfs_label="rootfs"):
    # strip colors from windows
    #colorama.init()

    print("YOU ARE HERE ---->" + sysdef.util.run("pwd"))


    qemu="/usr/bin/qemu-system-aarch64"
    sdcard=image_file #"/home/geoff/github/sysdef/sdcard.img"
    newdrive=temp_overlay_image #"/home/geoff/github/sysdef/overlay.img"
    drive=f"file={sdcard},if=none,index=0,media=disk,format=raw,id=hd0"
    drive2=f"file={newdrive},if=none,index=1,media=disk,format=raw,id=hd1"
    memory="1024"
    cpu="cortex-a53"
    kernel="/home/geoff/github/sysdef/Image"

    rootfs_uuid = sysdef.disk_image.get_uuid_for_label(sdcard, rootfs_label)


    # have to use the partition UUID not the label (not available)
    # https://unix.stackexchange.com/a/406463/360416
    qemu_command = f"""
    {qemu} \
        -m {memory}m \
        -M virt \
        -cpu {cpu} \
        -nographic \
        -smp 1 \
        -kernel {kernel} \
        -append "rootwait root=PARTUUID={rootfs_uuid} console=ttyAMA0 cgroup_enable=memory swapaccount=1" \
        -netdev "user,id=eth0,hostfwd=tcp::{host_ssh_port}-:22" \
        -device "virtio-net-device,netdev=eth0" \
        -drive {drive} \
        -device "virtio-blk-device,drive=hd0" \
        """
    if temp_overlay_image:
        logging.debug("starting QEMU with additional overlay: %s", temp_overlay_image)
        qemu_command += f"""
        -drive {drive2} \
        -device "virtio-blk-device,drive=hd1"
        """
    logging.debug(f"Final qemu command: {qemu_command}")
    qemu_command = qemu_command.replace('\n', '')

    # see also: https://sarge.readthedocs.io/en/latest/overview.html
    # http://eyalarubas.com/python-subproc-nonblock.html

    process = subprocess.Popen(qemu_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
    #     #while (process.poll() == None):
    output_thread = threading.Thread(target=stream, args=[process, interactive])
    output_thread.start()


    output_thread.join()
    #process.wait()
#        # while(process.stdout.readline)
        # for line in iter(process.stdout.readline, b''):  # replace '' with b'' for Python 3
        #     #sys.stdout.write(line)
        #     #msg(line.decode("utf-8"), end='', flush=True)
        #     threading.Thread(target=lambda a: msg("Hello, {}".format(a)), args=(["world"]))
        #     stdout.write(line)
        #     stdout.flush()


    # fixme - detect premature exit/error here
    msg('qemu exited')


def stream(process, interactive):
    with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:

        while (process.poll() == None):
            if not interactive:
                stdout.write(bytes(colorama.Style.DIM, 'utf-8'))
            stdout.write(process.stdout.read(1))
            stdout.flush()
        msg("finished streaming")


# def ssh_status():
#     s = socket.socket()
#
#     prev_status = False
#
#     while True:
#         try:
#             s.connect(("localhost", host_ssh_port))
#             this_status = True
#         except Exception as e:
#             this_status = False
#         finally:
#             s.close()
#
#         if this_status != prev_status:
#             msg("******************************")
#             msg(f"    ssh status change: {this_status}")
#             msg("******************************")
#             prev_status = this_status
#         time.sleep(1)


# ~~~
# def start_emulator_and_get_ssh_session():
#     this.qemu_daemon_thread = threading.Thread(target=start_qemu, args=[False])
#     this.qemu_daemon_thread.start()
#     ssh_session()
#     this.qemu_daemon_thread.join()

def start_emulator_and_get_ssh_session(image_file, temp_overlay_image=None):

    # start qemu
    this.qemu_daemon_thread = threading.Thread(target=start_qemu, args=[image_file, temp_overlay_image])
    this.qemu_daemon_thread.start()

    # wait for session to come back...
    return ssh_session()


def start_emulator_interactive(image_file):
    # start qemu
    this.qemu_daemon_thread = threading.Thread(target=start_qemu, args=[image_file])
    this.qemu_daemon_thread.start()

    # wait for emulator session to end (poweroff inside VM)
    this.qemu_daemon_thread.join()



def command(session, cmd, check=True):
    logging.debug("SSH> %s", cmd)
    channel = session.open_session()
    channel.execute(cmd)
    size, data = channel.read()
    while size > 0:
        logging.debug(data.decode())
        size, data = channel.read()
    channel.close()
    exit_status = channel.get_exit_status()
    logging.debug("...result: %s", exit_status)

    if check and exit_status != 0:
        raise RuntimeError(f"Error: command '{cmd}' returned exit status {exit_status}")
    return exit_status


def stop_emulator(session):
    channel = session.open_session()
    channel.execute(f"poweroff 2>&1")
    try:
        size, data = channel.read()
        while size > 0:
            logging.debug(data.decode())
            size, data = channel.read()
        channel.close()
    except ssh2.exceptions.SocketRecvError:
        logging.info("Emulator is shut down...")
