import os
from pathlib import Path

from dotenv import load_dotenv

from scapy.all import (
    Ether,
    ICMP,
    IP,
    Raw,
    TCP,
    wrpcap,
)


# =========================================================
# PATHS / ENVIRONMENT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)


stage5_flag = os.getenv(
    "STAGE5_FLAG"
)


if not stage5_flag:

    raise RuntimeError(
        "STAGE5_FLAG is missing from .env"
    )


OUTPUT_DIR = (
    BASE_DIR
    / "challenges"
    / "stage05"
)


OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE = (
    OUTPUT_DIR
    / "traffic_capture.pcap"
)


# =========================================================
# PACKET STORAGE
# =========================================================

packets = []

current_time = 1770000000.0


SERVER_IP = "172.16.18.50"

SERVER_MAC = "02:00:00:00:18:50"


# =========================================================
# PACKET TIMESTAMP HELPER
# =========================================================

def add_packet(packet):

    global current_time

    packet.time = current_time

    current_time += 0.05

    packets.append(
        packet
    )


# =========================================================
# TCP CONVERSATION GENERATOR
# =========================================================

def add_http_conversation(
    client_ip,
    client_mac,
    source_port,
    request_data,
    response_body,
    client_sequence,
    server_sequence
):

    request_bytes = (
        request_data.encode(
            "utf-8"
        )
    )


    body_bytes = (
        response_body.encode(
            "utf-8"
        )
    )


    response_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Server: CyberLearn-Training\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )


    response_bytes = (
        response_headers.encode(
            "utf-8"
        )
        + body_bytes
    )


    # -----------------------------------------------------
    # TCP SYN
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=client_mac,
            dst=SERVER_MAC
        )

        /

        IP(
            src=client_ip,
            dst=SERVER_IP
        )

        /

        TCP(
            sport=source_port,
            dport=80,
            flags="S",
            seq=client_sequence
        )
    )


    # -----------------------------------------------------
    # SYN / ACK
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=SERVER_MAC,
            dst=client_mac
        )

        /

        IP(
            src=SERVER_IP,
            dst=client_ip
        )

        /

        TCP(
            sport=80,
            dport=source_port,
            flags="SA",
            seq=server_sequence,
            ack=client_sequence + 1
        )
    )


    # -----------------------------------------------------
    # ACK
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=client_mac,
            dst=SERVER_MAC
        )

        /

        IP(
            src=client_ip,
            dst=SERVER_IP
        )

        /

        TCP(
            sport=source_port,
            dport=80,
            flags="A",
            seq=client_sequence + 1,
            ack=server_sequence + 1
        )
    )


    # -----------------------------------------------------
    # HTTP REQUEST
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=client_mac,
            dst=SERVER_MAC
        )

        /

        IP(
            src=client_ip,
            dst=SERVER_IP
        )

        /

        TCP(
            sport=source_port,
            dport=80,
            flags="PA",
            seq=client_sequence + 1,
            ack=server_sequence + 1
        )

        /

        Raw(
            load=request_bytes
        )
    )


    request_end = (
        client_sequence
        + 1
        + len(request_bytes)
    )


    # -----------------------------------------------------
    # ACK REQUEST
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=SERVER_MAC,
            dst=client_mac
        )

        /

        IP(
            src=SERVER_IP,
            dst=client_ip
        )

        /

        TCP(
            sport=80,
            dport=source_port,
            flags="A",
            seq=server_sequence + 1,
            ack=request_end
        )
    )


    # -----------------------------------------------------
    # HTTP RESPONSE
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=SERVER_MAC,
            dst=client_mac
        )

        /

        IP(
            src=SERVER_IP,
            dst=client_ip
        )

        /

        TCP(
            sport=80,
            dport=source_port,
            flags="PA",
            seq=server_sequence + 1,
            ack=request_end
        )

        /

        Raw(
            load=response_bytes
        )
    )


    response_end = (
        server_sequence
        + 1
        + len(response_bytes)
    )


    # -----------------------------------------------------
    # ACK RESPONSE
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=client_mac,
            dst=SERVER_MAC
        )

        /

        IP(
            src=client_ip,
            dst=SERVER_IP
        )

        /

        TCP(
            sport=source_port,
            dport=80,
            flags="A",
            seq=request_end,
            ack=response_end
        )
    )


    # -----------------------------------------------------
    # FIN
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=SERVER_MAC,
            dst=client_mac
        )

        /

        IP(
            src=SERVER_IP,
            dst=client_ip
        )

        /

        TCP(
            sport=80,
            dport=source_port,
            flags="FA",
            seq=response_end,
            ack=request_end
        )
    )


    # -----------------------------------------------------
    # FINAL ACK
    # -----------------------------------------------------

    add_packet(

        Ether(
            src=client_mac,
            dst=SERVER_MAC
        )

        /

        IP(
            src=client_ip,
            dst=SERVER_IP
        )

        /

        TCP(
            sport=source_port,
            dport=80,
            flags="A",
            seq=request_end,
            ack=response_end + 1
        )
    )


