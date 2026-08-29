import paramiko
import os
import sys

host = '100.100.52.93'
port = 22
username = 'nctlite'
password = '121212'
remote_dir = '/home/nctlite/filesaverbot'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {username}@{host}...")
    ssh.connect(host, port, username, password)
    
    sftp = ssh.open_sftp()
    
    print("Uploading filesaver_bot.py...")
    sftp.put('filesaver_bot.py', f'{remote_dir}/filesaver_bot.py')
    
    print("Uploading templates/index.html...")
    try:
        sftp.mkdir(f'{remote_dir}/templates')
    except IOError:
        pass # Directory likely exists
        
    sftp.put('templates/index.html', f'{remote_dir}/templates/index.html')
    
    print("Uploading templates/admin_dashboard.html...")
    sftp.put('templates/admin_dashboard.html', f'{remote_dir}/templates/admin_dashboard.html')
    
    sftp.close()

    print("\n--- Restarting filesaverbot.service ---")
    
    # Install GA4 library
    print("Installing google-analytics-data...")
    stdin, stdout, stderr = ssh.exec_command(f"echo '{password}' | sudo -S -u nctlite pip3 install --break-system-packages google-analytics-data")
    stdout.read()
    
    stdin, stdout, stderr = ssh.exec_command(f"echo '{password}' | sudo -S systemctl restart filesaverbot.service")
    err = stderr.read().decode()
    exit_status = stdout.channel.recv_exit_status()
    print("Service restarted.")
    
    stdin, stdout, stderr = ssh.exec_command("systemctl status filesaverbot.service | head -n 10")
    print(stdout.read().decode(errors='ignore'))
    
    print("Deployment to Pi successful!")
except Exception as e:
    print(f"Deployment failed: {e}")
finally:
    ssh.close()
