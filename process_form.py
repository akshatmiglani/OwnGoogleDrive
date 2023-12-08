#!/usr/bin/python3
import cgi
import os
import subprocess

print("Content-type: text/html\n")

form = cgi.FieldStorage()
ip = form.getvalue("hostname")
username = form.getvalue("username")
password = form.getvalue("password")
storage=form.getvalue("storage")
admin_pass=""

if ip is None or username is None or password is None:
    print("Error: Incomplete form data provided.")
else:
    try:
        script_content =f"""
        #!/bin/bash
	    echo {admin_pass} | sudo -S lvcreate -L {storage} -yn aklv1 vg0
        echo {admin_pass}|sudo -S  mkfs.ext4 /dev/vg0/aklv1
	    echo {admin_pass}| sudo -S mkdir -p /mnt/akshat_drive1
	    echo {admin_pass} | sudo -S mount /dev/vg0/aklv1 /mnt/akshat_drive1
        echo "/dev/vg0/aklv1 /mnt/akshat_drive1 ext4 defaults 0 0 "| sudo tee -a /etc/fstab    
        echo {admin_pass} | sudo -S chown -R nobody:nogroup /mnt/akshat_drive1
        echo {admin_pass} | sudo -S chmod 777 /mnt/akshat_drive1
        echo "/mnt/akshat_drive1 192.168.29.2/2(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports
        echo {admin_pass} |sudo -S  exportfs -a
        echo {admin_pass} | sudo -S systemctl restart nfs-kernel-server
        """
        ssh_command=["bash","-s"]
        # Execute the SSH command and pass the script content via stdin
        execute = subprocess.run(ssh_command, input=script_content, capture_output=True, text=True, check=True)

        script_content=f"""
        #!/bin/bash
	    echo "{password}" | sudo -S mkdir -p  /home/{username}/newdrive1
	    echo "{password}" | sudo -S mount -t nfs 192.168.29.2:/mnt/akshat_drive1 /home/{username}/newdrive1
        """
        
        ssh_command=["sshpass","-p",password,"ssh","-o","StrictHostKeyChecking=no",f"{username}@{ip}","bash -s"]
        execute = subprocess.run(ssh_command, input=script_content, capture_output=True, text=True, check=True)

        print("Drive created successfully.Thank you for using AKSHATDRIVE, You can use the drive from your home directory!")
        print(execute.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the script: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")





