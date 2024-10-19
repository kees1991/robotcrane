# Monumental Robot Crane

Author: Kees Loeff

## Overview

Simulating a robot crane, see [take home assignment](https://terraformco.notion.site/Visualizing-a-Robotic-Crane-Controls-3134774001644de2afaf41e82e01654b).

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (optional but recommended)

## Installation

Follow these steps to set up the application:

1. **Clone the repository**:
   ```bash
   git clone git@github.com:kees1991/robotcrane.git
   
2. **Move to repo directory**:
    ```bash
   cd robotcrane 
   
3. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   
4. **Install requirements**
   ```bash
   pip3 install -r requirements.txt
   ```
   
## Running

1. **Run app using uvicorn** 
    ```bash
   uvicorn backend.main:app --reload --port 8080
   ```
The application will run on http://localhost:8080/