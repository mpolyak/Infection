$script = <<SCRIPT

sudo apt-get update
sudo apt-get -y install python3-pip

echo "alias python=python3" >> ~/.bash_aliases
echo "alias pip=pip3" >> ~/.bash_aliases

echo "cd /vagrant" >> ~/.bashrc

cd /vagrant

SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |v|
    v.name = "Infection"
    v.memory = 512
    v.cpus = 1
  end

  config.vm.box_check_update = false

  config.vm.provision "shell", inline: $script, privileged: false
end