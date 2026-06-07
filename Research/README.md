# Zhe Wee (Derrick) Ng's Research

Selected research projects applying machine learning to engineering decision-making under incomplete, noisy, or unstructured data. Across e-waste supply-chain optimization, sustainable product-design analysis, and wildfire-response forecasting, the shared theme is translating real-world signals into interpretable models, datasets, and design or operations guidance.

## Research Projects

### 1. Machine Learning-Aided Supply Chain Analysis of Waste Management Systems

- **Role:** Lead researcher; first and corresponding author
- **Affiliation:** [Department of Electrical Engineering and Computer Sciences, UC Berkeley](https://eecs.berkeley.edu/)
- **Period:** April 2024 - October 2025
- **Focus:** Modeled an Indian e-waste supply-chain network as a sustainability and resilience problem, with attention to environmental, economic, and social variables, sparse industrial data, stochastic perturbations, and nonlinear arbitrage behavior.
- **Approach:** Combined Monte Carlo simulation for sparse-data perturbation with feedforward neural networks for arbitrage prediction and random forests for feature influence, sensitivity analysis, and dimensional reduction across supply-chain variables.
- **Contributions:** Published in *Sustainability*, 17(19), Article 8848, 2025. The study reported predictive performance above R2 = 0.97 across 21 variables, showed that FNN models better predicted arbitrage conditions while RF models supported interpretability, and produced a data-driven toolkit for sustainable e-waste supply-chain analysis.
- **Link:** [Publisher page](https://www.mdpi.com/2071-1050/17/19/8848)

### 2. Data-Driven Sustainable Design Opportunities from Automated User Insights

- **Role:** Research assistant; co-author
- **Affiliation:** [Co-Design Lab](https://codesign.berkeley.edu/team/derrick-ng/), [Berkeley Engineering Design Scholar Program](https://jacobsinstitute.berkeley.edu/berkeley-engineering-design-scholar-program/past-cohorts/), [Jacobs Institute for Design Innovation](https://jacobsinstitute.berkeley.edu/), and [UC Berkeley Mechanical Engineering](https://me.berkeley.edu/)
- **Period:** June 2024 - May 2025
- **Focus:** Studied how large-scale customer reviews can reveal sustainable-design opportunities that are grounded in user experience rather than only technical environmental claims.
- **Approach:** Built a review-to-design-insight workflow for Amazon Climate Pledge Friendly products, combining automated scraping, product/category normalization, certification mapping, GPT-assisted feature and affordance extraction, 16-dimension sustainability ABSA, topic modeling, certification and category analysis, and LLM-assisted design-lead synthesis.
- **Contributions:** Created the research database used in the ASME IDETC-CIE 2025 paper, covering more than 23,000 reviews across 290 products. The analysis connected sustainability certifications, product metadata, user sentiment, product affordances, and review evidence to surface certification-perception gaps, category-level redesign themes, and product-specific design leads for a printer, laptop, and USB-C to HDMI cable.
- **Links:** [Conference paper](https://codesign.berkeley.edu/papers/goridkov-reviews-idetc/) | [GitHub repository](https://github.com/NGZheWee/CoDesignLab-SustainableDesign-NLP)

### 3. Multimodal Wildfire Forecasting for Robotic Response Systems

- **Role:** Research assistant
- **Affiliation:** [BEST Lab, UC Berkeley](https://best.berkeley.edu/) in collaboration with [Squishy Robotics](https://best.berkeley.edu/squishy-robotics/)
- **Period:** January 2025 - May 2025
- **Focus:** Explored whether RGB imagery, near-infrared imagery, segmentation masks, and textual descriptors can jointly support interpretable forecasts of fire area, fire intensity, superposition, and spread direction for robotic situational awareness.
- **Approach:** Conducted exploratory analysis of the [Corsican Fire Database](https://pro.universita.corsica/article.php?id_art=2133&id_rub=572), including image/metadata cleaning, RGB-NIR pairing, mask-derived fire metrics, descriptor construction, Gemini-assisted annotation experiments, EfficientNet image embeddings, BERT descriptor embeddings, late-fusion transformer modules, and LSTM temporal forecasting prototypes.
- **Contributions:** Produced research notebooks and prototype forecasting workflows for multimodal wildfire data, including dataset diagnostics, feature-extraction utilities, late-fusion model experiments, tolerance-based evaluation, qualitative review artifacts, and presentation materials for a wildfire-response robotics research workflow.
- **Link:** [GitHub repository](https://github.com/NGZheWee/SquishyRobotics-Wildfire-Forecasting)
