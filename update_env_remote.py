import paramiko

# Update VPS
try:
    print("Updating VPS...")
    ssh_vps = paramiko.SSHClient()
    ssh_vps.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_vps.connect('178.128.59.217', username='root', key_filename=r'E:\00_Python\GPS\id_ed25519')
    ssh_vps.exec_command("sed -i '/GA4_PROPERTY_ID/d' /root/filesaverbot/.env")
    ssh_vps.exec_command("echo \"GA4_PROPERTY_ID = '396031246'\" >> /root/filesaverbot/.env")
    ssh_vps.exec_command("systemctl restart filesaverbot")
    print("VPS updated and restarted.")
except Exception as e:
    print(f"VPS error: {e}")

# Update Pi
try:
    print("Updating Pi...")
    ssh_pi = paramiko.SSHClient()
    ssh_pi.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_pi.connect('100.100.52.93', username='nctlite', password='121212')
    ssh_pi.exec_command("sed -i '/GA4_PROPERTY_ID/d' /home/nctlite/filesaverbot/.env")
    ssh_pi.exec_command("echo \"GA4_PROPERTY_ID = '396031246'\" >> /home/nctlite/filesaverbot/.env")
    ssh_pi.exec_command("echo '121212' | sudo -S systemctl restart filesaverbot.service")
    print("Pi updated and restarted.")
except Exception as e:
    print(f"Pi error: {e}")
