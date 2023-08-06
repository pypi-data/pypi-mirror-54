"""Base data to initiate an AtagDataStore."""

TESTDATA = {
    "_host": '192.168.1.3',  # atag IP
    "_port": 10000,
    "_mail": "matsnelissen@gmail.com",  # email registered in portal
    "_scan_interval": 30,
    # "{B52F235E-6695-4064-A48C-658F276C7FFE}", # interface of connecting device
    "_interface": None,
    "_sensors": [  # sensors to test, see const.py
        "temperature",
        "current_temperature"
    ]
}
SQLSERVER = {
    'host': '192.168.1.242',
    'port': 3306,
    'user': 'hass',
    'password': 'hassiomats',
    'db': 'hass-dev'
}

TESTDATA = {"_host": '192.168.1.3', "_port": 10000, "_mail": "matsnelissen@gmail.com",
            "_scan_interval": 30, "_interface": None, "_sensors":
            ["temperature", "current_temperature"]}

JSON_REPLY = {
    "retrieve_reply": {
        "seqnr": 1,
        "status": {
            "device_id": "6808-1401-3107_15-05-003-171",
            "device_status": 16385,
            "connection_status": 23,
            "date_time": 611770815
        },
        "report": {
            "report_time": 611770815,
            "burning_hours": 3216.87,
            "device_errors": "",
            "boiler_errors": "",
            "room_temp": 18.7,
            "outside_temp": 12.7,
            "dbg_outside_temp": 21.3,
            "pcb_temp": 25.2,
            "ch_setpoint": 0.0,
            "dhw_water_temp": 22.3,
            "ch_water_temp": 18.8,
            "dhw_water_pres": 0.0,
            "ch_water_pres": 1.3,
            "ch_return_temp": 18.8,
            "boiler_status": 0,
            "boiler_config": 772,
            "ch_time_to_temp": 0,
            "shown_set_temp": 12.0,
            "power_cons": 0,
            "tout_avg": 12.6,
            "rssi": 20,
            "current": -10,
            "voltage": 3919,
            "charge_status": 1,
            "lmuc_burner_starts": 0,
            "dhw_flow_rate": 0.0,
            "resets": 4,
            "memory_allocation": 7178,
            "details": {
                "boiler_temp": 44.2,
                "boiler_return_temp": 42.0,
                "min_mod_level": 23,
                "rel_mod_level": 0,
                "boiler_capacity": 0,
                "target_temp": 12.0,
                "overshoot": 10.345,
                "max_boiler_temp": 60.0,
                "alpha_used": 0.00017,
                "regulation_state": 1,
                "ch_m_dot_c": 898.188,
                "c_house": 82641120,
                "r_rad": 0.0009,
                "r_env": 0.0146,
                "alpha": 0.00016,
                "alpha_max": 0.00017,
                "delay": 1,
                "mu": 0.0,
                "threshold_offs": 15.0,
                "wd_k_factor": 1.8,
                "wd_exponent": 1.3,
                "lmuc_burner_hours": 0,
                "lmuc_dhw_hours": 0,
                "KP": 9.0,
                "KI": 0.00142
            }
        },
        "control": {
            "ch_status": 41,
            "ch_control_mode": 0,
            "ch_mode": 1,
            "ch_mode_duration": 0,
            "ch_mode_temp": 12.0,
            "dhw_temp_setp": 60.0,
            "dhw_status": 13,
            "dhw_mode": 1,
            "dhw_mode_temp": 150.0,
            "weather_temp": 12.7,
            "weather_status": 7,
            "vacation_duration": 0,
            "extend_duration": 0,
            "fireplace_duration": 3600
        },
        "acc_status": 2
    }
}
