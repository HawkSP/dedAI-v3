# Mini-Proposal for Final Major Project and Research Project

![Status](https://img.shields.io/badge/Status-Complete-green)
![Contributors](https://img.shields.io/badge/Contributors-1-blue)
![Last Updated](https://img.shields.io/badge/Last%20Updated-October%2011,%202023-yellowgreen)

> **Submitted to:** Hussain  
> **Submitted by:** Elliott Mitchell  
> **Date:** October 11, 2023

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Introduction](#introduction)
3. [Final Major Project (FMP)](#final-major-project-fmp)
    - [Objectives for FMP](#objectives-for-fmp)
    - [Methodology for FMP](#methodology-for-fmp)
    - [Deliverables for FMP](#deliverables-for-fmp)
4. [Research Project](#research-project)
    - [Objectives for Research](#objectives-for-research)
    - [Methodology for Research](#methodology-for-research)
    - [Deliverables for Research](#deliverables-for-research)
5. [Delineation Between FMP and Research Project](#delineation-between-fmp-and-research-project)
6. [Conclusion](#conclusion)
7. [Acknowledgments](#acknowledgments)


---

## Executive Summary
>This mini-proposal clarifies the distinct yet interrelated scope of two academic pursuits: the **Final Major Project (FMP)**, focusing on the commercial and technical facets of **DedAI**, and a separate **Research Project** aimed at investigating the neuro-aesthetic response to musical elements. Both projects pivot on computational neuroscience, machine learning, and musical neuroaesthetics.

---

## Introduction
Both the FMP and Research Project employ interdisciplinary strategies to explore the complex relationships between music, emotional states, and neurophysiological responses. This proposal outlines the specific **objectives**, **methodologies**, and **deliverables** for each endeavor.

---

## Final Major Project (FMP)
### Objectives for FMP
- To bring DedAI to market readiness, incorporating real-time emotion-state transition algorithms, AI-enabled music curation, and user interaction platforms.

### Methodology for FMP
- Utilize **Hidden Markov Models** to implement dynamic, real-time emotion-state transition models based on continuous EEG data.
- Develop an application with user-friendly interfaces for training both music and EEG data.
- Employ contemporary marketing strategies for brand development and user engagement.

### Deliverables for FMP
- WAV files of AI-orchestrated music that map to specific emotional states.
- A fully functional application designed for user interaction in training both music and EEG data.
- Marketing collateral, including a website for DedAI.
- A detailed methodology document outlining the entire development process.
- A GitHub repository containing all the source code, complete with extensive documentation.

<details>
  <summary>Code Repository Features</summary>
  
  - Well-commented source code
  - README for project overview
  - Contribution guidelines
  - Code of conduct and licensing information
</details>


<details>
  <summary>Technical Details</summary>
  
  ```python
  # Pseudo-code for Hidden Markov Model
  from hmmlearn import hmm
  model = hmm.GaussianHMM(n_components=3)
  model.fit(X)
```
</details>

## Research Project

### Objectives for Research
- To study the neurophysiological effects of different musical attributes.
- To publish the findings in a scholarly format.

### Methodology for Research
- Conduct an experimental study using the Emotiv EEG headset to capture brainwave data while participants listen to different types of music.
- Ensure ethical compliance and participant anonymity throughout the study.

<details>
  <summary>Technical Methodology</summary>
  
  ```python
  # Pseudo-code for EEG Data Analysis
  import mne
  raw = mne.io.read_raw_fif("your_file_here.fif")
  raw.filter(l_freq=1, h_freq=40)
```
</details>

### Deliverables for Research
- An experimental study that adheres to ethical standards and ensures participant anonymity.
- A 4000-word thesis detailing the methodology, results, and findings of the experiment.

<details>
  <summary>Ethical Compliance</summary>
  
  - Comprehensive ethical review protocols
  - Informed consent forms
  - Data anonymization techniques

</details>

---

## Delineation Between FMP and Research Project
While the FMP aims at the practical commercialization of DedAI, the Research Project is an academic endeavour that provides the scientific foundation upon which DedAI's machine-learning algorithms can be further refined and validated.

---

## Conclusion
This mini-proposal serves as an exhaustive guide for both projects, emphasizing their unique objectives, methodological approaches, and deliverables. Both contribute significantly to the fields of computational neuroscience, artificial intelligence, and musical neuroaesthetics.

---

## Acknowledgments
I extend my sincere gratitude to Hussain for his invaluable guidance and mentorship, which have been instrumental in shaping the practical feasibility of these projects.

> **Best regards,  
> Elliott Mitchell**

> elliott@iamdedeye.com


