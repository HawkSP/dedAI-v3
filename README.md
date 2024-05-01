# DedAI v3: Emotion-Aware Music Curation Through EEG and AI

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Test Coverage](https://img.shields.io/badge/coverage-98%25-green) ![Code Quality](https://img.shields.io/badge/code%20quality-A-blue)

## An Interdisciplinary Synergy of Computational Neuroscience, Artificial Intelligence, and Musicology

---

### Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Scientific Justification](#scientific-justification)
4. [Technology Stack](#technology-stack)
5. [Collaboration with Emotiv](#collaboration-with-emotiv)
6. [Installation](#installation)
7. [Usage](#usage)
8. [API Reference](#api-reference)
9. [Performance Metrics](#performance-metrics)
10. [Case Studies](#case-studies)
11. [Development Roadmap](#development-roadmap)
12. [Interactive Tutorials](#interactive-tutorials)
13. [Contributing](#contributing)
14. [FAQ](#faq)
15. [License](#license)
16. [Acknowledgements](#acknowledgements)
17. [Citations](#citations)
18. [Contact & Social Media](#contact--social-media)

---

## Introduction

DedAI v3 is a pioneering venture that leverages computational neuroscience and machine learning techniques to curate personalized music playlists based on real-time emotion detection through EEG (Electroencephalography) data. This project embodies the confluence of neuroaesthetics, the theory of emotional intelligence in music, and state-of-the-art AI algorithms.

![Demo GIF](https://i.imgur.com/cHxW0nf.gif)

---

## Features

- **Real-Time Emotion Detection**: Utilizing EEG spectral power densities to classify emotional states. (Real-time is still in development)
- **AI-Driven Music Recommendation**: Employing Reinforcement Learning and NLP algorithms to recommend music that aligns with the user's emotional state.
- **User Clustering for Enhanced Personalization**: Utilizing unsupervised learning algorithms to cluster users based on their emotional and musical preferences.

![Model Architecture](https://imgur.com/AgqkgTe.png)

---

## Scientific Justification

This section elaborates on the scientific methodologies and algorithms deployed in DedAI v3:

### EEG Data Processing
- **Fast Fourier Transform (FFT)**
- **Wavelet Transform**

### Machine Learning Algorithms
- **Reinforcement Learning**
- **Natural Language Processing (NLP)**

For more details, please refer to our [Scientific Whitepaper](./Scientific_Whitepaper.md).

---

## Technology Stack

- **EEG Data Processing**: Python, FFT, Wavelet Transform
- **Machine Learning**: TensorFlow, Keras, Scikit-learn
- **Backend**: Javascript, Python
- **Frontend**: Electron and Node.js

---

## Collaboration with Emotiv

Developed in partnership with Emotiv, a global leader in neuroengineering, to integrate high-fidelity EEG hardware for unparalleled accuracy in emotion detection.

---

## Installation

```bash
pip install -r requirements.txt
```
## Usage

Please refer to our [User Guide](./User_Guide.md) and [API Documentation](./API_Docs.md).

## API Reference

For an extensive API reference, visit our [API Docs](./API_Docs.md).

## Performance Metrics

- **Emotion Detection Accuracy**: TBA
- **User Satisfaction Rate**: TBA

## Case Studies

- **Wellness Centers**: Improved patient mental health by TBA
- **Educational Institutions**: Enhanced student focus by TBA


## Contributing

We welcome contributions! Please read our [Contributing Guidelines](./CONTRIBUTING.md) for more information.

## FAQ

- **Is DedAI v3 available for commercial use?**
  - At this stage, DedAI v3 is under active development and is not available for commercial use. We operate under a restricted license that protects the intellectual property while allowing for community contributions via feature suggestions. For more details, please consult our [License](./LICENSE.md).

- **What types of EEG devices are compatible with DedAI v3?**
  - DedAI v3 is developed in partnership with Emotiv, so Emotiv's EEG devices are fully supported. We aim to extend compatibility to other EEG hardware in the future.

- **How does DedAI v3 ensure data privacy?**
  - All EEG data is anonymized and encrypted to ensure user privacy. For more details, refer to our [Privacy Policy](./Privacy_Policy.md).

- **Can DedAI v3 integrate with other music streaming platforms?**
  - Integration with other music streaming platforms is part of our future development roadmap.

- **What machine learning algorithms does DedAI v3 use for emotion detection and music generation?**
  - We leverage a blend of Convolutional Neural Networks (CNNs), Recurrent Neural Networks (RNNs) and Physics Informed Neural Networks (PINNs) for music generation and Linear Regression and Support Vector Machines (SVMs) for emotion detection. Detailed information can be found in our [Technical Documentation](./Tech_Docs.md).

- **How accurate is the emotion detection?**
  - We are in the process of rigorously validating our emotion detection algorithms, and thus, a definitive accuracy figure is not available at this time.

- **Is real-time mood tracking available?**
  - Real-time mood tracking is currently under development and will be introduced in a future release.

- **How can I contribute to DedAI v3?**
  - We encourage community involvement and contributions. Please consult our [Contributing Guidelines](./CONTRIBUTING.md) for more details on how you can participate.

- **What programming languages and frameworks are used in DedAI v3?**
  - DedAI v3 is primarily developed using Python, TensorFlow, and Flask. The frontend is built with Flutter.

- **Are there any academic publications related to DedAI v3?**
  - We are in discussions with research institutions for potential collaborations and academic publications.

- **Is there an API I can use to integrate DedAI v3 into my own projects?**
  - A comprehensive API is available for developers who wish to integrate DedAI v3 functionalities into their own projects. Refer to our [API Documentation](./API_Docs.md) for more details.



## License

This project operates under the DedAI v3 Restricted License Agreement. See [LICENSE.md](./LICENSE.md) for details.

## Acknowledgements

Special thanks to the computational neuroscience community and Emotiv for their invaluable insights and collaboration. We also acknowledge the foundational algorithms and seminal papers that contribute to this project.

Also would like to credit gcui-art for the work on the Suno API [https://github.com/gcui-art/suno-api](./https://github.com/gcui-art/suno-api)

## Citations

For scholarly use, please cite this repository using the following Bibtex entry:

```bibtex
@misc{DedAI2023,
  author = {Elliott Mitchell},
  title = {DedAI v3: Emotion-Aware Music Curation Through EEG and AI},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\\url{https://github.com/HawkSP/DedAI}}
}
