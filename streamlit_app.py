import streamlit as st
import paramiko

st.set_page_config(layout="wide")
st.title("UPIMS MONITOR CONTROL")

tabs = st.tabs(["Update Dashboard"])

# Shared mapping
pi_map = {
    "Monitor 1": "upi-ms-pi12",
    "Monitor 2": "upi-ms-pi07",
    "Monitor 3": "upi-ms-pi02",
    "Monitor 4": "upi-ms-pi09",
    "Monitor 5": "upi-ms-pi16",
    "Monitor 6": "upi-ms-pi15",
    "Monitor 7": "upi-ms-pi06",
    "Monitor 8": "upi-ms-pi03",
    "Monitor 9": "upi-ms-pi01",
    "Monitor 10": "upi-ms-pi13",
    "Monitor 11": "upi-ms-pi11",
    "Monitor 12": "upi-ms-pi10",
    "Monitor 13": "upi-ms-pi05",
    "Monitor 14": "upi-ms-pi14"  
}

# --- Tab 1: Update Dashboard ---
with tabs[0]:
    selected_tv = st.selectbox("Select TV", list(pi_map.keys()), key="update_tv")
    actual_username = pi_map[selected_tv]

    url = st.text_input("Enter new dashboard URL")
    password = st.text_input("SSH Password", type="password")

    if st.button("Update Dashboard"):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=actual_username + ".local", username=actual_username, password=password)

            cmd = f"""
echo '#!/bin/bash
export DISPLAY=:0
chromium-browser --start-fullscreen --disable-gpu --noerrdialogs --disable-infobars --disable-extensions --disable-popup-blocking --disable-features=TranslateUI --no-first-run --no-default-browser-check  "{url}"' | sudo tee /home/{actual_username}/start-dashboard.sh > /dev/null && \
sudo chmod +x /home/{actual_username}/start-dashboard.sh && \
sudo systemctl restart dashboard.service
"""
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            ssh.close()

            if exit_status == 0:
                st.success(f"{selected_tv} updated successfully.")
            else:
                st.error(f"Command failed:\n{stderr.read().decode()}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

