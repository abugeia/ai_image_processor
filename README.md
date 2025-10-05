# AI Image Processor

Ce script permet de modifier en masse des images à partir d'un répertoire en utilisant différents services d'intelligence artificielle (Ollama, OpenRouter, Gemini). Pour chaque image trouvée dans le répertoire `data`, le script applique une série de prompts définis dans un fichier `prompts.yaml` et sauvegarde les nouvelles images dans le répertoire `output`.

## Fonctionnalités

- Traitement par lots d'images.
- Utilisation de prompts multiples pour chaque image.
- Prise en charge de plusieurs services d'IA :
    - **Ollama** (pour une utilisation locale, par exemple avec le modèle Llava)
    - **OpenRouter**
    - **Gemini**
- Gestion sécurisée des clés d'API via un fichier `.env`.
- Sélection facile du service via la ligne de commande.

## Installation

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo
    ```

2.  **Créez un environnement virtuel avec `uv` :**
    ```bash
    uv venv
    source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
    ```

3.  **Installez les dépendances avec `uv` :**
    Le projet est maintenant géré par `uv` et `pyproject.toml`. Pour synchroniser votre environnement virtuel avec les dépendances du projet, utilisez :
    ```bash
    uv sync
    ```

## Configuration

1.  **Ajoutez vos images :**
    Placez toutes les images que vous souhaitez modifier dans le répertoire `data/`.

2.  **Définissez vos prompts :**
    Ouvrez le fichier `prompts.yaml` et ajoutez ou modifiez la liste des prompts. Chaque prompt doit être une chaîne de caractères sur une nouvelle ligne précédée d'un tiret (`-`).

3.  **Configurez vos clés d'API :**
    - Renommez le fichier `.env.example` en `.env` (s'il existe) ou créez un fichier `.env`.
    - Ouvrez le fichier `.env` et ajoutez vos clés d'API pour les services que vous souhaitez utiliser.
    ```env
    OLLAMA_API_KEY="VOTRE_CLE_API_OLLAMA" # Non requis pour une instance locale standard
    OPENROUTER_API_KEY="VOTRE_CLE_API_OPENROUTER"
    GEMINI_API_KEY="VOTRE_CLE_API_GEMINI"
    ```

## Utilisation

Le script s'exécute en ligne de commande via le fichier `main.py`. Vous devez spécifier le service que vous souhaitez utiliser.

### Exemples

-   **Pour utiliser Ollama :**
    ```bash
    python main.py ollama
    ```

-   **Pour utiliser OpenRouter :**
    ```bash
    python main.py openrouter
    ```

-   **Pour utiliser Gemini :**
    ```bash
    python main.py gemini
    ```

Le script traitera alors toutes les images du répertoire `data` avec tous les prompts de `prompts.yaml` et sauvegardera les résultats dans le répertoire `output`.
