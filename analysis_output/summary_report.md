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

**Total Runs Analyzed:** 18  
**Agent Types:** 3  
**Date:** 2025-11-07

**Models Tested:** `openai-gpt-4.1-mini`, `google-gemini-2.5-pro`, `anthropic-claude-sonnet-4.5`

### Quick Stats

| Agent Type | Model | Runs | Success Rate | Avg Cost | Avg Time | Avg Steps |
|------------|-------|------|--------------|----------|----------|----------|
| `intent` | `claude-sonnet-4.5` | 3 | 100.0% | $0.35 | 200.2s | 16.3 |
| `intent` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.15 | 196.7s | 18.0 |
| `intent` | `gpt-4.1-mini` | 2 | 100.0% | $0.05 | 128.6s | 14.5 |
| `simple-raw` | `claude-sonnet-4.5` | 3 | 100.0% | $0.69 | 109.0s | 43.3 |
| `simple-raw` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.12 | 111.9s | 20.0 |
| `simple-raw` | `gpt-4.1-mini` | 2 | 50.0% | $0.09 | 91.5s | 87.5 |
| `simple-summarization` | `claude-sonnet-4.5` | 3 | 33.3% | $0.64 | 233.3s | 50.0 |
| `simple-summarization` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.16 | 123.4s | 24.0 |
| `simple-summarization` | `gpt-4.1-mini` | 2 | 50.0% | $0.05 | 123.5s | 65.5 |

---

## Success Rate

![Success Rate](success_rate.png)

