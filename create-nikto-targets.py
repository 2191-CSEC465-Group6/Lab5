import sys
import os
import subprocess
import argparse
import defusedxml


def _writeToTXT(file):
    if os.path.exists(file):
        os.remove(file)
    f = open(file, "a")
    return f


def _parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "targets", help="targets can be hostnames, IP addresses, networks, etc."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="nikto-targets.txt",
        help="output filename (default: %(default)s)",
    )

    return parser.parse_args(args)


def main():
    args = _parse_args(sys.argv[1:])

    txt_writer = _writeToTXT(args.output)

    process = subprocess.run(
        ["nmap", "--open", "-oX", "-", args.targets],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )

    tree = defusedxml.ElementTree.fromstring(process.stdout)
    for host in tree.findall("host"):
        ip_addr = host.find("address").get("addr")
        for port in host.find("ports").findall("port"):
            port_id = port.get("portid")
            txt_writer.write(ip_addr + ":" + port_id + "\n")


if __name__ == "__main__":
    main()
