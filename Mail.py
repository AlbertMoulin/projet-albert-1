import webbrowser
import urllib.parse

class Mail:

    def __init__(self):
        pass

    def create_mail(To, Content, Header):
        """
    Fonction : create_mail

    Description : Crée un brouillon d'email sans l'envoyer automatiquement.

    Paramètres :
    - To (string) : L'adresse email du destinataire (ex: "mairie@ville.fr")
    - Content (string) : Le contenu complet de l'email, incluant la salutation, le message principal, les questions et la signature
    - Header (string) : L'objet de l'email qui résume le but du message

    Fonctionnement :
    - Ouvre le client de messagerie par défaut de l'utilisateur avec un nouveau message pré-rempli
    - Utilise le protocole "mailto:" pour créer un lien vers un nouvel email

    Note : Cette fonction prépare uniquement l'email dans le client de messagerie par défaut. L'envoi devra être confirmé manuellement par l'utilisateur.

    Exemple d'utilisation :
    create_mail(
        To="mairie@paris.fr",
        Content="Madame, Monsieur,\n\nJe vous écris pour me renseigner sur la procédure d'obtention d'un permis d'entreprise dans votre municipalité...\n\nMerci pour votre aide.\n\nCordialement,\nJean Dupont\nTéléphone: 06 12 34 56 78",
        Header="Demande d'informations sur les permis d'entreprise"
    )
    """
        params = {
            "subject": Header,
            "body": Content
        }


        url = f"mailto:{To}?{urllib.parse.urlencode(params).replace('+', '%20')}"

        webbrowser.open(url)
