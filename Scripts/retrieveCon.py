import sys
import subprocess

NetCons = []

class NetworkConnection:

    def __init__(self, localAddr, localPort, remoteAddr, remotePort, state, pid):
        self.localAddr = localAddr
        self.localPort = localPort

        self.remoteAddr = remoteAddr
        self.remotePort = remotePort
        
        self.state = state
        self.pid = pid

    def printConnection(self):
        print(f"[i] Connection:\t{self.localAddr:>16}:{self.localPort}", end="")
        print(f"\t\t-->\t{self.remoteAddr:>16}:{self.remotePort}", end="")
        print(f"\t\t{self.state:<12}\t{self.pid:>7}")

def retrieveConnections():
    try:
        cmd = ["netstats", "-ano", "-p",  "tcp"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1)

        print(f"[i] Executing command: {' '.join(cmd)}")

        lines = []
        for line in proc.stdout:
            lines.append(line.strip())

        return_code = proc.wait()
        print(f"[i] Process finished with return code: {return_code}")

        # print("[i] Output: ")

        for line in lines:
            if "TCP" in line:
                spLine = line.split()

                localA = spLine[1].split(":")[0]
                localP = spLine[1].split(":")[1]

                remoteA = spLine[2].split(":")[0]
                remoteP = spLine[2].split(":")[1]

                NetCons.append(NetworkConnection(localA, localP, remoteA, remoteP, spLine[3], spLine[4]))

    except FileNotFoundError:
        print(f"[!] Error: Command '{cmd[0]}' not found. ")
        exit(0)
    except Exception as e:
        print(f"[!] An error occured: {e}")
        exit(0)

if __name__ == "__main__":
    retrieveConnections()
    listenCount = 0
    establCount = 0
    for con in NetCons:
        if con.state == "LISTENING":
            listenCount = listenCount + 1
        if con.state == "ESTABLISHED":
            establCount = establCount + 1

        con.printConnection()


    print(f"[i] We have {listenCount} listening connection...")
    print(f"[i] We have {establCount} established connnections...")