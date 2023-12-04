
---

# Suivi de Drones en Temps Réel

**Un système révolutionnaire pour le suivi dynamique des drones, combinant la puissance de la bibliothèque YOLO et NVIDIA TensorRT, spécialement conçu pour NVIDIA Jetson Nano.** Ce projet offre une solution de pointe pour la détection et le suivi en temps réel des drones, tirant parti des dernières avancées technologiques pour une précision et une performance accrues.

## Table des Matières
- [Introduction](#introduction)
- [Fonctionnalités Clés](#fonctionnalités-clés)
- [Guide d'Installation](#guide-dinstallation)
- [Configuration et Dépendances](#configuration-et-dépendances)
- [Guide d'Utilisation](#guide-dutilisation)
- [Personnalisation et Entraînement de Modèle](#personnalisation-et-entraînement-de-modèle)
- [Conversion de Modèles](#conversion-de-modèles)
- [Tests et Validation](#tests-et-validation)
- [Procédures de Déploiement](#procédures-de-déploiement)
- [Comment Contribuer](#comment-contribuer)
- [Licence](#licence)
- [Support](#support)

## Introduction
Ce projet vise à fournir une solution robuste pour le suivi de drones en temps réel. Il est idéal pour la surveillance, la gestion du trafic aérien, ou toute application nécessitant une surveillance aérienne précise et fiable. Notre système utilise les dernières innovations en matière d'intelligence artificielle et de traitement d'image pour offrir une expérience utilisateur sans précédent.

## Fonctionnalités Clés
- **Détection et Suivi en Temps Réel**: Utilise YOLO pour une détection et un suivi précis des drones.
- **Suivi Avancé**: Capable de suivre des drones malgré des mouvements rapides ou des changements de trajectoire.
- **Intégration de Capteurs NVIDIA**: Exploite les capteurs NVIDIA pour une précision améliorée.
- **Visualisation des Données de Suivi**: Affichage en temps réel des informations pour une surveillance efficace.
- **Compatibilité avec Diverses Caméras**: Supporte de nombreuses caméras compatibles avec Jetson Nano.
- **Flexibilité du Modèle YOLO**: Choisissez le modèle YOLO le plus adapté à vos besoins.

## Guide d'Installation
### Prérequis Système et Logiciel
Installez les dépendances nécessaires en exécutant les commandes suivantes :
```shell
sudo apt-get update
sudo apt-get install -y liblapack-dev libblas-dev gfortran libfreetype6-dev libopenblas-base libopenmpi-dev libjpeg-dev zlib1g-dev
sudo apt-get install -y python3-pip
pip install -r requirements.txt
```

### Problèmes Courants et Solutions
- **Dépendance Manquante**: Si une dépendance est manquante, essayez de l'installer manuellement.
- **Échec de l'Installation**: Assurez-vous que votre Jetson Nano est à jour avec la dernière version de JetPack.

## Configuration et Dépendances
- **Jetson Nano**: Developer Kit Version - Jetpack 4.6 [L4T 32.6.1]
- **Logiciels et Bibliothèques**: Cuda 10.2.300, OpenCV 4.1.1, TensorRT 8.0.1.6, cuDNN 8.2.1.32, PyTorch v1.10, torchvision v0.11.1, Python 3.6+, YOLOv5-7
- **Installation Additionnelle** :
   - **PyCuda** :
     ```shell
     export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}
     export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH
     pip install pycuda --user
     ```
   - **Seaborn** :
     ```shell
     sudo apt install python3-seaborn
     ```

### Installation de PyTorch et TensorRT
Suivez les instructions sur [ce lien](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048) pour installer PyTorch et torchvision sur Jetson Nano (choisir la

 version PyTorch v1.10 - torchvision v0.11.1).

## Guide d'Utilisation
Pour démarrer le suivi des drones, exécutez :
```shell
python3 track_drones.py
```
### FAQ sur l'Utilisation
- **Comment démarrer le suivi?** Lancez `track_drones.py` pour commencer le suivi.
- **Puis-je utiliser une caméra différente?** Oui, le système est compatible avec plusieurs modèles de caméras.

## Personnalisation et Entraînement de Modèle
Pour entraîner votre propre modèle YOLO, suivez ces étapes :
1. Collectez et préparez vos données.
2. Suivez les instructions de configuration du modèle YOLO.
3. Lancez le processus d'entraînement en utilisant `train.py`.

## Conversion de Modèles
Pour convertir un modèle `.pt` en format `.engine`, exécutez les commandes suivantes :
```shell
cd JetsonYoloV5
python3 gen_wts.py -w yolov5s.pt -o yolov5s.wts
```
Plus de détails dans la section [Conversion de Modèles](#conversion-de-modèles).

## Tests et Validation
Pour garantir la fiabilité, exécutez :
```shell
python3 -m unittest discover -s tests
```
Cette commande lance tous les tests unitaires disponibles.

## Procédures de Déploiement
Les instructions détaillées de déploiement sont disponibles dans le dossier `/deploy`. Elles comprennent des étapes spécifiques pour la mise en production.

## Comment Contribuer
Votre contribution est la bienvenue ! Pour contribuer, veuillez suivre les instructions dans [CONTRIBUTING.md](CONTRIBUTING.md). Assurez-vous de respecter nos directives de codage et de soumettre des pull requests.

## Licence
Ce projet est distribué sous la licence MIT. Consultez le fichier [LICENCE](LICENSE) pour les détails.

## Support
Pour toute question ou support, n'hésitez pas à ouvrir un ticket dans la section 'Issues' du dépôt GitHub.

