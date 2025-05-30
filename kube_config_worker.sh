# Désactiver la swap immédiatement (Kubernetes ne fonctionne pas avec)
sudo swapoff -a

# Désactiver la swap au démarrage en commentant la ligne correspondante dans /etc/fstab
sudo sed -i '/ swap / s/^/#/' /etc/fstab

# Mettre à jour la liste des paquets et installer containerd (runtime de conteneurs)
sudo apt-get update
sudo apt-get install -y containerd

# Configurer containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Activer la gestion des cgroups par systemd (recommandé pour Kubernetes)
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Activer le support de l'interface CRI (nécessaire pour Kubernetes)
sudo sed -i 's/disabled_plugins = \["cri"\]/#disabled_plugins = \["cri"\]/' /etc/containerd/config.toml

# Redémarrer et activer containerd au démarrage
sudo systemctl restart containerd
sudo systemctl enable containerd

# Vérifier que containerd est bien actif
sudo systemctl status containerd  # Doit être "active (running)"

# Charger les modules noyau nécessaires à Kubernetes
sudo modprobe br_netfilter
sudo modprobe overlay

# Appliquer les paramètres réseau requis pour Kubernetes
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

# Appliquer les changements de configuration du réseau
sudo sysctl --system

# join le worker grace au token a partir d'ici