## Assumption: the timestamps in hbt, evt, and diag data are synced.
## TODO: Sync the data points based on the timestamps

import numpy as np
import pandas as pd
from extract_from_csv import extract_data

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


def generate_features(data: pd.DataFrame):
    features = pd.DataFrame()

    # Data used - upload
    features["upload_data"] = data["hbt.nodes_stations_hbt"]["stations_bs"]

    # Data used - download
    features["download_data"] = data["hbt.nodes_stations_hbt"]["stations_br"]

    # Speed - upload
    features["upload_speed"] = data["diag.nodes_speedtest_diag"]["ookla_result"][
        "UploadSpeed"
    ]

    # Speed - download
    features["download_speed"] = data["diag.nodes_speedtest_diag"]["ookla_result"][
        "DownloadSpeed"
    ]

    # Legacy devices exist
    features["legacy_devices_exist"] = np.where(
        data["hbt.nodes_stations_hbt"]["stations_mode"].isin([0, 1, 2, 3]), "Yes", "No"
    )

    # Signal Strength
    features["signal_strength"] = data["hbt.nodes_stations_hbt"][
        "stations_signal_strength"
    ]

    # Stationary vs Mobile
    signal_strength_90th = data["hbt.nodes_stations_hbt"][
        "stations_signal_strength"
    ].quantile(0.9)
    signal_strength_median = data["hbt.nodes_stations_hbt"][
        "stations_signal_strength"
    ].median()
    features["stationary_vs_mobile"] = np.where(
        (signal_strength_90th - signal_strength_median) > 5, "Mobile", "Stationary"
    )

    # Phy Rate
    features["downlink_phy_rate"] = data["hbt.nodes_stations_hbt"][
        "stations_tx_link_rate"
    ]
    features["max_downlink_phy_rate"] = data["hbt.nodes_stations_hbt"][
        "stations_max_tx_phy_rate"
    ]
    features["uplink_phy_rate"] = data["hbt.nodes_stations_hbt"]["stations_link_rate"]
    features["max_uplink_phy_rate"] = data["hbt.nodes_stations_hbt"][
        "stations_max_rx_phy_rate"
    ]

    # Num Clients Connected
    features["num_clients_connected"] = data["hbt.group_nodes_hbt"]["tplg_node_sta_num"]

    # Num Access Points
    features["num_access_points"] = data["hbt.group_nodes_hbt"][
        "tplg_node_device_mac"
    ].nunique()

    # Mean Clients Per AP
    ap_clients = (
        data["hbt.group_nodes_hbt"]
        .groupby("tplg_node_device_mac")["stations_mac"]
        .nunique()
    )
    features["mean_clients_per_ap"] = ap_clients.mean()

    # Channel Switches
    features["channel_switches"] = (
        data["diag.nodes_acs_channelchange_diag"]["acs_bid"]
        .where(
            data["diag.nodes_acs_channelchange_diag"]["acs_primary_ch"]
            != data["diag.nodes_acs_channelchange_diag"]["acs_prev_ch"]
        )
        .count()
    )

    # Wifi Associations
    features["wifi_associations"] = np.where(
        data["evt.nodes_station_evt"]["event_type"] == 3,
        "Disassociation",
        np.where(
            data["evt.nodes_station_evt"]["event_type"] == 4, "Association", np.nan
        ),
    )

    # SON status (On/Off)
    features["son_status"] = data["hbt.group_nodes_hbt"]["tplg_node_son"]

    # SON Steer Success Status (Success/Failure)
    features["son_steer_success_status"] = np.where(
        (data["evt.stations_mesh_evt"]["event_type"].isin([2, 3]))
        & (data["evt.stations_mesh_evt"]["event_action"] == 0),
        "Failure",
        np.where(
            (data["evt.stations_mesh_evt"]["event_type"].isin([2, 3]))
            & (data["evt.stations_mesh_evt"]["event_action"] == 1),
            "Success",
            np.nan,
        ),
    )

    # Num Device Power Cycles
    features["num_device_power_cycles"] = (
        data["evt.nodes_events_evt"]["event_type"].isin([1, 8, 12, 13]).sum()
    )

    # Latency
    features["latency"] = data["diag.nodes_speedtest_diag"]["ookla_result"]["Latency"]

    # Timestamp and device_id
    features["timestamp"] = data["hbt.nodes_stations_hbt"]["createdts"]
    features["device_id"] = data["hbt.nodes_stations_hbt"]["sn"]

    return features
