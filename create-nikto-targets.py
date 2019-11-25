import subprocess
from defusedxml import ElementTree

# def _writeToTXT(file):
#     with open(filename, 'w') as f:

def main():
    ip_addr = "127.0.0.1"
    process = subprocess.run(
        ["nmap", "--open", "-oX", "-", ip_addr],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    
    tree = ElementTree.fromstring(process.stdout)
    for host in tree.findall('host'):
        addr = host.get('address')
        print(host)
        # print(ElementTree.tostring(host, encoding='utf8', method='xml').decode())


if __name__ == "__main__":
    main()
