DATABASE_URL = 'mysql+mysqlconnector://julien:pass@molok:3306/anime'  # on remplacera localhost par le nom de l'host quand on passera par docker
SECRET_KEY ="272763"

HTTP_OK = 200  # Requête réussie
HTTP_CREATED = 201  # Ressource créée avec succès
HTTP_ACCEPTED = 202  # Requête acceptée mais en cours de traitement
HTTP_NO_CONTENT = 204  # Requête réussie mais aucune donnée à renvoyer

HTTP_BAD_REQUEST = 400  # Mauvaise requête (données invalides)
HTTP_UNAUTHORIZED = 401  # Authentification requise
HTTP_FORBIDDEN = 403  # Accès refusé
HTTP_NOT_FOUND = 404  # Ressource non trouvée
HTTP_METHOD_NOT_ALLOWED = 405  # Méthode HTTP non autorisée
HTTP_CONFLICT = 409  # Conflit (ex : doublon)
HTTP_UNSUPPORTED_MEDIA_TYPE = 415  # Type de média non supporté

HTTP_TOO_MANY_REQUESTS = 429  # Trop de requêtes envoyées en peu de temps

HTTP_INTERNAL_SERVER_ERROR = 500  # Erreur interne du serveur
HTTP_NOT_IMPLEMENTED = 501  # Fonctionnalité non implémentée
HTTP_BAD_GATEWAY = 502  # Problème avec une passerelle
HTTP_SERVICE_UNAVAILABLE = 503  # Service temporairement indisponible
HTTP_GATEWAY_TIMEOUT = 504  # La passerelle a expiré
