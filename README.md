# Suivi de Drones en Temps Réel

Ce projet implémente un système de suivi de drones en temps réel, exploitant la puissance de la bibliothèque YOLO et de NVIDIA TensorRT, et est optimisé pour fonctionner sur une NVIDIA Jetson Nano.

## Sommaire

- [Présentation des Fonctionnalités](#présentation-des-fonctionnalités)
- [Guide d'Installation](#guide-dinstallation)
- [Configuration et Dépendances](#configuration-et-dépendances)
- [Utilisation](#utilisation)
- [Personnalisation et Entraînement de Modèle](#personnalisation-et-entraînement-de-modèle)
- [Conversion de Modèles](#conversion-de-modèles)
- [Tests et Validation](#tests-et-validation)
- [Procédures de Déploiement](#procédures-de-déploiement)
- [Contribuer au Projet](#contribuer-au-projet)
- [Licence](#licence)

## Présentation des Fonctionnalités

- **Détection et Suivi en Temps Réel** : Utilisation de YOLO pour la détection et le suivi dynamique des drones.
- **Suivi Avancé** : Capacité à suivre les drones en dépit de mouvements rapides ou de changements soudains de trajectoire.
- **Intégration des Capteurs NVIDIA** : Exploitation des capteurs NVIDIA pour une précision accrue.
- **Affichage des Informations de Suivi** : Visualisation en temps réel des données de suivi pour une surveillance efficace.
- **Compatibilité Caméra** : Prise en charge de diverses caméras fonctionnant avec Jetson Nano.
- **Choix de Modèle YOLO** : Flexibilité dans le choix du modèle YOLO adapté à vos besoins.

## Guide d'Installation

### Prérequis Système et Logiciel

```
sudo apt-get update
sudo apt-get install -y liblapack-dev libblas-dev gfortran libfreetype6-dev libopenblas-base libopenmpi-dev libjpeg-dev zlib1g-dev
sudo apt-get install -y python3-pip
pip install -r requirements.txt
```

## Configuration et Dépendances

- **Jetson Nano** : Developer Kit Version - Jetpack 4.6 [L4T 32.6.1]
- **Logiciels et Bibliothèques** : Cuda 10.2.300, OpenCV 4.1.1, TensorRT 8.0.1.6, cuDNN 8.2.1.32, PyTorch v1.10, torchvision v0.11.1, Python 3.6+, YOLOv5-7
- **Installation Additionnelle** :
   - **PyCuda** :
     ```
     export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}
     export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH
     pip install pycuda --user
     ```
     
   - **Seaborn** :
     ```
     sudo apt install python3-seaborn
     ```

   - **Installation de PyTorch et TensorRT** : Suivez les instructions sur [ce lien](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048) pour installer PyTorch, torchvision sur Jetson Nano (choisir la version PyTorch v1.10 - torchvision v0.11.1).

## Utilisation de YoloV5 avec le Moteur TensorRT sur Jetson

### Génération du fichier wts à partir du fichier pt

Yolov5s.pt et Yolov5n.pt sont déjà fournis dans le repo. Mais si vous le souhaitez, vous pouvez télécharger une autre version du modèle yolov5. Exécutez ensuite la commande ci-dessous pour convertir le fichier .pt en fichier .wts :

```
cd JetsonYoloV5
python3 gen_wts.py -w yolov5s.pt -o yolov5s.wts
```

### Compilation

Créez un répertoire de compilation à l'intérieur de yolov5. Copiez et collez le fichier wts généré dans le répertoire de compilation et exécutez les commandes suivantes. Si vous utilisez un modèle personnalisé , assurez-vous de mettre à jour kNumClas dans yolov5/src/config.h :

```
 cd yolov5/
 mkdir build
 cd build
 cp ../../yolov5s.wts .
 cmake ..
 make 
```

### Construction du fichier Engine

```
./yolov5_det -s yolov5s.wts yolov5s.engine s
```

### Test du fichier Engine

```
./yolov5_det -d yolov5s.engine ../images
```

Cela réalisera l'inférence sur les images et les résultats seront sauvegardés dans le répertoire de compilation.

## Utilisation

Pour démarrer le suivi des drones :

```
python3 track_drones.py
```

## Personnalisation et Entraînement de Modèle

Instructions pour entraîner votre propre modèle YOLO personnalisé.

## Conversion de Modèles

Guide pour convertir un modèle `.pt` en format `.engine` adapté à TensorRT.

## Tests et Validation

Exécutez des tests unitaires pour garantir la fiabilité :

```
python3 -m unittest discover -s tests
```

## Procédures de Déploiement

Instructions détaillées disponibles dans le dossier `/deploy` pour une mise en production.

## Contribuer au Projet

Instructions pour contribuer au développement et à l'amélioration du projet.

## Licence

Ce projet est distribué sous la licence MIT. Veuillez consulter le fichier [LICENCE](LICENSE) pour les détails complets sur l'utilisation et la distribution.
