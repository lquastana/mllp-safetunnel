# mllp‑safetunnel

Sécurisation des flux HL7/MLLP entre un EAI et un DPI à l'aide de **Stunnel** en TLS mutuel (mTLS). Chaque conteneur contient :

* **Stunnel** : termine/démarre la connexion TLS.
* De petits scripts **Python** simulant l'envoi et la réception de messages HL7 (MDM, ADT…).

> Objectif : fournir un bac à sable minimal pour valider rapidement la mise en place d'une enveloppe TLS autour d'un lien MLLP avant de brancher un « vrai » EAI/DPI.

---

## ⚡ Vue d'ensemble

```text
              ┌──────────────────────┐                ┌──────────────────────┐
              │        EAI           │                │         DPI          │
Plain HL7     │ (app :21010 / 22010) │                │ (app :21010 / 22010) │ Plain HL7
 ─────────▶  │ Stunnel client       │──mTLS 32100──▶ │  Stunnel server      │──────────▶
              │  Stunnel server      │←─mTLS 32200──  │  Stunnel client      │
              └──────────────────────┘                └──────────────────────┘
```

| Sens          | Port clair | Port TLS | Rôle                                                                       |
| ------------- | ---------- | -------- | -------------------------------------------------------------------------- |
| **EAI ➜ DPI** | `21010`    | `32100`  | Le client EAI se connecte localement en clair, Stunnel chiffre vers le DPI |
| **DPI ➜ EAI** | `22010`    | `32200`  | Même principe dans l'autre sens                                            |

Seuls les ports **32100** (serveur DPI) et **32200** (serveur EAI) sont exposés à l'hôte/réseau.

---

## 🗂️ Contenu du dépôt

| Chemin               | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `eai/`               | `Dockerfile` + scripts Python simulant l'envoi/écoute côté EAI |
| `dpi/`               | Idem côté DPI                                                  |
| `stunnel/`           | CA & certificats X.509 de développement + script de génération |
| `docker-compose.yml` | Orchestration des deux conteneurs & réseaux                    |
| `docs/`              | Diagrammes, cheatsheets HL7, bonnes pratiques sécurité         |

Deux réseaux **internes** : `net_eai` et `net_dpi`. Aucun flux clair n'est exposé hors conteneurs.

---

## 🚀 Mise en route rapide

```bash
# 1. Cloner le dépôt
$ git clone https://github.com/votre_org/mllp-safetunnel.git
$ cd mllp-safetunnel

# 2. (Optionnel) Régénérer les certificats de dev
$ ./stunnel/gen-certs.sh

# 3. Lancer l'infrastructure
$ docker compose up -d

# 4. Suivre les logs
$ docker compose logs -f eai   # côté EAI
$ docker compose logs -f dpi   # côté DPI
```

> **Astuce** : ajoutez `--build` pour reconstruire les images après modification des scripts.

---

## 🔧 Détails des configurations Stunnel

### EAI ➜ DPI (`eai/stunnel.conf`)

```ini
client      = yes
foreground  = yes
[hl7_to_dpi]
accept      = 0.0.0.0:21010   ; l'EAI se connecte ici en clair
connect     = dpi:32100       ; Stunnel chiffre vers le DPI
cert        = /certs/eai.crt
key         = /certs/eai.key
CAfile      = /certs/ca.crt
verify      = 2               ; mTLS obligatoire
sslVersion  = TLSv1.2
```

Le script `send.sh` du conteneur **EAI** écrit toujours sur `localhost:21010`. Stunnel relaie en TLS vers `dpi:32100`.

### DPI ➜ EAI (`dpi/stunnel.conf`)

```ini
foreground = yes
[hl7_from_eai]
accept     = 0.0.0.0:32100    ; écoute TLS
connect    = 127.0.0.1:21010  ; redirige vers l'app DPI en clair
cert       = /certs/dpi.crt
key        = /certs/dpi.key
CAfile     = /certs/ca.crt
verify     = 2
```

Le flux retour utilise `22010` (clair) ↔ `32200` (TLS) suivant la même logique.

---

## 🧪 Simulation des flux HL7

Scripts disponibles dans chaque conteneur :

| Script         | Rôle                                                                                                |
| -------------- | --------------------------------------------------------------------------------------------------- |
| `send.sh`      | Envoie un message HL7 depuis `message.hl7` vers le socket local, attend un ACK, log dans `send.log` |
| `send_loop.sh` | Relance `send.sh` toutes les 20 s (démarré automatiquement)                                         |
| `listen.sh`    | Écoute le port clair, affiche / log les messages reçus (`listen.log`) et renvoie un ACK             |
| `server.py`    | Petit serveur MLLP appelé par `listen.sh`                                                           |
| `stunnel.log`  | Journal Stunnel                                                                                     |

### Exemples de test

```bash
# Envoyer un MDM^T02 du EAI vers le DPI
$ docker compose exec eai /app/send.sh

# Vérifier la réception côté DPI
$ docker compose exec dpi /app/listen.sh

# Flux inverse : ADT^A01 du DPI vers l'EAI
$ docker compose exec dpi /app/send.sh
$ docker compose exec eai /app/listen.sh
```

---

## 🛠️ Personnalisation

| Besoin                       | Fichier(s) à modifier                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| **Certificats de prod**      | Remplacer les CRT/KEY dans `stunnel/` (penser à la CA)                                 |
| **Changement de ports**      | `stunnel/*.conf` + `docker-compose.yml`                                                |
| **Brancher un vrai EAI/DPI** | Remplacer l'image de simulation par votre application réelle dans `docker-compose.yml` |

---



## 📄 Licence

[MIT](LICENSE) – librement réutilisable et adaptable aux besoins hospitaliers.

---

## 🙌 Contribuer

Les PR sont les bienvenues ! Ouvrez un ticket pour discuter d'une fonctionnalité ou d'un correctif avant de soumettre.
