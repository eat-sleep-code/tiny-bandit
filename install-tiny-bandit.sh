# This script will install the Tiny Bandit software, display drivers, and any required prerequisites.
cd ~
echo -e ''
echo -e '\033[32mTiny Bandit [Installation Script] \033[0m'
echo -e '\033[32m-------------------------------------------------------------------------- \033[0m'
echo -e ''
echo -e '\033[93mUpdating package repositories... \033[0m'
sudo apt update

echo ''
echo -e '\033[93mInstalling prerequisites... \033[0m'
sudo apt install -y git python3 python3-pip 
sudo pip3 install pygame jmespath Rpi.GPIO

echo ''
echo -e '\033[93mInstalling Game Software... \033[0m'
cd ~
sudo rm -Rf ~/tiny-bandit
sudo git clone -b main --single-branch https://github.com/eat-sleep-code/tiny-bandit
sudo chown -R $USER:$USER tiny-bandit
cd tiny-bandit
sudo chmod +x tiny-bandit.py

echo ''
echo -e '\033[93mInstalling Display Drivers... \033[0m'
cd ~
sudo git clone https://github.com/tianyoujian/MZDPI.git
sudo chown -R $USER:$USER MZDPI
cd MZDPI/mzp354wv1b
sudo chmod +x mzdpi-wvga-autoinstall
sudo ./mzdpi-wvga-autoinstall

cd ~
echo ''
echo -e '\033[93mSetting up alias... \033[0m'
sudo touch ~/.bash_aliases
sudo chown -R $USER:$USER ~/.bash_aliases
echo "" | sudo tee -a ~/.bash_aliases
sudo sed -i '/\b\(function tiny-bandit\)\b/d' ~/.bash_aliases
sudo sed -i '$ a function tiny-bandit { sudo python3 ~/tiny-bandit/tiny-bandit.py "$@"; }' ~/.bash_aliases
echo -e 'You may use \e[1mtiny-bandit <options>\e[0m to launch the program.'

echo ''
echo -e '\033[32m-------------------------------------------------------------------------- \033[0m'
echo -e '\033[32mInstallation completed. \033[0m'
echo ''
sudo rm ~/install-tiny-bandit.sh

echo ''
echo -e '\033[33mA system reboot is required to complete the display driver installation. \033[0m'
