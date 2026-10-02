---
title: "Peen forming aircraft wing panels with Artificial Intelligence"
date: 2020-08-20
wpId: 474
tags: ["ai","neural networks","peen forming","shot peening","slender structure mechanics"]
categories: ["Publication"]
translation: "2020-08-20-mise-en-forme-par-grenaillage-de-panneaux-d-aile-d-avion-via-l-i-a"
---

![](/uploads/2020/08/MACH-3-DSC_0298-prcsd-resized-800x485-1.jpg)

Manual peen forming of an aircraft wing skin. Credit Skiesmag. [https://www.skiesmag.com/news/aero-montreal-help-smes-bridge-digital-divide/](https://www.skiesmag.com/news/aero-montreal-help-smes-bridge-digital-divide/)

Where should the operator shot peen a flat aluminium panel to form an aircraft wing skin?  
Wassime Siguerdidjane, PhD student supervised by Farbod Khameneifar, trained a neural network with FEM to do this!

This is akin to asking “How should the panel deform to adopt the wanted shape?” This is the inverse problem! Wassime’s insight was to formulate it as a pattern recognition problem, for which Neural Networks are highly capable! 

Wassime coded a *maze generator* and its *path finding algorithm*. These path solution where then turned into random, yet realistic peening patterns. These 60,000 patterns were then solved by the Finite Element Method, forming training, validation and test data sets.[](https://pbs.twimg.com/media/EfzdZ8MXoAAuJGG.png)The key in solving these 60,000 peen forming cases by the finite element method was to treat the problem as a bilayer one. The effect of shot peening on the aluminium panel is to locally expand the surface layer, hence inducing curvature.

![](/uploads/2020/08/bilayer.png)

Bilayer model: (a) a flat metal plate; (b) is impacted by shot, which; (c) locally expand the surface layer; (d) giving rise to curvatures.

Once trained this way, the neural network can accurately predict the peening pattern which will lead to the wanted 3D shape for the panel. It works even for highly geometrically nonlinear cases where the plate is highly curved.

[](https://pbs.twimg.com/media/EfzfMe-XoAAqWVu.jpg)Read more in Manufacturing Letters:  
[doi.org/10.1016/j.mfgl…](https://doi.org/10.1016/j.mfglet.2020.08.001)  
Preprint available here:  
[arxiv.org/abs/2008.08049](https://arxiv.org/abs/2008.08049)  
Thanks to [@FRQ\_NT](https://twitter.com/FRQ_NT) and [Aerosphère Inc.](http://www.aerosphere.ca/) for funding.
