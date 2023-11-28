# BTCTransactionsPlotter

## Overview
The tool retrieves all the transactions linked to a Bitcoin address and allows the user to visualize them with a graph and a table view. It is also possible to view the balance history of the account with a graph in the dedicated section. 

## Features

- **Network Visualization:** displays all the addresses who have sent or received cryptocurrency to/from the selected address;
- **Table Visualization:** lists all the transactions in table format;
- **Total Balance Graph:**: plots the total balance in a graph in function of time. 

## Prerequisites
The tool utilizes Python and a series of libraries for functioning. Requirements:
- Python 3.x
- PyQt5
- NetworkX
- Pandas
- MatPlotLib
- NumPy

## Installation
1. Clone the repository:
    ```bash 
    git clone https://github.com/theFlyF0x/BTCTransactionsPlotter.git
    cd BTCTransactionsPlotter
    ```
2. Install requirements
   TODO make a requirements.txt

## Running
The tools can be run with Python, or it can be compiled into an executable. 
1. Running with Python
    ```bash
    python main.py
    ```
2. Compiling into an executable
    TODO