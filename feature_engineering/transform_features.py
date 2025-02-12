## Assumption: the timestamps in hbt, evt, and diag data are synced.
## TODO: Sync the data points based on the timestamps

## Features to generate
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
#   Count `diag.nodes_acs_channelchange_diag.acs_bid` where acs_primary_ch != acs_prev_ch# Wifi Associations ✅
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

import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from constants import DATA_DIR

# Define base directory for data
base_dir = DATA_DIR / "synthetic_data"
output_dir = DATA_DIR / "processed_data"
os.makedirs(output_dir, exist_ok=True)

# List of files to extract
data_files = {
    "hbt": ["hbt.nodes_wifi_hbt.csv", "hbt.nodes_wan_hbt.csv", "hbt.nodes_stations_hbt.csv", "hbt.group_nodes_hbt.csv"],
    "diag": ["diag.nodes_speedtest_diag.csv", "diag.nodes_group_wifi_scan_diag.csv", "diag.nodes_acs_channelchange_diag.csv"],
    "evt": ["evt.nodes_station_evt.csv", "evt.stations_mesh_evt.csv", "evt.nodes_events_evt.csv"]
}

def extract_from_csv():
    """Load all raw CSV files into DataFrames."""
    data = {}
    for folder, files in data_files.items():
        for file in files:
            file_path = os.path.join(base_dir, folder, file)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                data[file] = df
            else:
                print(f"Warning: {file_path} not found.")
    return data

def transform_features(data):
    """Transform raw data into meaningful features."""
    merged_features = pd.DataFrame()
    
    # Extract required features
    if "hbt.nodes_stations_hbt.csv" in data:
        df = data["hbt.nodes_stations_hbt.csv"]
        df["legacy_devices"] = df["stations_mode"].apply(lambda x: "Yes" if x in [0,1,2,3] else "No")
        df["stationary_mobile"] = df.groupby("sn")["stations_signal_strength"].transform(lambda x: "Mobile" if x.quantile(0.9) - x.median() > 5 else "Stationary")
        df = df.loc[:, [
            "sn", "createdts", "stations_bs", "stations_br", "stations_signal_strength", 
            "legacy_devices", "stationary_mobile", "stations_tx_link_rate", 
            "stations_max_tx_phy_rate", "stations_link_rate", "stations_max_rx_phy_rate"
        ]]
        df.rename(columns={
            "stations_bs": "upload_data",
            "stations_br": "download_data",
            "stations_signal_strength": "signal_strength",
            "stations_tx_link_rate": "downlink_phy_rate",
            "stations_max_tx_phy_rate": "max_downlink_phy_rate",
            "stations_link_rate": "uplink_phy_rate",
            "stations_max_rx_phy_rate": "max_uplink_phy_rate"
        }, inplace=True)
        merged_features = df if merged_features.empty else merged_features.merge(df, on=["sn", "createdts"], how="inner")
    
    if "hbt.group_nodes_hbt.csv" in data:
        df = data["hbt.group_nodes_hbt.csv"]
        df = df.loc[:, ["sn", "createdts", "tplg_node_sta_num", "tplg_node_son"]]
        df.rename(columns={"tplg_node_sta_num": "num_clients_connected", "tplg_node_son": "son_status"}, inplace=True)
        merged_features = df if merged_features.empty else merged_features.merge(df, on=["sn", "createdts"], how="inner")
    
    if "diag.nodes_speedtest_diag.csv" in data:
        df = data["diag.nodes_speedtest_diag.csv"]
        df["upload_speed"] = df["ookla_result"].apply(lambda x: eval(x)["UploadSpeed"])
        df["download_speed"] = df["ookla_result"].apply(lambda x: eval(x)["DownloadSpeed"])
        df["latency"] = df["ookla_result"].apply(lambda x: eval(x)["Latency"])
        df = df.loc[:, ["sn", "createdts", "upload_speed", "download_speed", "latency"]]
        merged_features = df if merged_features.empty else merged_features.merge(df, on=["sn", "createdts"], how="inner")
    
    if "diag.nodes_acs_channelchange_diag.csv" in data:
        df = data["diag.nodes_acs_channelchange_diag.csv"]
        df = df[df["acs_primary_ch"] != df["acs_prev_ch"]].groupby(["sn", "createdts"]).size().reset_index(name="channel_switches")
        merged_features = df if merged_features.empty else merged_features.merge(df, on=["sn", "createdts"], how="inner")
    
    if "evt.nodes_station_evt.csv" in data:
        df = data["evt.nodes_station_evt.csv"]
        if "event_type" in df.columns:
            df["wifi_association"] = df["event_type"].apply(lambda x: "Disassociation" if x == 3 else "Association" if x == 4 else "None")
            df = df.loc[:, ["sn", "createdts", "wifi_association"]]
            merged_features = df if merged_features.empty else merged_features.merge(df, on=["sn", "createdts"], how="inner")
        else:
            print("Warning: 'event_type' column not found in evt.nodes_station_evt.csv")
    
    if "evt.nodes_events_evt.csv" in data:
        df = data["evt.nodes_events_evt.csv"]
        if "event_type" in df.columns:
            df["num_device_power_cycles"] = df["event_type"].apply(lambda x: 1 if x in [1,8,12,13] else 0)
            df = df.groupby(["sn", "createdts"]).agg({"num_device_power_cycles": "sum"}).reset_index()
            merged_features = df if merged_features.empty else merged_features.merge(df, on=["sn", "createdts"], how="inner")
        else:
            print("Warning: 'event_type' column not found in evt.nodes_events_evt.csv")
    
    if "evt.stations_mesh_evt.csv" in data:
        df = data["evt.stations_mesh_evt.csv"]
        if "event_type" in df.columns and "event_action" in df.columns:
            df["son_steer_success_status"] = df.apply(lambda x: "Failure" if x["event_type"] in [2, 3] and x["event_action"] == 0 else "Success" if x["event_type"] in [2, 3] and x["event_action"] == 1 else "None", axis=1)
            df = df.loc[:, ["sn", "createdts", "son_steer_success_status"]]
            merged_features = df if merged_features.empty else merged_features.merge(df, on=["sn", "createdts"], how="inner")
        else:
            print("Warning: 'event_type' or 'event_action' column not found in evt.stations_mesh_evt.csv")
    
    merged_features.to_csv(os.path.join(output_dir, "transformed_features.csv"), index=False)
    print("Feature transformation complete.")

if __name__ == "__main__":
    raw_data = extract_from_csv()
    transform_features(raw_data)