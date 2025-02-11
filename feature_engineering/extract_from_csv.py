# Data folder structure
# ├── data/
# │   ├── hbt/
# │   |   ├── hbt.nodes_wifi_hbt.csv
# │   |   ├── hbt.nodes_wan_hbt.csv
# │   |   ├── hbt.nodes_stations_hbt.csv
# │   |   ├── hbt.group_nodes_hbt.csv
# │   ├── diag/
# │   |   ├── diag.nodes_speedtest_diag.csv
# │   |   ├── diag.nodes_group_wifi_scan_diag.csv
# │   |   ├── diag.nodes_acs_channelchange_diag.csv
# │   ├── evt/
# │   |   ├── evt.nodes_station_evt.csv
# │   |   ├── evt.stations_mesh_evt.csv
# │   |   ├── evt.nodes_events_evt.csv

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

from pathlib import Path
from loguru import logger

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from constants import DATA_DIR


def load_data(data_path: Path):
    """
    Load data from a CSV file
    :param data_path: Path to the CSV file
    :return: DataFrame
    """
    return pd.read_csv(data_path)


def extract_data(device_id: str, startdate: str):
    # Features to extract
    # Data used - upload ✅
    #   hbt.nodes_stations_hbt.stations_bs
    # Data used - download ✅
    #   hbt.nodes_stations_hbt.stations_br
    # Speed - upload ✅
    #   diag.nodes_speedtest_diag.ookla_result.UploadSpeed
    # Speed - download ✅
    #   diag.nodes_speedtest_diag.ookla_result.DownloadSpeed
    # Legacy devices exist ✅
    #   if hbt.nodes_stations_hbt.stations_mode in [0,1,2,3] then "Yes" else "No"
    # Signal Strength ✅
    #   hbt.nodes_stations_hbt.stations_signal_strength
    # Stationary vs Mobile ✅ ❓
    #   Compute "90th Percentile" and "Median" of `Signal Strength`
    #   If the difference between the two is greater than 5, then "Mobile" else "Stationary"
    # Phy Rate {DownlinkPhyRate, MaxDownlinkPhyRate, UplinkPhyRate, MaxUplinkPhyRate} ✅
    #   hbt.nodes_stations_hbt.[stations_tx_link_rate, stations_max_tx_phy_rate, stations_link_rate, stations_max_rx_phy_rate]
    # Num Clients Connected ✅
    #   hbt.group_nodes_hbt.tplg_node_sta_num
    # Num Access Points ✅
    #   Number of Unique `hbt.group_nodes_hbt.tplg_node_device_mac`
    # Mean Clients Per AP ✅ ❓
    #  for each `AP = hbt.group_nodes_hbt.tplg_node_device_mac`, compute the number of unique `hbt.nodes_stations_hbt.stations_mac` with `hbt.nodes_stations_hbt.parent_id = AP` and take the mean across all APs
    # Channel Switches ✅
    #   Count `diag.nodes_acs_channelchange_diag.acs_bid` where acs_primary_ch != acs_prev_ch
    # Wifi Associations ✅
    #   "Disassociation" if `evt.nodes_station_evt.event_type` = 3. "Association" if `evt.nodes_station_evt.event_type` = 4
    # SON status (On/Off) ✅
    #   hbt.group_nodes_hbt.tplg_node_son
    # SON Steer Success Status (Success/Failure) ✅
    #   if `evt.stations_mesh_evt.event_type` = (2 or 3) and `evt.stations_mesh_evt.event_action` = 0 then "Failure", elif
    #   `evt.stations_mesh_evt.event_type` = (2 or 3) and `evt.stations_mesh_evt.event_action` = 1 then "Success"
    # Num Device Power Cycles ✅
    #   Number of `evt.nodes_events_evt.event_type` in [1,8,12,13]
    # Latency ✅
    #   diag.nodes_speedtest_diag.ookla_result.Latency


    try:
        startdate = datetime.strptime(startdate, "%Y-%m-%d")
    except ValueError:
        logger.error("Invalid start date format. Use 'YYYY-MM-DD' format")
        sys.exit(1)
    raw_data = {"timestamp": startdate, "device_id": device_id}

    # Data Used (UL, DL), Legacy Devices Exist, Signal Strength, Phy Rate
    filename = DATA_DIR / "hbt" / "hbt.nodes_stations_hbt.csv"
    data = load_data(filename)
    data = data[data["sn"] == device_id]
    data = data[data["createdts"] >= startdate]
    raw_data["hbt.nodes_stations_hbt"] = data.copy()

    # Speed (UL, DL), Latency
    filename = DATA_DIR / "diag" / "diag.nodes_speedtest_diag.csv"
    data = load_data(filename)
    data = data[data["sn"] == device_id]
    data = data[data["createdts"] >= startdate]
    raw_data["diag.nodes_speedtest_diag"] = data.copy()

    # Num Clients Connected, Num Access Points, Mean Clients Per AP, SON Status
    filename = DATA_DIR / "hbt" / "hbt.group_nodes_hbt.csv"
    data = load_data(filename)
    data = data[data["sn"] == device_id]
    data = data[data["createdts"] >= startdate]
    raw_data["hbt.group_nodes_hbt"] = data.copy()

    # Channel Switches
    filename = DATA_DIR / "diag" / "diag.nodes_acs_channelchange_diag.csv"
    data = load_data(filename)
    data = data[data["sn"] == device_id]
    data = data[data["createdts"] >= startdate]
    raw_data["diag.nodes_acs_channelchange_diag"] = data.copy()

    # Wifi Associations
    filename = DATA_DIR / "evt" / "evt.nodes_station_evt.csv"
    data = load_data(filename)
    data = data[data["sn"] == device_id]
    data = data[data["createdts"] >= startdate]
    raw_data["evt.nodes_station_evt"] = data.copy()

    # SON Steer Success Status
    filename = DATA_DIR / "evt" / "evt.stations_mesh_evt.csv"
    data = load_data(filename)
    data = data[data["sn"] == device_id]
    data = data[data["createdts"] >= startdate]
    raw_data["evt.stations_mesh_evt"] = data.copy()

    # Num Device Power Cycles
    filename = DATA_DIR / "evt" / "evt.nodes_events_evt.csv"
    data = load_data(filename)
    data = data[data["sn"] == device_id]
    data = data[data["createdts"] >= startdate]
    raw_data["evt.nodes_events_evt"] = data.copy()

    return raw_data


