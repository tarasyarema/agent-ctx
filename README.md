# Agent Context Engineering

Comparative analysis of different LLM agent architectures for data analysis tasks.

## Setup

**Requirements:** `uv` and `git-lfs`

```bash
git clone <repository>
cd agent-ctx
git lfs pull
uv sync
```

## Usage

### Run Agent Tests
```bash
uv run python main.py
```

Runs three agent types (simple-raw, simple-summarization, intent) against the configured model and saves results to `outputs/`.

### Generate Analysis
```bash
uv run python analyze_agents.py
```

Creates visualizations, CSVs, and a summary report in `analysis_output/`:
- **Visualizations**: PNG charts comparing performance metrics
- **CSVs**: Detailed and aggregated metrics
- **Report**: `summary_report.md` with comprehensive analysis

## Metrics

- **Success Rate**: Task completion percentage (empty metrics = failure)
- **Cost**: API costs per run and per step
- **Speed**: Total execution time
- **Step Count**: Number of agent iterations
- **Per-Step Latency**: Average time per agent step
- **Token Usage**: Input/output tokens consumed
- **Throughput**: Tokens processed per second
- **Accuracy**: Correctness vs. ground truth (5% tolerance for numeric fields)
- **Proximity Score**: 0-1 score showing how close predictions are to correct values

## Test Data

NYC Yellow Taxi trip data (Jan-Sep 2025) from [NYC.gov](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) in Parquet format.

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

For more information, please refer to <https://unlicense.org/>
