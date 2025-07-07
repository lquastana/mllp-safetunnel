# mllp-safetunnel

Sécurisation des échanges HL7/MLLP entre un **EAI** et un **DPI** au moyen de Stunnel (TLS mutuel).  
Le projet fournit deux images Docker – `eai` et `dpi` – reliées par une double paire de tunnels chiffrés :


```
        +-------------+          TLS :32100                               +-------------+
        |   EAI (app) | ==lo=> [Stunnel-EAI] ~~~~~~> [Stunnel-DPI] ==lo=> |   DPI (app) |
        |             | 21010                    21010                    |             |
        +-------------+                                                   +-------------+

        +-------------+          TLS :32200                                   +-------------+
        |   DPI (app) | ==lo=> [Stunnel-DPI-out] ~~~> [Stunnel-EAI-in] ==lo=> |   EAI (app) |
        |             | 22010                    22010                        |             |
        +-------------+                                                       +-------------+
```



* `21010` : flux sortants **EAI → DPI** (HL7/MLLP clair), encapsulés dans TLS :32100  
* `22010` : flux sortants **DPI → EAI** (HL7/MLLP clair), encapsulés dans TLS :32200  

---

## Contenu du dépôt

| Répertoire / fichier | Rôle |
|----------------------|------|
| `eai/`               | Dockerfile + script de simulation (netcat) qui pousse/scrute HL7 sur 21010/22010 |
| `dpi/`               | Idem côté DPI |
| `stunnel/`           | Certificats X.509 *dev* et paires de `stunnel.conf` client / serveur |
| `docker-compose.yml` | Orchestration complète des 4 conteneurs |
| `docs/`              | Diagrammes, cheatsheets HL7, bonnes pratiques sécurité |

---

## Prérequis

* Docker ≥ 24.0 et Docker Compose v2  
* OpenSSL (génération de certificats) si vous changez les clés fournies  
* Ports libres : **21010, 22010, 32100, 32200**

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
docker compose logs -f stunnel-eai
````

---

## Détails des tunnels Stunnel

### EAI → DPI (`stunnel/eai/stunnel.conf`)

```ini
client  = yes
foreground = no
[hl7_to_dpi]
accept  = 0.0.0.0:21010      ; l’EAI se connecte ici en clair
connect = dpi:32100          ; TLS vers le serveur DPI
cert    = /certs/eai.crt
key     = /certs/eai.key
CAfile  = /certs/ca.crt
verify  = 2                  ; mTLS
options = NO_TLSv1 NO_TLSv1_1
```

### DPI (serveur) (`stunnel/dpi/stunnel.conf`)

```ini
foreground = no
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

Les conteneurs `eai` et `dpi` incluent un script bash minimal :

* `send.sh` – envoie un message HL7 depuis un fichier vers le socket local
* `listen.sh` – écoute et affiche les messages reçus

Vous pouvez ainsi tester facilement :

```bash
docker compose exec eai /app/send.sh          # pousse un ORU^R01
docker compose exec dpi /app/listen.sh        # constate la réception
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

