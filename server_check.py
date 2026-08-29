import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

def restart_service():
    host = '192.168.1.167'
    port = 22
    username = 'nctlite'
    password = '121212'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {username}@{host}...")
        ssh.connect(host, port, username, password)
        
        print("\n--- Restarting filesaverbot.service ---")
        stdin, stdout, stderr = ssh.exec_command(f"echo '{password}' | sudo -S systemctl restart filesaverbot.service")
        stdout.channel.recv_exit_status()
        print("Done.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == '__main__':
    restart_service()
