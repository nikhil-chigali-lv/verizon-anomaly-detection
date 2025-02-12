# Data folder structure
# ├── data/
# │   ├── hbt/
# │   |   ├── hbt.nodes_wifi_hbt.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── wc_interface: num - Interface number
# │   |   |   ├── wc_current_ch: num - Current channel
# │   |   |   ├── wc_enable: bool - Enable status
# │   |   ├── hbt.nodes_wan_hbt.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── wan_data_ipv4_ip: str - WAN IP address
# │   |   ├── hbt.nodes_stations_hbt.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── stations_bs: num - Upload data
# │   |   |   ├── stations_br: num - Download data
# │   |   |   ├── stations_mode: num - Mode of the device
# │   |   |   ├── stations_signal_strength: num - Signal strength of the device
# │   |   |   ├── stations_tx_link_rate: num - Transmit link rate
# │   |   |   ├── stations_max_tx_phy_rate: num - Maximum transmit PHY rate
# │   |   |   ├── stations_link_rate: num - Link rate
# │   |   |   ├── stations_max_rx_phy_rate: num - Maximum receive PHY rate
# │   |   |   ├── stations_parent_id: str - Parent ID
# │   |   |   ├── stations_mode: num - Mode of the device
# │   |   |   ├── stations_airtime_utilization: num - Airtime utilization
# │   |   |   ├── stations_station_name: str - Station name
# │   |   |   ├── connect_type: str - Connection type {MoCA, Ether, 2.4G, 2.4G_guest, 5G, 5G_guest, 5G_iptv, 5G_H, 5G_H_guest, 5G_H_iptv, 6G, 6G_guest, 6G_iptv}
# │   |   ├── hbt.group_nodes_hbt.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── tplg_node_sta_num: num - Number of clients connected
# │   |   |   ├── tplg_node_type: num - Node type
# │   |   |   ├── tplg_node_son: bool - SON status
# │   ├── diag/
# │   |   ├── diag.nodes_speedtest_diag.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── ookla_result: dict - Speedtest results (Sample: {"SpeedTestType": "OoklaTCP", "TransactionID": "","OoklaServerID": "37686","TestResponse": "Completed","TestProgress": 100,"DownloadSpeed": "39.809355","UploadSpeed": "12.807557","Latency": "220.8 13000","PacketLossRate": "0.458716","Jitter": "1.246000","Download LatencyIQM": "359.915000","Download LatencyLow": "225.368000","Download LatencyHigh": "1190.148000","Download LatencyJitter": "81.475000","UploadLatencyIQM": "335.244000","UploadLatencyLow": "223.766000","Upload LatencyHigh": "470.672000","UploadLatencyJitter": "77.880000",})
# │   |   ├── diag.nodes_group_wifi_scan_diag.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── wifi_ap_band_info_band_id: str - Band ID {2.4G, 2.4G_guest, 5G, 5G_guest, 5G_iptv, 5G_H, 5G_H_guest, 5G_H_iptv, 6G, 6G_guest, 6G_iptv}
# │   |   |   ├── wifi_ap_band_info_channel: num - Channel number
# │   |   |   ├── wifi_ap_band_info_wifi_name: str - WiFi name
# │   |   |   ├── wifi_ap_band_info_bssid: str - BSSID (Format: xx:xx:xx:xx:xx:xx)
# │   |   ├── diag.nodes_acs_channelchange_diag.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── acs_bid: int - ACS BID
# │   |   |   ├── acs_primary_ch: int - Primary channel
# │   |   |   ├── acs_prev_ch: int - Previous channel
# │   |   |   ├── acs_reason: int - Reason for channel change
# │   ├── evt/
# │   |   ├── evt.nodes_station_evt.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── event_type: num - Event type
# │   |   ├── evt.stations_mesh_evt.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── event_type: num - Event type
# │   |   |   ├── event_action: num - Event action
# │   |   ├── evt.nodes_events_evt.csv
# │   |   |   ├── distid: str - Unique identifier for the row item (concatenate sn and createdts)
# │   |   |   ├── createdts: str - Timestamp of the data
# │   |   |   ├── sn: str - Device serial number
# │   |   |   ├── event_reason: num - Event reason

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from constants import DATA_DIR

# Set random seed for reproducibility
np.random.seed(42)

# Define base directory for synthetic data
base_dir = DATA_DIR / "synthetic_data"
sub_dirs = ["hbt", "diag", "evt"]
for sub_dir in sub_dirs:
    os.makedirs(os.path.join(base_dir, sub_dir), exist_ok=True)

# Define time range
num_devices = 10
num_days = 120  # 4 months
timestamps_per_day = 24  # One entry per hour
timestamps = [
    datetime(2024, 9, 1) + timedelta(hours=i)
    for i in range(num_days * timestamps_per_day)
]


def save_csv(df, subdir, filename):
    """Save DataFrame to a CSV file."""
    path = os.path.join(base_dir, subdir, filename)
    df.to_csv(path, index=False)
    return path


def random_ip():
    return f"192.168.{np.random.randint(0, 255)}.{np.random.randint(1, 255)}"


def random_mac():
    return ":".join([f"{np.random.randint(0, 255):02x}" for _ in range(6)])


def random_wifi_band():
    return np.random.choice(
        ["2.4G", "5G", "6G", "5G_guest", "6G_guest", "5G_iptv", "6G_iptv"]
    )


# Generate data
device_ids = [f"DEV_{i:03d}" for i in range(1, num_devices + 1)]

