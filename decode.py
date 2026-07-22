#!/usr/bin/env python3
import os
from PIL import Image


def decode_image(nom_img: str, encoder_name: str = "red") -> str:
    """Decode message from `nom_img` using the named encoder.

    Writes output to `Output_decode_<nom_img>.txt` and returns the message.
    """
    from encoders import get_encoder_by_name

    enc = get_encoder_by_name(encoder_name)
    message = enc.decode(nom_img)

    out_name = "Output_decode_" + nom_img + ".txt"
    with open(out_name, "w", encoding="utf-8", errors="ignore") as f:
        f.write(message)

    return message


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

    message = decode_image(nom_img)
    print("Fini.")
