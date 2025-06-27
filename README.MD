# Monumental Robot Crane

Author: Kees Loeff

## Overview

Simulating a robot crane.

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
   
4. **Activate virtual environment**
   ```bash
   source .venv/bin/activate
   
5. **Install requirements**
   ```bash
   pip3 install -r requirements.txt
   ```
   
## Running

Follow these steps to run the application locally:

1. **Run app using uvicorn** 
    ```bash
   uvicorn backend.main:app --reload --port 8080
   ```
The application will run on http://localhost:8080/
