from abc import ABC, abstractmethod

class ImageProcessingService(ABC):
    """
    Classe de base abstraite pour les services de traitement d'images.
    Définit l'interface commune que tous les clients de service doivent implémenter.
    """

    def __init__(self, api_key=None):
        """
        Initialise le service avec une clé d'API optionnelle.
        """
        self.api_key = api_key

    @abstractmethod
    def process_image(self, image_path: str, prompt: str) -> str:
        """
        Méthode abstraite pour traiter une image avec un prompt donné.

        Args:
            image_path (str): Le chemin vers l'image à traiter.
            prompt (str): Le prompt décrivant la modification à appliquer.

        Returns:
            str: Le chemin vers la nouvelle image sauvegardée.
                 Retourne None en cas d'échec.
        """
        pass

# Les implémentations concrètes pour chaque service (Ollama, OpenRouter, Gemini)
# seront ajoutées ici plus tard.

import requests
import base64
import os
import time

class OllamaService(ImageProcessingService):
    """
    Client pour le service de traitement d'images Ollama (par exemple, avec un modèle comme Llava).
    """

    def __init__(self, api_key=None, model="llava", api_url="http://localhost:11434/api/generate"):
        super().__init__(api_key)
        self.model = model
        self.api_url = api_url

    def process_image(self, image_path: str, prompt: str) -> str:
        print(f"Traitement de '{image_path}' avec Ollama et le prompt : '{prompt}'...")

        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "images": [encoded_string]
            }

            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP

            # NOTE : Le code ci-dessous est une simulation.
            # La réponse réelle de l'API Ollama/Llava pour la génération d'images
            # à partir d'une image et d'un prompt peut être différente.
            # Il faudra l'adapter en fonction de la documentation de l'API.
            
            # Simulation : on suppose que l'API retourne l'image modifiée en base64
            # new_image_data = response.json().get("image_data")
            # if not new_image_data:
            #     print("Erreur : Aucune donnée d'image retournée par l'API Ollama.")
            #     return None
            #
            # image_bytes = base64.b64decode(new_image_data)

            # Pour la simulation, nous allons simplement copier l'image originale
            with open(image_path, 'rb') as f_in:
                image_bytes = f_in.read()


            # Sauvegarde de la nouvelle image
            base, ext = os.path.splitext(os.path.basename(image_path))
            timestamp = int(time.time())
            output_filename = f"{base}_ollama_{timestamp}{ext}"
            output_path = os.path.join("output", output_filename)

            with open(output_path, "wb") as f:
                f.write(image_bytes)

            print(f"Nouvelle image sauvegardée sous : {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Une erreur d'API est survenue avec Ollama : {e}")
            return None
        except IOError as e:
            print(f"Une erreur de lecture/écriture de fichier est survenue : {e}")
            return None

class OpenRouterService(ImageProcessingService):
    """
    Client pour le service de traitement d'images OpenRouter.
    """

    def __init__(self, api_key, model="google/gemini-pro-vision", api_url="https://openrouter.ai/api/v1/chat/completions"):
        super().__init__(api_key)
        if not self.api_key:
            raise ValueError("La clé d'API OpenRouter est requise.")
        self.model = model
        self.api_url = api_url

    def process_image(self, image_path: str, prompt: str) -> str:
        print(f"Traitement de '{image_path}' avec OpenRouter et le prompt : '{prompt}'...")

        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                image_data_url = f"data:image/jpeg;base64,{encoded_string}"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_data_url}}
                        ]
                    }
                ]
            }

            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()

            # NOTE : Le code ci-dessous est une simulation.
            # La réponse réelle de l'API OpenRouter pour la génération d'images
            # peut être différente. Il faudra l'adapter.
            
            # Simulation : on suppose que l'API retourne l'image modifiée en base64
            # new_image_data = response.json().get("choices").get("message").get("content")
            # if not new_image_data:
            #     print("Erreur : Aucune donnée d'image retournée par l'API OpenRouter.")
            #     return None
            #
            # image_bytes = base64.b64decode(new_image_data)

            # Pour la simulation, nous allons simplement copier l'image originale
            with open(image_path, 'rb') as f_in:
                image_bytes = f_in.read()

            # Sauvegarde de la nouvelle image
            base, ext = os.path.splitext(os.path.basename(image_path))
            timestamp = int(time.time())
            output_filename = f"{base}_openrouter_{timestamp}{ext}"
            output_path = os.path.join("output", output_filename)

            with open(output_path, "wb") as f:
                f.write(image_bytes)

            print(f"Nouvelle image sauvegardée sous : {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Une erreur d'API est survenue avec OpenRouter : {e}")
            return None
        except (IOError, ValueError) as e:
            print(f"Une erreur est survenue : {e}")
            return None

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

class GeminiService(ImageProcessingService):
    """
    Client pour le service de traitement d'images Gemini de Google.
    """

    def __init__(self, api_key, model="gemini-2.5-flash-image"):
        super().__init__(api_key)
        if not self.api_key:
            raise ValueError("La clé d'API Gemini est requise.")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model

    def process_image(self, image_path: str, prompt: str) -> str:
        print(f"Traitement de '{image_path}' avec Gemini et le prompt : '{prompt}'...")

        try:
            img = Image.open(image_path)
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, img],
            )

            # Parcourir les parties de la réponse selon la documentation officielle
            text_responses = []
            image_generated = False
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    text_responses.append(part.text)
                    print(f"Réponse texte de Gemini : {part.text}")
                elif part.inline_data is not None:
                    # Image générée trouvée
                    image_generated = True
                    generated_image = Image.open(BytesIO(part.inline_data.data))
                    
                    # Sauvegarde de la nouvelle image
                    base, _ = os.path.splitext(os.path.basename(image_path))
                    timestamp = int(time.time())
                    output_filename = f"{base}_gemini_{timestamp}.png"
                    output_path = os.path.join("output", output_filename)
                    
                    generated_image.save(output_path)
                    print(f"Nouvelle image générée sauvegardée sous : {output_path}")
                    return output_path

            # Si aucune image n'a été générée mais qu'il y a une réponse texte
            if not image_generated:
                if text_responses:
                    print("Note : Gemini a fourni une réponse texte mais pas d'image générée.")
                    # Pour la simulation, copier l'image originale avec annotation
                    with open(image_path, 'rb') as f_in:
                        image_bytes = f_in.read()

                    # Sauvegarde de l'image (copie) avec annotation textuelle
                    base, ext = os.path.splitext(os.path.basename(image_path))
                    timestamp = int(time.time())
                    output_filename = f"{base}_gemini_text_{timestamp}{ext}"
                    output_path = os.path.join("output", output_filename)

                    with open(output_path, "wb") as f:
                        f.write(image_bytes)

                    print(f"Image copiée avec analyse Gemini sauvegardée sous : {output_path}")
                    return output_path
                else:
                    print("Erreur : Aucune réponse (texte ou image) retournée par l'API Gemini.")
                    return None

        except Exception as e:
            print(f"Une erreur est survenue avec Gemini : {e}")
            return None
