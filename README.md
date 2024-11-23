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
In this project we compare two RL-based methods. The first approach, made by Vidali et al. ()[Deep Q-Learning Agent for Traffic Signal Control](https://github.com/AndreaVidali/Deep-QLearning-Agent-for-Traffic-Signal-Control)) , uses a Deep Reinforcement Learning (DRL) aiming to select optimal traffic light phases based on the number of vehicles in each lane. In the second approach, presented by Lucas N. Alegre et al. ([sumo-rl](https://github.com/LucasAlegre/sumo-rl)) is used to minimize delays, observing real-time traffic data.


## Features

- Generate train and test datasets containing customizable scenarios
- Train previous model on the generated dataset
- Test the trained models and provide comparisons


---
## File Structure

Here’s an overview of the file structure in this project:

```plaintext
projectname/
│
├── src/                # Source code directory
│   ├── main.py         # Main application entry point
│   ├── utils.py        # Utility functions used across the project
│   └── config.py       # Configuration settings
│
├── data/               # Data files
│   ├── input/          # Input datasets
│   └── output/         # Generated output files
│
├── tests/              # Unit and integration tests
│   └── test_main.py    # Tests for main application
│
├── LICENSE             # License file
├── README.md           # Project documentation
├── requirements.txt    # Dependencies for the project
└── .gitignore          # Git ignored files and directories
```

## Getting Started

### Prerequisites

List the tools or dependencies needed to run your project:
- [Software/Library Name](link) (e.g., Node.js, Python)

### Installation

Step-by-step guide on how to set up the project locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/projectname.git

# Navigate to the project directory
cd projectname

# Install dependencies
npm install

# Start the application
npm start
```

### Credits

This project uses code from the following repositories:

- [sumo-rl](https://github.com/LucasAlegre/sumo-rl)  

- [Deep Q-Learning Agent for Traffic Signal Control](https://github.com/AndreaVidali/Deep-QLearning-Agent-for-Traffic-Signal-Control)  
  
 Changes were made to unify the output of the models, number of steps per and number of episodes.
