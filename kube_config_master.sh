# Désactiver la swap immédiatement (Kubernetes ne fonctionne pas avec)
sudo swapoff -a

# Désactiver la swap au démarrage en commentant la ligne correspondante dans /etc/fstab
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

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

# Initialiser le cluster Kubernetes avec Calico (réseau des pods en 192.168.0.0/16)
output=$(sudo kubeadm init --pod-network-cidr=192.168.0.0/16)

# Extraire la ligne contenant "kubeadm join" et les deux lignes suivantes
join_command=$(echo "$output" | grep -A 2 "kubeadm join")

# Sauvegarder la commande kubeadm join dans token.txt
echo "$join_command" > token.txt

# Configurer kubectl pour l'utilisateur actuel
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Modifier les permissions du fichier de configuration Kubernetes
sudo chmod 644 /etc/kubernetes/admin.conf

# Rendre la configuration persistante pour l'utilisateur
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> $HOME/.bashrc
source $HOME/.bashrc

# Télécharger le fichier Calico sur la machine avant de l'appliquer
wget https://docs.projectcalico.org/manifests/calico.yaml -O calico.yaml
kubectl apply -f calico.yaml


# Attendre quelques secondes pour laisser les pods se créer
echo "Attente de 10 secondes pour l'initialisation..."
sleep 10

# Vérifier les pods en cours
while true; do
    echo "Vérification de l'état des pods..."
    kubectl get pods -n kube-system

    # Demander à l'utilisateur s'il veut redémarrer calico-node
    read -p "Voulez-vous redémarrer les pods calico-node ? (y/n) : " choix
    choix=$(echo "$choix" | tr -d '[:space:]')  # Suppression des espaces au début et à la fin

    if [ "$choix" = "y" ]; then  # Utilisation de [ ... ] au lieu de [[ ... ]]
        echo "Redémarrage des pods calico-node..."
        kubectl delete pod -n kube-system -l k8s-app=calico-node
        echo "Attente de 10 secondes après redémarrage..."
        sleep 10
    elif [ "$choix" = "n" ]; then  # Utilisation de [ ... ] au lieu de [[ ... ]]
        echo "Sortie du script."
        break
    else
        echo "Réponse invalide, veuillez répondre par 'y' ou 'n'."
    fi
done
