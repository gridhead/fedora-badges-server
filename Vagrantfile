Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.vm.define "badgesserver" do |badgesserver|
    badgesserver.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/38/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-38-1.6.x86_64.vagrant-libvirt.box"
    badgesserver.vm.box = "f38-cloud-libvirt"
    badgesserver.vm.hostname = "server.badges.test"

    badgesserver.vm.synced_folder '.', '/vagrant', type: "sshfs"

    badgesserver.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048
    end

    badgesserver.vm.provision "ansible" do |ansible|
      ansible.playbook = "devel/ansible/badgesserver.yml"
      ansible.config_file = "devel/ansible/ansible.cfg"
      ansible.verbose = true
    end
  end

end
