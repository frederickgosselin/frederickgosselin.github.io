---
title: "Mise en forme par grenaillage de panneaux d’aile d’avion via l’I.A."
date: 2020-08-20
wpId: 479
categories: ["Publications.fr"]
translation: "2020-08-20-peen-forming-aircraft-wing-panels-with-artificial-intelligence"
---

![](/uploads/2020/08/MACH-3-DSC_0298-prcsd-resized-800x485-1.jpg)

Mise en forme manuelle d’un panneau d’aile d’avion par grenaillage. Credit Skiesmag. [https://www.skiesmag.com/news/aero-montreal-help-smes-bridge-digital-divide/](https://www.skiesmag.com/news/aero-montreal-help-smes-bridge-digital-divide/)

Comment est-ce qu’un opérateur doit grenailler une tôle d’aluminium le former en panneau d’aile d’avion? Wassime Siguerdidjane, étudiant PhD supervisé par Farbod Khameneifar, a entraîné un réseau de neurones avec des simulations éléments finis pour trouver!

Wassime a développé un générateur de trajectoires de grenaillage aléatoires mais réalistes. Ces 60 000 modèles ont été résolus par la méthode des éléments finis, formant des ensembles de données d’apprentissage, de validation et de test. La clé pour résoudre ces 60 000 cas par éléments finis est de les traiter comme des problèmes de bi-couches. L’effet du grenaillage sur le panneau d’aluminium est d’en étirer localement la couche supérieure, et ainsi d’induire une courbure du panneau.

![](/uploads/2020/08/bilayer.png)

Modèle bi-couches: (a) une plaque plane de métal; (b) est impactée par des grenailles, qui; (c) induisent localement une expansion de la couche de surface; (d) donnant lieur à la courbure du panneau.

Une fois entraîné de cette manière, le réseau de neurones peut prédire avec précision le motif de grenaillage qui conduira à la forme 3D souhaitée pour le panneau. Cela fonctionne même pour les cas très géométriquement non linéaires où la plaque est fortement courbée.

[](https://pbs.twimg.com/media/EfzfMe-XoAAqWVu.jpg)Apprenez-en plus sur Manufacturing Letters:  
[doi.org/10.1016/j.mfgl…](https://doi.org/10.1016/j.mfglet.2020.08.001)  
Preprint disponible ici:  
[arxiv.org/abs/2008.08049](https://arxiv.org/abs/2008.08049)  
Avec le financement du [@FRQ\_NT](https://twitter.com/FRQ_NT) et d’[Aerosphère Inc.](http://www.aerosphere.ca/)
