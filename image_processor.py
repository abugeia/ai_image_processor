import os

def list_image_files(directory="data"):
    """
    Liste tous les fichiers image dans un répertoire donné.

    Args:
        directory (str): Le chemin vers le répertoire des images.

    Returns:
        list: Une liste des chemins complets vers les fichiers image.
    """
    image_files = []
    supported_extensions = ['.png', '.jpg', '.jpeg', '.webp', '.bmp']
    if not os.path.isdir(directory):
        print(f"Le répertoire '{directory}' n'a pas été trouvé.")
        return image_files

    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            image_files.append(os.path.join(directory, filename))
    return image_files