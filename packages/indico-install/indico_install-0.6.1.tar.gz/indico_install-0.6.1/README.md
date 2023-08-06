# Indico Platform Management

This repository contains tools to create and manage Indico K8S clusters. It is used by the Indico Engineering Team and is also used for client installations.

- [Introduction and Setup](https://github.com/IndicoDataSolutions/indico-deployment/wiki/Introduction-and-Setup)
- [Wiki](https://github.com/IndicoDataSolutions/indico-deployment/wiki)
- [Contributing](#contributing)


## Contributing
When making any changes to the CLI or tools, please appropriately document them in the wiki and include the updated pages as part of your PR.

## AKS Create CLI
```bash
az aks create \
    --name indico-cluster \
    --resource-group indico-platform \
    --vnet-subnet-id /subscriptions/3b9132d4-3ce3-40d8-a4fb-a185ac249199/resourceGroups/indico-platform/providers/Microsoft.Network/virtualNetworks/indico-network/subnets/default \
    --node-count 1 \
    --generate-ssh-keys \
    --node-osdisk-size 100 \
    --vm-set-type VirtualMachineScaleSets \
    --node-vm-size Standard_NC6 \
    --max-pods 110

az aks get-credentials -n indico-cluster -g indico-platform
cp ~/.kube/config indico_install/.kube/config
mkdir aks_deploy
cd aks_deploy
indico infra aks init
cp ../gcr_keys/wastemanagement.json indico.json
indico infra aks create
# storageaccount: indicostorage
# storageaccountkey: GET IT FROM HERE: https://portal.azure.com/#@madisonindico.onmicrosoft.com/resource/subscriptions/3b9132d4-3ce3-40d8-a4fb-a185ac249199/resourceGroups/indico-platform/providers/Microsoft.Storage/storageAccounts/indicostorage/keys
# File share names: https://portal.azure.com/#@madisonindico.onmicrosoft.com/resource/subscriptions/3b9132d4-3ce3-40d8-a4fb-a185ac249199/resourceGroups/indico-platform/providers/Microsoft.Storage/storageAccounts/indicostorage/fileList
```

## AKS Stand alone postgres

### Create Postgres VM in the Azure Portal
- Same Resource Group as AKS
- Same Location as AKS
- Image: Ubuntu 18.04 LTS
- Size: Standard F4s_v2
- SSH Key access
- Attach additional disk of at least 800GB
- Same VNET
- Same Subnet
- Enable Accelerated Networking
- Add Network rule for AKS cluster access on 5432 to the Postgres VM instance
- Add Network rule for Your SSH Access on 22 to the Postgres VM instance

### Setting up the VM
SSH into the VM

#### Mount additional data directory
Please mount the extra data disk to /var/lib/postgresql
```bash
# Find your device name
$ lsblk
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda       8:0    0   30G  0 disk
├─sda1    8:1    0 29.9G  0 part /
├─sda14   8:14   0    4M  0 part
└─sda15   8:15   0  106M  0 part /boot/efi
sdb       8:16   0   32G  0 disk
└─sdb1    8:17   0   32G  0 part /mnt
sdc       8:32   0 1023G  0 disk  **** # This is the one we want
sr0      11:0    1  628K  0 rom

$ sudo mkfs.ext4 /dev/sdc
$ sudo mkdir /var/lib/postgresql # create mount point directory
$ sudo mount /dev/sdc /var/lib/postgresql
```

#### Install Postgres
```bash
sudo apt-get update
sudo apt install -y postgresql postgresql-contrib
```

#### Edit Connection Configurations
Edit: `/etc/postgresql/10/main/pg_hba.conf to include the following line`

```bash
host    all             all             0.0.0.0/0               md5
```

Edit: `/etc/postgresql/10/main/postgresql.conf` for the following lines

```bash
listen_addresses = '*'          # what IP address(es) to listen on;
max_connections = 1024                  # (change requires restart)
shared_buffers = 1024MB                 # min 128kB
```

Restart the Postgresql Service
```
sudo service postgresql restart
```

#### Setup the Database

```bash
sudo -i -u postgres
createuser -ds <YOUR CONFIGURED POSTGRES USER>
psql -c "alter USER <YOUR CONFIGURED POSTGRES USER> WITH PASSWORD '<YOUR CONFIGURED PASSWORD>';"
export PGPASSWORD=<YOUR CONFIGURED PASSWORD>
psql -U <YOUR CONFIGURED POSTGRES USER> -h 127.0.0.1 -c "create database cyclone;" postgres
psql -U <YOUR CONFIGURED POSTGRES USER> -h 127.0.0.1 -c "create database noct;" postgres
psql -U <YOUR CONFIGURED POSTGRES USER> -h 127.0.0.1 -c "create database crowdlabel;" postgres
psql -U <YOUR CONFIGURED POSTGRES USER> -h 127.0.0.1 -c "create database elmosfire;" postgres
psql -U <YOUR CONFIGURED POSTGRES USER> -h 127.0.0.1 -c "create database moonbow;" postgres
```
