# Traffic Lights Optimization

![Contributors](https://img.shields.io/github/contributors/lifalb/Traffic-Lights-Optimization)
![Last Commit](https://img.shields.io/github/last-commit/lifalb/Traffic-Lights-Optimization)

> This project is addressed to a challenge of optimizing traffic flow with the use of artificial intelligence. Two reinforcement learning (RL) methods that are made to increase the throughput at intersections and reduce the travel time of vehicles are compared in our project; using metrics such as average waiting time and fuel consumption.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [File Structure](#file-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## About

In modern cities, one of the major issues is traffic congestion. This problem is the reason of increased travel times, air pollution, and fuel consumption. Traditional traffic light control methods rely on fixed timing schedules, and, as a result, fail to adapt to current traffic state. Hence, the task of implementing AI methods to this problem is critical.
In this project we compare two RL-based methods. The first approach, made by Vidali et al. ([Deep Q-Learning Agent for Traffic Signal Control](https://github.com/AndreaVidali/Deep-QLearning-Agent-for-Traffic-Signal-Control)) , uses a Deep Reinforcement Learning (DRL) aiming to select optimal traffic light phases based on the number of vehicles in each lane. In the second approach, presented by Lucas N. Alegre et al. ([sumo-rl](https://github.com/LucasAlegre/sumo-rl)) is used to minimize delays, observing real-time traffic data.


## Features

- Generate train and test datasets containing customizable scenarios
- Train previous model on the generated dataset
- Test the trained models and provide comparisons


---
## File Structure

Here’s an overview of the file structure in this project:

```plaintext
Traffic-Lights-Optimization/
│
├── Generate route files/                # Generating datasets directory
│   ├── generate_test.py                 # Generating test set script
│   └── generate_train.py                # Generating training set script
│
├── Models/                              # Contains the testing and training code for the three approaches
│   ├── Andrea/                          # Contains testing and training code Vidali et al. approach
│   ├── BasicTLS/                        # Contains testing and training for the basic Traffic Light system
│   └── Sumo-rl/                         # Contains testing and training code Lucas N. Alegre et al. approach
├── outputs - ablation/                  # Outputs of the ablation study
├── outputs - test/                      # Outputs of the tests
├── outputs - train/                     # Outputs of the training
├── plots/                               # Contains the plots generated from the outputs
├── tests/                               # Contains the route files of the testing dataset
├── training_network/                    # Contains the files that describe the network used
├── visualize_ablation.ipynb             # Notebook to visualize ablation study outputs
├── visualize_test.ipynb                 # Notebook to visualize tests outputs
└── visualize_train.ipynb                # Notebook to visualize training outputs
```

## Getting Started

### Prerequisites

- **Python**: Version 3.8 or higher
- **SUMO**: [Installation Guide](https://sumo.dlr.de/docs/Installing/index.html)
  - Follow the official guide to install SUMO on your operating system.

### Installation

Step-by-step guide on how to set up the project locally:

```bash
# Clone the repository
git clone https://github.com/lifalb/Traffic-Lights-Optimization.git

# Navigate to the project directory
cd Traffic-Lights-Optimization

# Install dependencies
pip install -r requirements.txt

```

### Credits

This project uses code from the following repositories:

- [sumo-rl](https://github.com/LucasAlegre/sumo-rl)  

- [Deep Q-Learning Agent for Traffic Signal Control](https://github.com/AndreaVidali/Deep-QLearning-Agent-for-Traffic-Signal-Control)  
  
 Changes were made to unify the output of the models, number of steps per and number of episodes.
