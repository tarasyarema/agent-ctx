# Agent Performance Analysis Report

> Comprehensive comparison of different agent architectures for data analysis tasks

## Table of Contents

- [Overview](#overview)
- [Success Rate](#success-rate)
- [Performance Metrics](#performance-metrics)
- [Detailed Analysis](#detailed-analysis)
- [Key Insights](#key-insights)
- [Recommendations](#recommendations)

---

## Overview

**Total Runs Analyzed:** 15  
**Agent Types:** 3  
**Date:** 2025-11-07

**Models Tested:** `openai-gpt-4.1-mini`, `anthropic-claude-sonnet-4.5`

### Quick Stats

| Agent Type | Model | Runs | Success Rate | Avg Cost | Avg Time | Avg Steps |
|------------|-------|------|--------------|----------|----------|----------|
| `intent` | `claude-sonnet-4.5` | 3 | 100.0% | $0.35 | 200.2s | 16.3 |
| `intent` | `gpt-4.1-mini` | 2 | 100.0% | $0.05 | 128.6s | 14.5 |
| `simple-raw` | `claude-sonnet-4.5` | 3 | 100.0% | $0.69 | 109.0s | 43.3 |
| `simple-raw` | `gpt-4.1-mini` | 2 | 50.0% | $0.09 | 91.5s | 87.5 |
| `simple-summarization` | `claude-sonnet-4.5` | 3 | 33.3% | $0.64 | 233.3s | 50.0 |
| `simple-summarization` | `gpt-4.1-mini` | 2 | 50.0% | $0.05 | 123.5s | 65.5 |

---

## Success Rate

![Success Rate](success_rate.png)

- **`intent`** (claude-sonnet-4.5): 3/3 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (gpt-4.1-mini): 2/2 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (claude-sonnet-4.5): 3/3 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (gpt-4.1-mini): 1/2 successful (50.0%) ![50%](https://img.shields.io/badge/success-50%25-yellow)
- **`simple-summarization`** (claude-sonnet-4.5): 1/3 successful (33.3%) ![33%](https://img.shields.io/badge/success-33%25-red)
- **`simple-summarization`** (gpt-4.1-mini): 1/2 successful (50.0%) ![50%](https://img.shields.io/badge/success-50%25-yellow)

---

## Performance Metrics

### Cost Comparison

![Cost Comparison](cost_comparison.png)

| Agent Type | Model | Average Cost | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | $0.35 | ±$0.05 |
| `intent` | `gpt-4.1-mini` | $0.05 | ±$0.01 |
| `simple-raw` | `claude-sonnet-4.5` | $0.69 | ±$0.24 |
| `simple-raw` | `gpt-4.1-mini` | $0.10 | ±$nan |
| `simple-summarization` | `claude-sonnet-4.5` | $0.66 | ±$nan |
| `simple-summarization` | `gpt-4.1-mini` | $0.05 | ±$nan |

### Execution Time

![Execution Time](execution_time.png)

| Agent Type | Model | Average Time | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | 200.2s | ±26.7s |
| `intent` | `gpt-4.1-mini` | 128.6s | ±6.2s |
| `simple-raw` | `claude-sonnet-4.5` | 109.0s | ±6.4s |
| `simple-raw` | `gpt-4.1-mini` | 91.5s | ±28.0s |
| `simple-summarization` | `claude-sonnet-4.5` | 233.3s | ±14.2s |
| `simple-summarization` | `gpt-4.1-mini` | 123.5s | ±39.6s |

### Step Count

![Step Count](step_count.png)

| Agent Type | Model | Average Steps | Std Dev |
|------------|-------|---------------|----------|
| `intent` | `claude-sonnet-4.5` | 16.3 | ±0.6 |
| `intent` | `gpt-4.1-mini` | 14.5 | ±4.9 |
| `simple-raw` | `claude-sonnet-4.5` | 43.3 | ±3.1 |
| `simple-raw` | `gpt-4.1-mini` | 87.5 | ±19.1 |
| `simple-summarization` | `claude-sonnet-4.5` | 50.0 | ±0.0 |
| `simple-summarization` | `gpt-4.1-mini` | 65.5 | ±4.9 |

### Token Usage

![Token Usage](token_usage.png)

| Agent Type | Model | Input Tokens | Output Tokens | Total Tokens |
|------------|-------|--------------|---------------|-------------|
| `intent` | `claude-sonnet-4.5` | 153637 | 9895 | 163532 |
| `intent` | `gpt-4.1-mini` | 66312 | 7764 | 74075 |
| `simple-raw` | `claude-sonnet-4.5` | 206549 | 4890 | 211439 |
| `simple-raw` | `gpt-4.1-mini` | 211686 | 3636 | 215322 |
| `simple-summarization` | `claude-sonnet-4.5` | 183831 | 6229 | 190060 |
| `simple-summarization` | `gpt-4.1-mini` | 106056 | 4188 | 110245 |

### Tokens vs Steps Relationship

![Tokens vs Steps](tokens_vs_steps.png)

### Accuracy Score

![Accuracy Score](accuracy_score.png)

| Agent Type | Model | Average Accuracy | Std Dev |
|------------|-------|------------------|----------|
| `intent` | `claude-sonnet-4.5` | 66.67% | ±16.67% |
| `intent` | `gpt-4.1-mini` | 91.67% | ±11.79% |
| `simple-raw` | `claude-sonnet-4.5` | 88.89% | ±9.62% |
| `simple-raw` | `gpt-4.1-mini` | 33.33% | ±nan% |
| `simple-summarization` | `claude-sonnet-4.5` | 83.33% | ±nan% |
| `simple-summarization` | `gpt-4.1-mini` | 33.33% | ±nan% |

### Field-Level Accuracy Analysis

#### Field Accuracy Heatmap

![Field Accuracy Heatmap](field_accuracy_heatmap.png)

#### Proximity Score Heatmap

![Field Proximity Heatmap](field_proximity_heatmap.png)

#### Field Accuracy Rates

| Field | intent
(claude-sonnet-4.5) | intent
(gpt-4.1-mini) | simple-raw
(claude-sonnet-4.5) | simple-raw
(gpt-4.1-mini) | simple-summarization
(claude-sonnet-4.5) | simple-summarization
(gpt-4.1-mini) |
|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 0% | 100% | 33% | 0% | 0% | 0% |
| `best_revenue_hour` | 67% | 100% | 100% | 0% | 100% | 100% |
| `best_revenue_zone` | 67% | 100% | 100% | 100% | 100% | 100% |
| `optimal_distance_bracket` | 100% | 50% | 100% | 100% | 100% | 0% |
| `trips_above_max_distance` | 100% | 100% | 100% | 0% | 100% | 0% |
| `trips_below_min_fare` | 67% | 100% | 100% | 0% | 100% | 0% |

#### Percentage Error (Numeric Fields)

![Percentage Error](field_percentage_error.png)

| Field | intent
(claude-sonnet-4.5) | intent
(gpt-4.1-mini) | simple-raw
(claude-sonnet-4.5) | simple-raw
(gpt-4.1-mini) | simple-summarization
(claude-sonnet-4.5) | simple-summarization
(gpt-4.1-mini) |
|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 42.4% | 0.0% | 29.2% | 8.0% | 43.7% | 36.1% |
| `best_revenue_hour` | 2.0% | 0.0% | 0.0% | 5.9% | 0.0% | 0.0% |
| `trips_above_max_distance` | 0.0% | 0.0% | 0.0% | 92.7% | 0.0% | 92.7% |
| `trips_below_min_fare` | 18.4% | 0.0% | 0.0% | 93.2% | 0.0% | 93.2% |

---

## Detailed Analysis

### `intent` (openai-gpt-4.1-mini)

![Runs](https://img.shields.io/badge/runs-5-blue) ![Success](https://img.shields.io/badge/success-5-green) 

**Performance (Successful Runs Only):**

- **Average Steps:** 15.6
- **Average Cost:** $0.23
- **Average Time:** 171.6s
- **Average Tokens:** 127749
- **Tokens per Step:** 8117
- **Cost per Step:** $0.0140
- **Time per Step:** 11.07s
- **Average Accuracy:** 76.67%

### `simple-raw` (openai-gpt-4.1-mini)

![Runs](https://img.shields.io/badge/runs-5-blue) ![Success](https://img.shields.io/badge/success-4-green) ![Failed](https://img.shields.io/badge/failed-1-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 51.0
- **Average Cost:** $0.54
- **Average Time:** 109.6s
- **Average Tokens:** 216390
- **Tokens per Step:** 4445
- **Cost per Step:** $0.0123
- **Time per Step:** 2.27s
- **Average Accuracy:** 75.00%

**Note:** This agent had failed runs. Check detailed metrics for more information.

### `simple-summarization` (openai-gpt-4.1-mini)

![Runs](https://img.shields.io/badge/runs-5-blue) ![Success](https://img.shields.io/badge/success-2-green) ![Failed](https://img.shields.io/badge/failed-3-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 56.0
- **Average Cost:** $0.35
- **Average Time:** 200.5s
- **Average Tokens:** 150292
- **Tokens per Step:** 2795
- **Cost per Step:** $0.0070
- **Time per Step:** 3.72s
- **Average Accuracy:** 58.33%

**Note:** This agent had failed runs. Check detailed metrics for more information.

---

## Key Insights

### Rankings

#### Success Rate

🥇 **`intent`**: 100.0%
🥈 **`simple-raw`**: 80.0%
🥉 **`simple-summarization`**: 40.0%

#### Cost Efficiency (Lower is Better)

🥇 **`intent`**: $0.23
🥈 **`simple-summarization`**: $0.35
🥉 **`simple-raw`**: $0.54

#### Speed (Lower is Better)

🥇 **`simple-raw`**: 109.6s
🥈 **`intent`**: 171.6s
🥉 **`simple-summarization`**: 200.5s

#### Accuracy (Higher is Better)

🥇 **`intent`**: 76.67%
🥈 **`simple-raw`**: 75.00%
🥉 **`simple-summarization`**: 58.33%

---

## Recommendations

### Best Agent for Different Use Cases

- **💰 Most Cost-Efficient:** `intent` ($0.23 per run)
- **⚡ Fastest:** `simple-raw` (109.6s per run)
- **🎯 Most Accurate:** `intent` (76.67% accuracy)
- **✅ Most Reliable:** `intent` (100.0% success rate)

### Overall Assessment

Based on the analysis:

The data suggests different agents excel in different areas. Choose based on your priorities:

- If **budget is critical**, prioritize the most cost-efficient agent
- If **speed is essential**, choose the fastest agent
- If **accuracy matters most**, select the most accurate agent
- If **reliability is key**, go with the highest success rate

---

*Report generated on 2025-11-07 02:06:46*
