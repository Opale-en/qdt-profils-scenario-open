# Profils et scénarios pour QDT

Documentation officielle de QGIS Deployment Toolbelt : <https://qgis-deployment.github.io/qgis-deployment-toolbelt-cli/>

## Workflow et procédure

> [!NOTE]
> Les flèches en gras correspondent aux étapes automatisées (tâche planifiée, GPO...).

```mermaid
---
title: "Flux de travail QDT : édition, publication, déploiement"
---

flowchart TB
    subgraph Administrateurs SIG
    direction TB
        A[Poste Pierre] <---> |git pull & git push| G((fa:fa-github Repository<br>Github))
    end

    subgraph Serveur réseau local
        direction TB

        SP@{ shape: hourglass, label: "Tâche planifiée" } ==>|Pull| SRV
        SRV[["$USERPROFILE\Opale Energies Naturelles\Carto - SIG\0_RESSOURCES\2_LOGICIELS\QGIS\QDT\scenario-profils"]]

        G ==> SP
        SRV ==> AP & BP
    end
    
    subgraph Postes utilisateur final B
        direction TB

        BP@{ shape: hourglass, label: "Tâche planifiée" } ==> BW
        BW@{ shape: procs, label: "Exécution planifiée de QDT<br/>($USERPROFILE/Opale Energies Naturelles/Carto - SIG/0_RESSOURCES/2_LOGICIELS/QGIS/QDT/qdt.exe)" } ==> |Sync copie locale QDT| BC

        BC("$USERPROFILE/.cache/qgis-deployment-toolbelt")

        BC ==>|"Sync<br>(si les conditions sont remplies)"| BQ("%APPDATA%/QGIS3/profiles")
    end

    subgraph Postes utilisateur final A
        direction TB

        AP@{ shape: hourglass, label: "Tâche planifiée" } ==> AZ
        AZ@{ shape: procs, label: "Exécution planifiée de QDT<br/>($USERPROFILE/Opale Energies Naturelles/Carto - SIG/0_RESSOURCES/2_LOGICIELS/QGIS/QDT/qdt.exe)" } ==> |Sync copie locale QDT| AC

        AC("$USERPROFILE/.cache/qgis-deployment-toolbelt")

        AC ==>|"Sync<br>(si les conditions sont remplies)"| AQ("%APPDATA%/QGIS3/profiles")

    end
```

### Synchronisation Github --> Serveur réseau local

Une tâche planifiée installée sur l'ordinateur de Pierre se charge de faire un `git pull` depuis GitHub vers l'emplacement sur le réseau local : `$USERPROFILE\Opale Energies Naturelles\Carto - SIG\0_RESSOURCES\2_LOGICIELS\QGIS\QDT\scenario-profils`. C'est ce script de la documentation qui est utilisé : <https://qgis-deployment.github.io/qgis-deployment-toolbelt-cli/guides/howto_manage_private_git.html>.

Pour ce faire, un jeton d'authentification en lecture seule du projet a été créé avec la procédure ci-après :

1. Créer un jeton d'accès <https://github.com/settings/personal-access-tokens/>
1. Remplir le formulaire commme ci-dessous :

  <img width="1920" height="2106" alt="image" src="https://github.com/user-attachments/assets/52f399ab-6923-4bb8-a831-576d2783c40f" />

1. Stocker le jeton dans son gestionnaire de mots de passe
1. Stocker le jeton en variable d'environnement :
    - nom : `QDT_GH_TOKEN_SYNC_PROFILS`
    - valeur : le jeton
1. Entrer le jeton à l'invite du Git Credentials Manager dans l'onglet "Token"
