# mawqi-tamwil
Ce projet vise à créer une carte interactive et accessible des ressources financières à travers le Maroc, permettant aux individus de localiser facilement les banques, les institutions de microfinance et d'autres services financiers à proximité. 
# Mawqia Tamwil (Localisateur Financier)

Ce projet vise à créer une carte interactive et accessible des ressources financières à travers le Maroc, permettant aux individus de localiser facilement les banques, les institutions de microfinance et d'autres services financiers à proximité. Il utilise les données ouvertes de Bank Al-Maghrib pour promouvoir l'inclusion financière et améliorer l'accès aux services financiers pour tous les Marocains.  Ce projet a été développé dans le cadre du hackathon Open Data.

## Table des matières

- [Introduction](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Sources de données](#sources-de-données)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribution](#contribution)
- [Licence](#licence)
- [Contact](#contact)

## Introduction

L'accès aux services financiers est un facteur crucial pour l'autonomisation économique et le développement social. "Mawqia Tamwil" cherche à combler le fossé de l'inclusion financière en fournissant une plateforme conviviale qui simplifie la recherche de ressources financières. Que vous soyez un particulier à la recherche d'une agence bancaire locale, un micro-entrepreneur en quête d'options de microfinance ou un chercheur étudiant l'accès financier, ce projet offre un outil précieux.

## Fonctionnalités

*   **Carte interactive:** Explorez une carte du Maroc avec des marqueurs indiquant l'emplacement des institutions financières.
*   **Recherche et filtrage:** Recherchez facilement des institutions spécifiques par nom ou filtrez par région, type d'institution (banque, microfinance, etc.) ou services offerts (lorsque les données sont disponibles).
*   **Informations détaillées:** Cliquez sur un marqueur pour afficher des informations détaillées sur l'institution, notamment le nom, l'adresse, les coordonnées et les services offerts (lorsque disponibles).
*   **Téléchargement des données:** Téléchargez les données sous-jacentes au format CSV pour une analyse ou une utilisation ultérieure.
*   **(Futur) Support multilingue:** Options linguistiques arabe et français.
*   **(Futur) Contributions des utilisateurs:** Permettre aux utilisateurs de contribuer aux données en suggérant de nouveaux emplacements ou des mises à jour.

## Technologies utilisées

*   **Cartographie:** Leaflet (bibliothèque JavaScript pour les cartes interactives)
*   **Traitement des données:** Python (avec la bibliothèque Pandas)
*   **Géocodage:** OpenStreetMap Nominatim (pour convertir les adresses en coordonnées)
*   **Développement Web:** HTML, CSS, JavaScript
*   **Stockage des données:** CSV (Comma Separated Values)
*   **Contrôle de version:** Git & GitHub

## Sources de données

*   **Source de données principale:** "Détail implantation bancaire au 31 décembre 2022" de Bank Al-Maghrib.
*   **Sources de données potentielles futures:** Données sur les institutions de microfinance, les agences de transfert d'argent, les coopératives de crédit, les services financiers mobiles et les programmes de littératie financière (de Bank Al-Maghrib ou d'autres organisations pertinentes).

## Installation

1.  Clonez le dépôt :

    ```bash
    git clone [https://github.com/MohamedELHAMDY/mawqi-tamwil.git](https://www.google.com/search?q=https://github.com/MohamedELHAMDY/mawqi-tamwil.git)  # Remplacez par l'URL de votre dépôt
    ```

2.  (Si vous développez localement) Naviguez jusqu'au répertoire du projet :

    ```bash
    cd mawqi-tamwil
    ```

3.  (Si vous développez localement) Vous pouvez configurer un serveur Web local (par exemple, en utilisant le module `http.server` de Python ou une solution plus avancée comme XAMPP ou MAMP) pour afficher la carte dans votre navigateur.

## Utilisation

1.  Ouvrez le fichier `index.html` dans votre navigateur Web. (Si vous utilisez GitHub Pages, le site sera en ligne à l'URL fournie).
2.  Explorez la carte, zoomez et dézoomez, et cliquez sur les marqueurs pour afficher les détails.
3.  Utilisez les options de recherche et de filtrage (lorsqu'elles seront implémentées) pour trouver des institutions spécifiques.
4.  Téléchargez les données à l'aide du bouton de téléchargement (lorsqu'il sera implémenté).

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à soumettre des demandes d'extraction, à ouvrir des problèmes ou à suggérer de nouvelles fonctionnalités. Consultez le fichier `CONTRIBUTING.md` (si vous en créez un) pour obtenir des instructions détaillées.

## Licence

MIT License

Copyright (c) 2025 Mohamed El Hamdy

La permission est accordée, à titre gratuit, à toute personne obtenant une copie
de ce logiciel et des fichiers de documentation associés (le "Logiciel"), de
traiter le Logiciel sans restriction, y compris, sans limitation, les droits
d'utiliser, de copier, de modifier, de fusionner, de publier, de distribuer, de
concéder en sous-licence et/ou de vendre des copies du Logiciel, et de
permettre aux personnes auxquelles le Logiciel est fourni de le faire, sous
les conditions suivantes :   

L'avis de droit d'auteur ci-dessus et cet avis de permission doivent être
inclus dans toutes les copies ou parties substantielles du Logiciel.

LE LOGICIEL EST FOURNI "TEL QUEL", SANS GARANTIE D'AUCUNE SORTE, EXPRESSE
OU IMPLICITE, Y COMPRIS, MAIS SANS S'Y LIMITER, LES GARANTIES DE
COMMERCIALISATION, D'ADÉQUATION À UN USAGE PARTICULIER ET DE
NON-CONTREFAÇON. EN AUCUN CAS, LES AUTEURS OU TITULAIRES DU DROIT
D'AUTEUR NE POURRONT ÊTRE TENUS RESPONSABLES DE TOUTE RÉCLAMATION,
DE TOUT DOMMAGE OU DE TOUTE AUTRE RESPONSABILITÉ, QUE CE SOIT DANS
LE CADRE D'UN CONTRAT, D'UN DÉLIT OU AUTRE, DÉCOULANT DU LOGICIEL,
DE SON UTILISATION OU D'AUTRES TRAITÉS DANS LE LOGICIEL.   


## Contact

*   Mohamed El Hamdy
*   [email address removed]
*   [linkedin.com/in/melhamdy](linkedin.com/in/melhamdy)
