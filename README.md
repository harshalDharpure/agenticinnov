# Agentic Memory Management Simulator

Research-grade Python project that simulates a smartphone memory management system controlled by a multi-agent AI. The simulator compares LRU, FIFO, and an agentic policy that predicts next app usage and proactively manages memory.

## Features
- Modular architecture (agents, models, simulator, baselines, experiments, utils)
- Context-aware Markov predictor for next-app usage
- Multi-agent planning, allocation, eviction, and cache tracking
- Metrics: average load time, cache hit rate, memory usage, thrashing
- Experiment pipeline with CSV output and visualization

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Experiments
```bash
python main.py
```

Outputs are stored in the `results/` directory:
- `experiment_results.csv`
- `load_time_vs_method.png`
- `cache_hit_rate_vs_method.png`
- `memory_usage_vs_method.png`

## Configuration
Edit `config.py` to adjust memory size, app catalog, sequence length, random seed, and prediction parameters.
