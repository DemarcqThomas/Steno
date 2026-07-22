import os
from PIL import Image
from encoders import get_encoder_by_name


def encode_image(nom_img: str, text: str, encoder_name: str = "red") -> None:
    """Encode `text` inside `nom_img` using the named encoder.

    `encoder_name` should match one of the available encoders (eg. "red", "rgb-cycle").
    """
    enc = get_encoder_by_name(encoder_name)
    enc.encode(nom_img, text)


if __name__ == "__main__":
    fichiers = os.listdir('.')
    IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')
    images_disponibles = [f for f in fichiers if f.lower().endswith(IMAGE_EXTS)]

    if not images_disponibles:
        print("Aucune image trouvée (formats supportés: {} ).".format(", ".join(IMAGE_EXTS)))
        exit()

    print("\n--- Choisissez une image ---")
    for i, image in enumerate(images_disponibles):
        print(f"[{i + 1}] {image}")

    while True:
        choix = input("\nEntrez le numéro de l'image : ")
        if choix.isdigit() and 1 <= int(choix) <= len(images_disponibles):
            nom_img = images_disponibles[int(choix) - 1]
            break
        print("Choix invalide, réessayez.")

    try:
        print(f"Image chargée : {nom_img}")
    except Exception as e:
        print(f"Erreur : {e}")
        exit()

    text = input("Entrez votre message : ")
    encode_image(nom_img, text)
    print("\nFini.")