hbt_data_definitions = {
    "hbt.nodes_wifi_hbt.csv": [
        "distid",
        "createdts",
        "sn",
        "wc_interface",
        "wc_current_ch",
        "wc_enable",
    ],
    "hbt.nodes_wan_hbt.csv": ["distid", "createdts", "sn", "wan_data_ipv4_ip"],
    "hbt.nodes_stations_hbt.csv": [
        "distid",
        "createdts",
        "sn",
        "stations_bs",
        "stations_br",
        "stations_mode",
        "stations_signal_strength",
        "stations_tx_link_rate",
        "stations_max_tx_phy_rate",
        "stations_link_rate",
        "stations_max_rx_phy_rate",
        "stations_airtime_utilization",
        "stations_station_name",
        "connect_type",
        "stations_parent_id",  # Added missing column
    ],
    "hbt.group_nodes_hbt.csv": [
        "distid",
        "createdts",
        "sn",
        "tplg_node_sta_num",
        "tplg_node_type",
        "tplg_node_son",
    ],
}

# Generate Synthetic data - hbt
for filename, columns in hbt_data_definitions.items():
    subdir = "hbt"
    records = []
    for device in device_ids:
        for timestamp in timestamps[:: np.random.randint(1, 6)]:
            record = {
                "distid": f"{device}_{timestamp}",
                "createdts": timestamp,
                "sn": device,
            }
            for col in columns[3:]:
                if col == "wan_data_ipv4_ip":
                    record[col] = random_ip()
                elif col == "stations_station_name":
                    record[col] = f"Station_{np.random.randint(1, 10)}"
                elif col == "connect_type":
                    record[col] = np.random.choice(
                        [
                            "MoCA",
                            "Ether",
                            "2.4G",
                            "2.4G_guest",
                            "5G",
                            "5G_guest",
                            "5G_iptv",
                            "5G_H",
                            "5G_H_guest",
                            "5G_H_iptv",
                            "6G",
                            "6G_guest",
                            "6G_iptv",
                        ]
                    )
                elif col == "stations_parent_id":
                    record[col] = f"PARENT_{np.random.randint(1, 10)}"
                else:
                    record[col] = np.random.randint(1, 100)
            records.append(record)
    df = pd.DataFrame(records, columns=columns)
    save_csv(df, subdir, filename)


evt_data_definitions = {
    "evt.nodes_station_evt.csv": ["distid", "createdts", "sn", "event_type"],
    "evt.stations_mesh_evt.csv": [
        "distid",
        "createdts",
        "sn",
        "event_type",
        "event_action",
    ],
    "evt.nodes_events_evt.csv": ["distid", "createdts", "sn", "event_reason"],
}
# Generate Synthetic data - evt
for filename, columns in evt_data_definitions.items():
    subdir = "evt"
    records = []
    for device in device_ids:
        for timestamp in timestamps[:: np.random.randint(1, 6)]:
            record = {
                "distid": f"{device}_{timestamp}",
                "createdts": timestamp,
                "sn": device,
            }
            for col in columns[3:]:
                # Event type, Event action, Event reason
                record[col] = np.random.randint(1, 100)
            records.append(record)
    df = pd.DataFrame(records, columns=columns)
    save_csv(df, subdir, filename)


diag_data_definitions = {
    "diag.nodes_speedtest_diag.csv": ["distid", "createdts", "sn", "ookla_result"],
    "diag.nodes_group_wifi_scan_diag.csv": [
        "distid",
        "createdts",
        "sn",
        "wifi_ap_band_info_band_id",
        "wifi_ap_band_info_channel",
        "wifi_ap_band_info_wifi_name",
        "wifi_ap_band_info_bssid",
    ],
    "diag.nodes_acs_channelchange_diag.csv": [
        "distid",
        "createdts",
        "sn",
        "acs_bid",
        "acs_primary_ch",
        "acs_prev_ch",
        "acs_reason",
    ],
}
# Generate Synthetic data - diag
for filename, columns in diag_data_definitions.items():
    subdir = "diag"
    records = []
    for device in device_ids:
        for timestamp in timestamps[:: np.random.randint(1, 6)]:
            record = {
                "distid": f"{device}_{timestamp}",
                "createdts": timestamp,
                "sn": device,
            }
            for col in columns[3:]:
                if col == "wifi_ap_band_info_band_id":
                    record[col] = random_wifi_band()
                elif col == "wifi_ap_band_info_bssid":
                    record[col] = random_mac()
                elif col == "ookla_result":
                    record[col] = {
                        "SpeedTestType": "OoklaTCP",
                        "TransactionID": "",
                        "OoklaServerID": "37686",
                        "TestResponse": "Completed",
                        "TestProgress": 100,
                        "DownloadSpeed": np.random.randint(1, 100),
                        "UploadSpeed": np.random.randint(1, 100),
                        "Latency": np.random.randint(1, 100),
                        "PacketLossRate": np.random.randint(1, 100),
                        "Jitter": np.random.randint(1, 100),
                        "Download LatencyIQM": np.random.randint(1, 100),
                        "Download LatencyLow": np.random.randint(1, 100),
                        "Download LatencyHigh": np.random.randint(1, 100),
                        "Download LatencyJitter": np.random.randint(1, 100),
                        "UploadLatencyIQM": np.random.randint(1, 100),
                        "UploadLatencyLow": np.random.randint(1, 100),
                        "Upload LatencyHigh": np.random.randint(1, 100),
                        "UploadLatencyJitter": np.random.randint(1, 100),
                    }
                else:
                    record[col] = np.random.randint(1, 100)
            records.append(record)
    df = pd.DataFrame(records, columns=columns)
    save_csv(df, subdir, filename)

print("All synthetic data files generated successfully!")