- **`intent`** (claude-sonnet-4.5): 3/3 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (gpt-4.1-mini): 2/2 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (claude-sonnet-4.5): 3/3 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (gpt-4.1-mini): 1/2 successful (50.0%) ![50%](https://img.shields.io/badge/success-50%25-yellow)
- **`simple-summarization`** (claude-sonnet-4.5): 1/3 successful (33.3%) ![33%](https://img.shields.io/badge/success-33%25-red)
- **`simple-summarization`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-summarization`** (gpt-4.1-mini): 1/2 successful (50.0%) ![50%](https://img.shields.io/badge/success-50%25-yellow)

---

## Performance Metrics

### Cost Comparison

![Cost Comparison](cost_comparison.png)

| Agent Type | Model | Average Cost | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | $0.35 | ±$0.05 |
| `intent` | `google-gemini-2.5-pro` | $0.15 | ±$nan |
| `intent` | `gpt-4.1-mini` | $0.05 | ±$0.01 |
| `simple-raw` | `claude-sonnet-4.5` | $0.69 | ±$0.24 |
| `simple-raw` | `google-gemini-2.5-pro` | $0.12 | ±$nan |
| `simple-raw` | `gpt-4.1-mini` | $0.10 | ±$nan |
| `simple-summarization` | `claude-sonnet-4.5` | $0.66 | ±$nan |
| `simple-summarization` | `google-gemini-2.5-pro` | $0.16 | ±$nan |
| `simple-summarization` | `gpt-4.1-mini` | $0.05 | ±$nan |

### Execution Time

![Execution Time](execution_time.png)

| Agent Type | Model | Average Time | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | 200.2s | ±26.7s |
| `intent` | `google-gemini-2.5-pro` | 196.7s | ±nans |
| `intent` | `gpt-4.1-mini` | 128.6s | ±6.2s |
| `simple-raw` | `claude-sonnet-4.5` | 109.0s | ±6.4s |
| `simple-raw` | `google-gemini-2.5-pro` | 111.9s | ±nans |
| `simple-raw` | `gpt-4.1-mini` | 91.5s | ±28.0s |
| `simple-summarization` | `claude-sonnet-4.5` | 233.3s | ±14.2s |
| `simple-summarization` | `google-gemini-2.5-pro` | 123.4s | ±nans |
| `simple-summarization` | `gpt-4.1-mini` | 123.5s | ±39.6s |

### Step Count

![Step Count](step_count.png)

| Agent Type | Model | Average Steps | Std Dev |
|------------|-------|---------------|----------|
| `intent` | `claude-sonnet-4.5` | 16.3 | ±0.6 |
| `intent` | `google-gemini-2.5-pro` | 18.0 | ±nan |
| `intent` | `gpt-4.1-mini` | 14.5 | ±4.9 |
| `simple-raw` | `claude-sonnet-4.5` | 43.3 | ±3.1 |
| `simple-raw` | `google-gemini-2.5-pro` | 20.0 | ±nan |
| `simple-raw` | `gpt-4.1-mini` | 87.5 | ±19.1 |
| `simple-summarization` | `claude-sonnet-4.5` | 50.0 | ±0.0 |
| `simple-summarization` | `google-gemini-2.5-pro` | 24.0 | ±nan |
| `simple-summarization` | `gpt-4.1-mini` | 65.5 | ±4.9 |

### Token Usage

![Token Usage](token_usage.png)

| Agent Type | Model | Input Tokens | Output Tokens | Total Tokens |
|------------|-------|--------------|---------------|-------------|
| `intent` | `claude-sonnet-4.5` | 153637 | 9895 | 163532 |
| `intent` | `google-gemini-2.5-pro` | 96056 | 18008 | 114064 |
| `intent` | `gpt-4.1-mini` | 66312 | 7764 | 74075 |
| `simple-raw` | `claude-sonnet-4.5` | 206549 | 4890 | 211439 |
| `simple-raw` | `google-gemini-2.5-pro` | 25278 | 9018 | 34296 |
| `simple-raw` | `gpt-4.1-mini` | 211686 | 3636 | 215322 |
| `simple-summarization` | `claude-sonnet-4.5` | 183831 | 6229 | 190060 |
| `simple-summarization` | `google-gemini-2.5-pro` | 32588 | 11767 | 44355 |
| `simple-summarization` | `gpt-4.1-mini` | 106056 | 4188 | 110245 |

### Tokens vs Steps Relationship

![Tokens vs Steps](tokens_vs_steps.png)

### Per-Step Latency

![Per-Step Latency](per_step_latency.png)

| Agent Type | Model | Avg Latency per Step | Std Dev |
|------------|-------|----------------------|----------|
| `intent` | `claude-sonnet-4.5` | 12.23s | ±1.19s |
| `intent` | `google-gemini-2.5-pro` | 10.93s | ±nans |
| `intent` | `gpt-4.1-mini` | 9.34s | ±2.76s |
| `simple-raw` | `claude-sonnet-4.5` | 2.52s | ±0.23s |
| `simple-raw` | `google-gemini-2.5-pro` | 5.59s | ±nans |
| `simple-raw` | `gpt-4.1-mini` | 1.11s | ±0.56s |
| `simple-summarization` | `claude-sonnet-4.5` | 4.67s | ±0.28s |
| `simple-summarization` | `google-gemini-2.5-pro` | 5.14s | ±nans |
| `simple-summarization` | `gpt-4.1-mini` | 1.91s | ±0.75s |

### Token Processing Throughput

![Tokens per Second](tokens_per_second.png)

| Agent Type | Model | Tokens/Second | Std Dev |
|------------|-------|---------------|----------|
| `intent` | `claude-sonnet-4.5` | 820 | ±35 |
| `intent` | `google-gemini-2.5-pro` | 580 | ±nan |
| `intent` | `gpt-4.1-mini` | 575 | ±55 |
| `simple-raw` | `claude-sonnet-4.5` | 1914 | ±642 |
| `simple-raw` | `google-gemini-2.5-pro` | 307 | ±nan |
| `simple-raw` | `gpt-4.1-mini` | 2430 | ±499 |
| `simple-summarization` | `claude-sonnet-4.5` | 816 | ±42 |
| `simple-summarization` | `google-gemini-2.5-pro` | 359 | ±nan |
| `simple-summarization` | `gpt-4.1-mini` | 943 | ±318 |

### Latency vs Token Usage

![Latency vs Tokens](latency_vs_tokens.png)

This scatter plot shows the relationship between tokens per step and latency per step, helping identify efficiency patterns across different agent configurations.

### Accuracy Score

![Accuracy Score](accuracy_score.png)

| Agent Type | Model | Average Accuracy | Std Dev |
|------------|-------|------------------|----------|
| `intent` | `claude-sonnet-4.5` | 66.67% | ±16.67% |
| `intent` | `google-gemini-2.5-pro` | 83.33% | ±nan% |
| `intent` | `gpt-4.1-mini` | 91.67% | ±11.79% |
| `simple-raw` | `claude-sonnet-4.5` | 88.89% | ±9.62% |
| `simple-raw` | `google-gemini-2.5-pro` | 66.67% | ±nan% |
| `simple-raw` | `gpt-4.1-mini` | 33.33% | ±nan% |
| `simple-summarization` | `claude-sonnet-4.5` | 83.33% | ±nan% |
| `simple-summarization` | `google-gemini-2.5-pro` | 66.67% | ±nan% |
| `simple-summarization` | `gpt-4.1-mini` | 33.33% | ±nan% |

### Field-Level Accuracy Analysis

#### Field Accuracy Heatmap

![Field Accuracy Heatmap](field_accuracy_heatmap.png)

#### Proximity Score Heatmap

![Field Proximity Heatmap](field_proximity_heatmap.png)

#### Field Accuracy Rates

| Field | intent (claude-sonnet-4.5) | intent (google-gemini-2.5-pro) | intent (gpt-4.1-mini) | simple-raw (claude-sonnet-4.5) | simple-raw (google-gemini-2.5-pro) | simple-raw (gpt-4.1-mini) | simple-summarization (claude-sonnet-4.5) | simple-summarization (google-gemini-2.5-pro) | simple-summarization (gpt-4.1-mini) |
|---|---|---|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 0% | 100% | 100% | 33% | 0% | 0% | 0% | 0% | 0% |
| `best_revenue_hour` | 67% | 100% | 100% | 100% | 100% | 0% | 100% | 100% | 100% |
| `best_revenue_zone` | 67% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| `optimal_distance_bracket` | 100% | 0% | 50% | 100% | 0% | 100% | 100% | 0% | 0% |
| `trips_above_max_distance` | 100% | 100% | 100% | 100% | 100% | 0% | 100% | 100% | 0% |
| `trips_below_min_fare` | 67% | 100% | 100% | 100% | 100% | 0% | 100% | 100% | 0% |

#### Percentage Error (Numeric Fields)

![Percentage Error](field_percentage_error.png)

| Field | intent (claude-sonnet-4.5) | intent (google-gemini-2.5-pro) | intent (gpt-4.1-mini) | simple-raw (claude-sonnet-4.5) | simple-raw (google-gemini-2.5-pro) | simple-raw (gpt-4.1-mini) | simple-summarization (claude-sonnet-4.5) | simple-summarization (google-gemini-2.5-pro) | simple-summarization (gpt-4.1-mini) |
|---|---|---|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 42.4% | 0.0% | 0.0% | 29.2% | 39.7% | 8.0% | 43.7% | 43.7% | 36.1% |
| `best_revenue_hour` | 2.0% | 0.0% | 0.0% | 0.0% | 0.0% | 5.9% | 0.0% | 0.0% | 0.0% |
| `trips_above_max_distance` | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 92.7% | 0.0% | 0.0% | 92.7% |
| `trips_below_min_fare` | 18.4% | 0.0% | 0.0% | 0.0% | 0.0% | 93.2% | 0.0% | 0.0% | 93.2% |

---

## Detailed Analysis

### `intent` (openai-gpt-4.1-mini)

![Runs](https://img.shields.io/badge/runs-6-blue) ![Success](https://img.shields.io/badge/success-6-green) 

**Performance (Successful Runs Only):**

- **Average Steps:** 16.0
- **Average Cost:** $0.21
- **Average Time:** 175.7s
- **Average Tokens:** 125468
- **Tokens per Step:** 7820
- **Cost per Step:** $0.0130
- **Time per Step:** 11.05s
- **Average Accuracy:** 77.78%

### `simple-raw` (openai-gpt-4.1-mini)

![Runs](https://img.shields.io/badge/runs-6-blue) ![Success](https://img.shields.io/badge/success-5-green) ![Failed](https://img.shields.io/badge/failed-1-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 44.8
- **Average Cost:** $0.46
- **Average Time:** 110.1s
- **Average Tokens:** 179972
- **Tokens per Step:** 3899
- **Cost per Step:** $0.0111
- **Time per Step:** 2.93s
- **Average Accuracy:** 73.33%

**Note:** This agent had failed runs. Check detailed metrics for more information.

### `simple-summarization` (openai-gpt-4.1-mini)

![Runs](https://img.shields.io/badge/runs-6-blue) ![Success](https://img.shields.io/badge/success-3-green) ![Failed](https://img.shields.io/badge/failed-3-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 45.3
- **Average Cost:** $0.29
- **Average Time:** 174.8s
- **Average Tokens:** 114980
- **Tokens per Step:** 2479
- **Cost per Step:** $0.0069
- **Time per Step:** 4.19s
- **Average Accuracy:** 61.11%

**Note:** This agent had failed runs. Check detailed metrics for more information.

---

## Key Insights

### Rankings

#### Success Rate

🥇 **`intent`** (claude-sonnet-4.5): 100.0%  
🥈 **`intent`** (google-gemini-2.5-pro): 100.0%  
🥉 **`intent`** (gpt-4.1-mini): 100.0%  
4. **`simple-raw`** (claude-sonnet-4.5): 100.0%  
5. **`simple-raw`** (google-gemini-2.5-pro): 100.0%  
6. **`simple-summarization`** (google-gemini-2.5-pro): 100.0%  
7. **`simple-raw`** (gpt-4.1-mini): 50.0%  
8. **`simple-summarization`** (gpt-4.1-mini): 50.0%  
9. **`simple-summarization`** (claude-sonnet-4.5): 33.3%  

#### Cost Efficiency (Lower is Better)

🥇 **`intent`** (gpt-4.1-mini): $0.05  
🥈 **`simple-summarization`** (gpt-4.1-mini): $0.05  
🥉 **`simple-raw`** (gpt-4.1-mini): $0.10  
4. **`simple-raw`** (google-gemini-2.5-pro): $0.12  
5. **`intent`** (google-gemini-2.5-pro): $0.15  
6. **`simple-summarization`** (google-gemini-2.5-pro): $0.16  
7. **`intent`** (claude-sonnet-4.5): $0.35  
8. **`simple-summarization`** (claude-sonnet-4.5): $0.66  
9. **`simple-raw`** (claude-sonnet-4.5): $0.69  

#### Speed (Lower is Better)

🥇 **`simple-raw`** (claude-sonnet-4.5): 109.0s  
🥈 **`simple-raw`** (gpt-4.1-mini): 111.3s  
🥉 **`simple-raw`** (google-gemini-2.5-pro): 111.9s  
4. **`simple-summarization`** (google-gemini-2.5-pro): 123.4s  
5. **`intent`** (gpt-4.1-mini): 128.6s  
6. **`simple-summarization`** (gpt-4.1-mini): 151.5s  
7. **`intent`** (google-gemini-2.5-pro): 196.7s  
8. **`intent`** (claude-sonnet-4.5): 200.2s  
9. **`simple-summarization`** (claude-sonnet-4.5): 249.5s  

#### Accuracy (Higher is Better)

🥇 **`intent`** (gpt-4.1-mini): 91.67%  
🥈 **`simple-raw`** (claude-sonnet-4.5): 88.89%  
🥉 **`intent`** (google-gemini-2.5-pro): 83.33%  
4. **`simple-summarization`** (claude-sonnet-4.5): 83.33%  
5. **`intent`** (claude-sonnet-4.5): 66.67%  
6. **`simple-raw`** (google-gemini-2.5-pro): 66.67%  
7. **`simple-summarization`** (google-gemini-2.5-pro): 66.67%  
8. **`simple-raw`** (gpt-4.1-mini): 33.33%  
9. **`simple-summarization`** (gpt-4.1-mini): 33.33%  

---

## Recommendations

### Best Agent for Different Use Cases

- **💰 Most Cost-Efficient:** `intent` (gpt-4.1-mini) - $0.05 per run
- **⚡ Fastest:** `simple-raw` (claude-sonnet-4.5) - 109.0s per run
- **🎯 Most Accurate:** `intent` (gpt-4.1-mini) - 91.67% accuracy
- **✅ Most Reliable:** `intent` (claude-sonnet-4.5) - 100.0% success rate

### Overall Assessment

Based on the analysis:

The data suggests different agents excel in different areas. Choose based on your priorities:

- If **budget is critical**, prioritize the most cost-efficient agent
- If **speed is essential**, choose the fastest agent
- If **accuracy matters most**, select the most accurate agent
- If **reliability is key**, go with the highest success rate

---

*Report generated on 2025-11-07 02:37:18*