# =========================================================
# BACKGROUND ICMP TRAFFIC
# =========================================================

for number in range(3):

    add_packet(

        Ether(
            src="02:00:00:00:18:21",
            dst=SERVER_MAC
        )

        /

        IP(
            src="172.16.18.21",
            dst=SERVER_IP
        )

        /

        ICMP(
            type=8,
            id=100 + number,
            seq=number
        )

        /

        Raw(
            load=b"CyberLearn ping test"
        )
    )


# =========================================================
# HTTP STREAM 1 - DISTRACTOR
# =========================================================

request_1 = (
    "GET /status HTTP/1.1\r\n"
    "Host: training.cyberlearn.local\r\n"
    "User-Agent: CyberLearn-Monitor/1.0\r\n"
    "Accept: */*\r\n"
    "\r\n"
)


response_1 = (
    "CyberLearn Training Server\n"
    "Status: ONLINE\n"
    "Service health: NORMAL\n"
)


add_http_conversation(

    client_ip="172.16.18.21",

    client_mac="02:00:00:00:18:21",

    source_port=41001,

    request_data=request_1,

    response_body=response_1,

    client_sequence=1000,

    server_sequence=5000
)


# =========================================================
# HTTP STREAM 2 - IMPORTANT INVESTIGATION STREAM
# =========================================================

request_2 = (
    "GET /investigation/report?id=42 HTTP/1.1\r\n"
    "Host: training.cyberlearn.local\r\n"
    "User-Agent: Analyst-Workstation/2.6\r\n"
    "X-Case-ID: CL-NET-05\r\n"
    "Accept: text/plain\r\n"
    "\r\n"
)


response_2 = (
    "CYBERLEARN NETWORK INVESTIGATION\n"
    "================================\n"
    "\n"
    "Case ID: CL-NET-05\n"
    "Status: Recovered\n"
    "\n"
    "Investigation Marker:\n"
    f"{stage5_flag}\n"
    "\n"
    "NEXT_CLUE:\n"
    "The final problem begins where ordinary "
    "permissions end.\n"
)


add_http_conversation(

    client_ip="172.16.18.77",

    client_mac="02:00:00:00:18:77",

    source_port=42318,

    request_data=request_2,

    response_body=response_2,

    client_sequence=2000,

    server_sequence=7000
)


# =========================================================
# HTTP STREAM 3 - DISTRACTOR
# =========================================================

request_3 = (
    "GET /downloads/manual.txt HTTP/1.1\r\n"
    "Host: training.cyberlearn.local\r\n"
    "User-Agent: Mozilla/5.0\r\n"
    "Accept: text/plain\r\n"
    "\r\n"
)


response_3 = (
    "CyberLearn User Manual\n"
    "\n"
    "Remember to follow standard security procedures.\n"
    "This document contains no investigation markers.\n"
)


add_http_conversation(

    client_ip="172.16.18.44",

    client_mac="02:00:00:00:18:44",

    source_port=43550,

    request_data=request_3,

    response_body=response_3,

    client_sequence=3000,

    server_sequence=9000
)


# =========================================================
# EXTRA BACKGROUND ICMP
# =========================================================

for number in range(2):

    add_packet(

        Ether(
            src="02:00:00:00:18:12",
            dst=SERVER_MAC
        )

        /

        IP(
            src="172.16.18.12",
            dst=SERVER_IP
        )

        /

        ICMP(
            type=8,
            id=200 + number,
            seq=number
        )

        /

        Raw(
            load=b"routine network check"
        )
    )


# =========================================================
# WRITE PCAP FILE
# =========================================================

wrpcap(
    str(OUTPUT_FILE),
    packets
)


# =========================================================
# SUCCESS
# =========================================================

print(
    "Stage 05 challenge created successfully:"
)

print(
    OUTPUT_FILE
)

print(
    f"Total packets created: {len(packets)}"
)