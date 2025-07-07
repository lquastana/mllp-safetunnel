# mllp-safetunnel

Sécurisation des échanges HL7/MLLP entre un **EAI** et un **DPI** à l'aide de Stunnel (TLS mutuel). Chaque conteneur intègre Stunnel et de petits scripts Python pour simuler l'envoi et la réception de messages.

```
EAI (21010/22010) <--TLS 32100/32200--> DPI
```

* `21010` : flux sortants **EAI → DPI** en clair redirigés vers Stunnel
* `22010` : flux sortants **DPI → EAI** en clair redirigés vers Stunnel
* Seuls les ports TLS `32100` (DPI) et `32200` (EAI) sont exposés

## Contenu du dépôt

| Répertoire / fichier | Rôle |
|----------------------|------|
| `eai/`               | Dockerfile et scripts Python simulant l'envoi/réception HL7 |
| `dpi/`               | Idem côté DPI |
| `stunnel/`           | Certificats X.509 *dev* |
| `docker-compose.yml` | Orchestration des deux conteneurs |
| `docs/`              | Diagrammes, cheatsheets HL7, bonnes pratiques sécurité |

Les conteneurs utilisent deux réseaux internes : `net_eai` et `net_dpi`. Seuls les ports TLS sont exposés à l'hôte.

---

## Prérequis

* Docker ≥ 24.0 et Docker Compose v2  
* OpenSSL (génération de certificats) si vous changez les clés fournies  
* Ports libres : **32100, 32200** (21010 et 22010 restent internes)

---

## Lancement rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre_org/mllp-safetunnel.git
cd mllp-safetunnel

# 2. (Optionnel) régénérer les certificats
./stunnel/gen-certs.sh

# 3. Démarrer l'ensemble
docker compose up -d

# 4. Vérifier
docker compose logs -f eai
````

---

## Détails des tunnels Stunnel

### EAI → DPI (`eai/stunnel.conf`)

```ini
client  = yes
foreground = yes
[hl7_to_dpi]
accept  = 0.0.0.0:21010      ; l’EAI se connecte ici en clair
connect = dpi:32100          ; TLS vers le serveur DPI
cert    = /certs/eai.crt
key     = /certs/eai.key
CAfile  = /certs/ca.crt
verify  = 2                  ; mTLS
sslVersion = TLSv1.2
```

### DPI (serveur) (`dpi/stunnel.conf`)

```ini
foreground = yes
[hl7_from_eai]
accept  = 0.0.0.0:32100      ; écoute TLS
connect = 127.0.0.1:21010    ; redirige vers l’app DPI en clair
cert    = /certs/dpi.crt
key     = /certs/dpi.key
CAfile  = /certs/ca.crt
verify  = 2
```

> Les tunnels **retour** (DPI → EAI) suivent le même schéma avec les ports `22010` (clair) et `32200` (TLS).

---

## Simulation des flux HL7

Les conteneurs `eai` et `dpi` incluent des scripts Python simples :

* `send.sh` – envoie un message HL7 depuis un fichier vers le socket local (journalise dans `send.log`)
* `listen.sh` – écoute et affiche les messages reçus (journalise dans `listen.log`)
* `stunnel.log` – journal de Stunnel (client et serveur)
* `server.log` – journal du serveur MLLP lancé au démarrage du conteneur
Les logs sont visibles via `docker compose logs` et conservés sur disque.

Vous pouvez ainsi tester facilement :

```bash
docker compose exec eai /app/send.sh          # envoie un MDM^T02 vers le DPI
docker compose exec dpi /app/listen.sh        # constate la réception côté DPI

docker compose exec dpi /app/send.sh          # envoie un ADT^A01 vers l'EAI
docker compose exec eai /app/listen.sh        # constate la réception côté EAI
```

---

## Personnalisation

| Besoin                          | Où modifier                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| Ajouter des certificats de prod | remplacer `stunnel/ca.crt`, `eai.crt`, `dpi.crt`, etc.       |
| Changer les ports               | éditer `stunnel.conf` + `docker-compose.yml`                 |
| Monter un vrai EAI / DPI        | remplacer l’image de simulation par votre application réelle |

---

## Sécurité & bonnes pratiques

1. **mTLS obligatoire** (`verify = 2`).
2. Rotation des certificats : script `gen-certs.sh` prévu pour du renouvellement.
3. Pare-feu extérieur : ouvrez uniquement `32100` et `32200` entre les deux hôtes.
4. Surveiller `stunnel.log`; passer `debug = notice` en prod.

---

## Licence

MIT – adaptable aux besoins hospitaliers (conformité HDS / SEGUR à vérifier selon vos flux réels).

---

## Auteur

Laurent Quastana (@laurent.quastana) – Poupie Family
Contributions bienvenues !
