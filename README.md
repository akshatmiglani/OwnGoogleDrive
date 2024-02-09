Steps for host server.
1.sudo pvcreate /dev/sdb
2.sudo pvs /dev/sdb -verify
3.sudo vgcreate vg0 /dev/sdb
4.sudo lvcreate -n lv0 -L 1.5G vg0
5.sudo mkfs.ext4 /dev/vg0/lv0
6. sudo mkdir /mnt/lv0
7. sudo mount /dev/vg0/lv0 /mnt/lv0/
8.df -Th | grep -i /mnt/lv0
9. sudo nano /etc/fstab
10. /dev/vg0/lv0 /mnt/lv1	ext4	defaults 0 0

Next use apache/nginx for hosting a form.
