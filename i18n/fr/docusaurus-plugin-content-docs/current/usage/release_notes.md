---
# Le reste de la sidebar est encore en anglais : on garde le libellé anglais pour rester cohérent.
# Retirer cette ligne quand la majorité des pages seront traduites.
sidebar_label: Release Notes
---

# Notes de version

<!--
  Format des titres de version (à conserver pour chaque nouvelle version, les ancres doivent rester stables) :

    ## Version X.Y.Z (YYYY-MM-DD) {#vX-Y-Z}

  - La date est au format ISO 8601 (YYYY-MM-DD).
  - L'ancre explicite {#vX-Y-Z} ne dépend que du numéro de version : remplacer chaque point par un tiret.
    Exemple : 1.7.11 -> {#v1-7-11}, 1.71.1 -> {#v1-71-1}.
  - Les ancres DOIVENT être identiques à celles de la version anglaise (docs/usage/release_notes.md).
  - Ne PAS se fier à l'ancre auto-générée : Docusaurus supprime les points, donc 1.7.11 et 1.71.1
    donneraient tous deux "version-1711", et changer la date changerait le lien.
-->

## Version 1.8.5 (2026-11-09) {#v1-8-5}

### Nouveautés ✨

#### Layers
- **Override Layers** : à la création d'un layer, et lors de son édition ensuite, il est possible de choisir entre Additive et Override. Attention : l'ordre compte ! Les layers peuvent être déplacés vers le haut ou le bas via le menu contextuel. Les layers Override sont affichés sous forme de cercle (additive = carré).
- **Option "Float only"** pour les layers additifs.
- **Layers pour les booléens (True/False) et les entiers** (choix énumérés, comme les FPS Body/World/Face sur le World), en override uniquement (pas d'additif pour ces types).
- **Usage plugs** : un plug à l'intérieur d'un layer peut être temporairement ignoré. Activez le layer, faites un clic droit sur le plug dans le layer (ex. "Translate X") > Add Usage Plug. Un nouveau plug apparaît tout en bas, avec le même nom et le suffixe " Usage" (ex. "Translate X Usage"). Il est keyable (un float pour les plugs de type float). Le désactiver exclut le plug d'origine du calcul.

#### Tweak Tools
- **Bake** : bake toutes les X frames (avec une gestion spéciale des contraintes) et supprime les clés qui ne sont pas sur les bonnes frames.
- **Simplify Densify** : permet d'ajouter ou de supprimer des clés sur les courbes d'animation. La suppression retire en premier les clés qui affectent le moins la forme de la courbe.
- **Smooth Rough** : lisse ou accentue les courbes d'animation.
- **Connect** : réajuste un bloc de la courbe, ou un bloc de clés sélectionnées, pour le raccorder à la pose précédente ou suivante.
- **Blend to Neighbor** : mélange la pose ou les clés sélectionnées vers le voisin de gauche ou de droite. Contrairement à Tween, qui ignore la valeur courante et mélange à partir des deux voisins, cet outil part de la valeur courante et l'estompe vers un seul voisin, selon la direction du tweak.
- **Scale from Average** : met à l'échelle les clés en utilisant la moyenne de chaque bloc contigu de clés sélectionnées comme pivot.
- **Scale from Mid-range** : met à l'échelle les clés en utilisant la moyenne des deux extrêmes de chaque bloc contigu de clés sélectionnées comme pivot.
- **Staggered Rephase** : similaire à Rephase, mais chaque contrôleur reçoit un décalage différent, afin de synchroniser l'animation tout en conservant la synchronisation du timing des clés.
- **Rephase** : nouveau mode Frames, nouvelle option Fit (la décocher pour que l'outil ne modifie pas les modes de tangentes existants), et comportement plus précis sur les courbes contenant de petites valeurs.
- Les tweak tools sont 10 à 15 % plus rapides.

#### Divers
- Amélioration de l'édition des canaux int au clic milieu, désormais utilisable aussi sur les booléens (true/false).
- Le cycle baking fonctionne maintenant aussi sur les courbes booléennes et entières (auparavant uniquement les courbes décimales).
- Ajout d'un bouton pour baker les contraintes sélectionnées sur chaque frame où elles sont actives, puis supprimer les contraintes.

#### Timeline & Range slider
- **Frame** (raccourci "F") sur la timeline : le range slider s'ajuste aux clés sélectionnées.
- Double-clic sur le range slider : bascule entre la plage complète du plan et la précédente.

#### Import / Sauvegarde / Library
- **Import de fichiers mocap en FBX.**
- L'auto-save est activé par défaut, et son dossier est épinglé dans la barre latérale de la fenêtre de chargement de fichiers "shot".
- L'auto-load privilégie désormais le fichier le plus proche de la racine du serveur plutôt que le plus profond lorsque deux fichiers sont candidats.
- Une boîte de dialogue prévient l'utilisateur qu'un asset buildé (c'est-à-dire non importé) ne peut pas être sauvegardé dans un .shot.

### Corrections 🐛
- Les courbes en escalier (step) avec cycles sont maintenant correctement affichées dans le curve editor.
- Les clés inter-frames pouvaient produire des résultats non déterministes.
- Corrections sur l'undo pour les layers sans animation, ainsi que sur la suppression et le renommage d'un layer.
- Le quick fix pour les FPS animés est généralisé à tous les rigs (il dépendait auparavant des rigs TT).
- Pan zoom 2D : le reset (touche retour arrière) provoquait un comportement incohérent avec le toggle d'activation/désactivation, et le rectangle de preview était erroné lors d'un pan sans changement de zoom.
- Le tweak tool Blend to Bindpose fonctionne maintenant avec les dummies.
- La création du shot cluster est ignorée au chargement d'un shot si son contrôleur parent n'existe plus (asset modifié).
- Les chemins UDIM pointant vers un dossier inaccessible sont ignorés.
- Library :
  - Request auto-incrémente désormais les éléments provenant de layers de même nom au lieu de les écraser.
  - Migration et import corrigés pour les anciens formats de clips bakés contenant du shot rig (dummies, cluster, contrainte…).
  - Import corrigé lorsque le clip ne contenait que du shot rig et aucune donnée d'animation/pose d'un asset.
  - Divers correctifs sur les shot clusters bankés (ajout automatique de stick controller, problème d'identification de la géométrie).
- Crash aléatoire du viewport lors de la suppression d'un nœud de géométrie de la scène.
- Crash lors de la suppression d'un asset ou d'un dummy avec un motion trail actif.

### Dev/Rig ⚙
- `mg.get_attr("{ns}", "ctrl", "attribute")` est disponible pour les boutons de script de picker.
- Les paramètres d'interpolation des contraintes multi-cibles sont maintenant définis directement sur le nœud de contrainte.
- **Export USD** :
  - Ouvertures de caméra converties en millimètres.
  - Correction d'un crash lors de l'export direct d'un nœud asset (cas de la caméra ; contournement = exporter ses nœuds "geo" et "world" par leur nom).
  - Meilleure préservation des chemins relatifs.
- Export de package de shot localisé amélioré : prend en compte les animations et pickers référencés, ajoute un dossier de lib serveur par défaut.
- Mikan 1.0.10.
