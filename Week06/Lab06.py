# ============================================================
#  WEEK 06 LAB: NETWORK DIAGNOSTIC LOGGER
#  COMP2152 — Windows
#  Muhammad-Amin Farhan Ali
# ============================================================

import subprocess
import csv
from datetime import datetime


# -------------------- SYSTEM COMMANDS --------------------

def run_ping(host):
    result = subprocess.run(
        ["ping", "-n", "3", host],
        capture_output=True, text=True
    )
    return result.stdout


def run_nslookup(domain):
    result = subprocess.run(
        ["nslookup", domain],
        capture_output=True, text=True
    )
    return result.stdout


def get_network_info():
    result = subprocess.run(
        ["ipconfig", "/all"],
        capture_output=True, text=True
    )
    return result.stdout


def get_arp_table():
    result = subprocess.run(
        ["arp", "-a"],
        capture_output=True, text=True
    )
    return result.stdout


def get_hostname():
    result = subprocess.run(
        ["hostname"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


# -------------------- PARSING --------------------

def parse_ping(output):
    stats = {
        "transmitted": 0,
        "received": 0,
        "loss": "100%",
        "avg_ms": "N/A",
        "status": "Failed"
    }

    for line in output.splitlines():
        if "Sent =" in line and "Received =" in line:
            parts = line.split(",")
            for part in parts:
                if "Sent" in part:
                    stats["transmitted"] = int(part.split("=")[1])
                if "Received" in part:
                    stats["received"] = int(part.split("=")[1])
                if "%" in part:
                    stats["loss"] = part.split("%")[0].strip("() ") + "%"

        if "Average" in line:
            stats["avg_ms"] = line.split("=")[-1].replace("ms", "").strip()

    if stats["received"] > 0:
        stats["status"] = "Success"

    return stats


def parse_nslookup(output):
    result = {"ip": "Not found", "status": "Failed"}
    found = False

    for line in output.splitlines():
        if "Non-authoritative answer" in line:
            found = True
        if found and "Address:" in line:
            ip = line.split("Address:")[1].strip()
            if "." in ip:
                result["ip"] = ip
                result["status"] = "Success"
                break

    return result


def parse_mac_address(output):
    info = {"mac": "Not found", "ip": "Not found"}

    for line in output.splitlines():
        if "Physical Address" in line:
            info["mac"] = line.split(":")[1].strip()
        if "IPv4 Address" in line:
            info["ip"] = line.split(":")[-1].replace("(Preferred)", "").strip()

    return info


def parse_arp_table(output):
    devices = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2 and "." in parts[0]:
            devices.append({"ip": parts[0], "mac": parts[1]})
    return devices


# -------------------- TEXT FILES (TASK 1) --------------------

def write_to_log(filename, entry):
    with open(filename, "a") as file:
        file.write(entry + "\n")


def read_log(filename):
    with open(filename, "r") as file:
        return file.read()


def log_command_result(command, target, output, filename):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{time}] {command} {target}\n{output}" + "-" * 40
    write_to_log(filename, entry)


# -------------------- CSV FILES (TASK 2) --------------------

LOG_FILE = "diagnostics.csv"


def log_to_csv(filename, command, target, result, status):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time, command, target, result, status])


def read_csv_log(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            print(" | ".join(row))


def analyze_csv_log(filename):
    with open(filename, "r", newline="") as file:
        rows = list(csv.reader(file))

    if not rows:
        print("Log is empty.")
        return

    print("Total entries:", len(rows))

    cmds = {}
    results = {}

    for row in rows:
        cmds[row[1]] = cmds.get(row[1], 0) + 1
        results[row[4]] = results.get(row[4], 0) + 1

    print("\nCommands:")
    for c in cmds:
        print(" ", c, cmds[c])

    print("\nResults:")
    for r in results:
        print(" ", r, results[r])


# -------------------- SAFE READ (TASK 3) --------------------

def safe_read_log(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()

        if content == "":
            print("Log file is empty.")
            return ""

        return content

    except FileNotFoundError:
        print("No log file found. Run a diagnostic first.")
        return ""

    finally:
        print("Log read attempt completed.")


# -------------------- MENU + MAIN --------------------

def display_menu():
    print("\n1. Ping")
    print("2. DNS Lookup")
    print("3. Network Info")
    print("4. ARP Table")
    print("5. View Log")
    print("6. Analyze Log")
    print("7. Quit")


def main():
    print("Network Diagnostic Logger")
    print("Running on:", get_hostname())

    while True:
        display_menu()
        choice = input("Choice (1-7): ")

        if choice == "1":
            host = input("Host: ")
            out = run_ping(host)
            data = parse_ping(out)
            log_to_csv(LOG_FILE, "ping", host, data["avg_ms"], data["status"])
            log_command_result("PING", host, out, "network_log.txt")

        elif choice == "2":
            domain = input("Domain: ")
            out = run_nslookup(domain)
            data = parse_nslookup(out)
            log_to_csv(LOG_FILE, "nslookup", domain, data["ip"], data["status"])

        elif choice == "3":
            info = parse_mac_address(get_network_info())
            log_to_csv(LOG_FILE, "ipconfig", "all", info["mac"], "Captured")

        elif choice == "4":
            devices = parse_arp_table(get_arp_table())
            log_to_csv(LOG_FILE, "arp", "local", len(devices), "Captured")

        elif choice == "5":
            read_csv_log(LOG_FILE)

        elif choice == "6":
            analyze_csv_log(LOG_FILE)

        elif choice == "7":
            print("Done.")
            break


main()