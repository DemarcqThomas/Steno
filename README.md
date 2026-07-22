# Steno

Steno est un petit outil Python de stéganographie permettant de cacher un texte dans une image sans modifier visiblement son apparence.

Le projet implémente plusieurs méthodes d'encodage dans les pixels d'une image, principalement via les bits de poids faible (LSB) et les bits de poids fort (MSB) sur les canaux RGB.

## ✨ Fonctionnalités

- Encodage d'un texte dans une image
- Décodage d'un message à partir d'une image
- Support de plusieurs encodeurs RGB
- Interface interactive en ligne de commande
- Interface TUI avec `curses` pour une utilisation guidée

## 🧠 Encodeurs disponibles

Le dépôt expose les encodeurs suivants dans [encoders.py](encoders.py) :

- `LSB-red`
- `LSB-green`
- `LSB-blue`
- `LSB-rgb-cycle`
- `MSB-red`
- `MSB-green`
- `MSB-blue`

## 📁 Structure du projet

- [main.py](main.py) : script interactif pour encoder un message dans une image
- [decode.py](decode.py) : script interactif pour décoder un message depuis une image
- [cli.py](cli.py) : interface texte (TUI) pour choisir entre encoder et décoder
- [encoders.py](encoders.py) : implémentation des méthodes de stéganographie
- [test_blue.py](test_blue.py) : test de validation pour l'encodeur `BlueLSBEncoder`

## ⚙️ Prérequis

Python 3 et la dépendance suivante :

```bash
pip install pillow
```

## 🚀 Utilisation

### 1. Lancer l'interface TUI

```bash
python3 cli.py
```

Cette interface propose :

- l'encodage d'un message dans une image,
- le décodage d'un message depuis une image,
- et la sortie du programme.

### 2. Utiliser le script principal

```bash
python3 main.py
```

Le script liste les images disponibles dans le dossier courant et vous guide pour :

1. choisir une image,
2. saisir le texte à cacher,
3. encoder le message dans l'image.

### 3. Décoder un message

```bash
python3 decode.py
```

Le message décodé est sauvegardé dans un fichier du type :

```text
Output_decode_<nom_image>.txt
```

## 🛠️ Exemple de flux

1. Place une image dans le dossier du projet.
2. Lance `python3 cli.py`.
3. Choisis l'option d'encodage.
4. Sélectionne une image.
5. Saisis le message à cacher.
6. Relance `python3 decode.py` pour le retrouver.

## ⚠️ Note importante

Ce projet est une démonstration de stéganographie dans des images. Il ne fournit pas de chiffrement robuste ni de protection cryptographique avancée.

## 🧪 Vérification rapide

```bash
python3 test_blue.py
```

Ce test crée une image de démonstration, encode un message avec `BlueLSBEncoder`, puis vérifie que le message est bien décodé sans perte.

## 📌 À retenir

Steno est un projet simple et pédagogique pour comprendre les bases de la stéganographie dans les images en Python.
