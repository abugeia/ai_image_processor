import yaml

def load_prompts(file_path="prompts.yaml"):
    """
    Charge la liste des prompts depuis un fichier YAML.

    Args:
        file_path (str): Le chemin vers le fichier de prompts.

    Returns:
        list: Une liste de prompts.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
            if not isinstance(prompts, list):
                print(f"Erreur : Le fichier '{file_path}' doit contenir une liste de prompts.")
                return []
            return prompts
    except FileNotFoundError:
        print(f"Le fichier de prompts '{file_path}' n'a pas été trouvé.")
        return []
    except yaml.YAMLError as e:
        print(f"Erreur lors de la lecture du fichier YAML '{file_path}': {e}")
        return []

import argparse
import config
from image_processor import list_image_files
from services import OllamaService, OpenRouterService, GeminiService

def main():
    """
    Fonction principale pour orchestrer le traitement des images.
    """
    # --- Gestion des arguments de la ligne de commande ---
    parser = argparse.ArgumentParser(description="Modifie des images en utilisant un service d'IA.")
    parser.add_argument(
        "service",
        choices=["ollama", "openrouter", "gemini"],
        help="Le service à utiliser pour le traitement des images."
    )
    args = parser.parse_args()

    # --- Étape 1: Charger les prompts ---
    prompts = load_prompts()
    if not prompts:
        print("Aucun prompt trouvé. Arrêt du script.")
        return

    # --- Étape 2: Lister les images ---
    image_paths = list_image_files()
    if not image_paths:
        print("Aucune image trouvée dans le répertoire 'data'. Arrêt du script.")
        return

    # --- Étape 3: Sélectionner et initialiser le service ---
    service = None
    if args.service == "ollama":
        service = OllamaService()
    elif args.service == "openrouter":
        if not config.OPENROUTER_API_KEY:
            print("Erreur : La clé OPENROUTER_API_KEY n'est pas définie dans le fichier .env")
            return
        service = OpenRouterService(api_key=config.OPENROUTER_API_KEY)
    elif args.service == "gemini":
        if not config.GEMINI_API_KEY:
            print("Erreur : La clé GEMINI_API_KEY n'est pas définie dans le fichier .env")
            return
        service = GeminiService(api_key=config.GEMINI_API_KEY)

    print(f"Utilisation du service : {args.service}")

    # --- Étape 4: Traiter chaque image avec chaque prompt ---
    print(f"\nDébut du traitement de {len(image_paths)} image(s) avec {len(prompts)} prompt(s)...")
    total_generations = 0
    for image_path in image_paths:
        for prompt in prompts:
            new_image_path = service.process_image(image_path, prompt)
            if new_image_path:
                total_generations += 1
    
    print(f"\nTraitement terminé. {total_generations} nouvelle(s) image(s) créée(s) dans le répertoire 'output'.")


if __name__ == "__main__":
    main()
