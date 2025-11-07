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

**Total Runs Analyzed:** 39  
**Agent Types:** 3  
**Date:** 2025-11-07

**Models Tested:** `anthropic-claude-sonnet-4.5`, `openai-gpt-5`, `openai-gpt-4.1-mini`, `google-gemini-2.5-pro`, `openai-gpt-4.1`

### Quick Stats

| Agent Type | Model | Runs | Success Rate | Avg Cost | Avg Time | Avg Steps |
|------------|-------|------|--------------|----------|----------|----------|
| `intent` | `claude-sonnet-4.5` | 5 | 100.0% | $0.38 | 208.7s | 17.4 |
| `intent` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.15 | 196.7s | 18.0 |
| `intent` | `gpt-4.1` | 2 | 100.0% | $0.32 | 253.2s | 22.0 |
| `intent` | `gpt-4.1-mini` | 4 | 100.0% | $0.05 | 108.4s | 15.5 |
| `intent` | `gpt-5` | 1 | 0.0% | $0.11 | 97.4s | 12.0 |
| `simple-raw` | `claude-sonnet-4.5` | 5 | 100.0% | $0.85 | 945.9s | 46.0 |
| `simple-raw` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.12 | 111.9s | 20.0 |
| `simple-raw` | `gpt-4.1` | 2 | 100.0% | $0.32 | 88.6s | 56.0 |
| `simple-raw` | `gpt-4.1-mini` | 4 | 25.0% | $0.10 | 99.9s | 89.5 |
| `simple-raw` | `gpt-5` | 1 | 0.0% | $0.29 | 181.2s | 34.0 |
| `simple-summarization` | `claude-sonnet-4.5` | 5 | 60.0% | $0.57 | 189.5s | 46.0 |
| `simple-summarization` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.16 | 123.4s | 24.0 |
| `simple-summarization` | `gpt-4.1` | 2 | 0.0% | $0.27 | 51.6s | 67.0 |
| `simple-summarization` | `gpt-4.1-mini` | 4 | 50.0% | $0.08 | 108.6s | 63.2 |
| `simple-summarization` | `gpt-5` | 1 | 0.0% | $0.37 | 227.2s | 41.0 |

---

## Success Rate

![Success Rate](success_rate.png)

- **`intent`** (claude-sonnet-4.5): 5/5 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (gpt-4.1): 2/2 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (gpt-4.1-mini): 4/4 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (gpt-5): 0/1 successful (0.0%) ![0%](https://img.shields.io/badge/success-0%25-red)
- **`simple-raw`** (claude-sonnet-4.5): 5/5 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (gpt-4.1): 2/2 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (gpt-4.1-mini): 1/4 successful (25.0%) ![25%](https://img.shields.io/badge/success-25%25-red)
- **`simple-raw`** (gpt-5): 0/1 successful (0.0%) ![0%](https://img.shields.io/badge/success-0%25-red)
- **`simple-summarization`** (claude-sonnet-4.5): 3/5 successful (60.0%) ![60%](https://img.shields.io/badge/success-60%25-yellow)
- **`simple-summarization`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-summarization`** (gpt-4.1): 0/2 successful (0.0%) ![0%](https://img.shields.io/badge/success-0%25-red)
- **`simple-summarization`** (gpt-4.1-mini): 2/4 successful (50.0%) ![50%](https://img.shields.io/badge/success-50%25-yellow)
- **`simple-summarization`** (gpt-5): 0/1 successful (0.0%) ![0%](https://img.shields.io/badge/success-0%25-red)

---

## Performance Metrics

### Cost Comparison

![Cost Comparison](cost_comparison.png)

| Agent Type | Model | Average Cost | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | $0.38 | ±$0.09 |
| `intent` | `google-gemini-2.5-pro` | $0.15 | ±$nan |
| `intent` | `gpt-4.1` | $0.32 | ±$0.16 |
| `intent` | `gpt-4.1-mini` | $0.05 | ±$0.01 |
| `simple-raw` | `claude-sonnet-4.5` | $0.85 | ±$0.46 |
| `simple-raw` | `google-gemini-2.5-pro` | $0.12 | ±$nan |
| `simple-raw` | `gpt-4.1` | $0.32 | ±$0.20 |
| `simple-raw` | `gpt-4.1-mini` | $0.10 | ±$nan |
| `simple-summarization` | `claude-sonnet-4.5` | $0.52 | ±$0.14 |
| `simple-summarization` | `google-gemini-2.5-pro` | $0.16 | ±$nan |
| `simple-summarization` | `gpt-4.1-mini` | $0.06 | ±$0.02 |

### Execution Time

![Execution Time](execution_time.png)

| Agent Type | Model | Average Time | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | 208.7s | ±40.5s |
| `intent` | `google-gemini-2.5-pro` | 196.7s | ±nans |
| `intent` | `gpt-4.1` | 253.2s | ±146.1s |
| `intent` | `gpt-4.1-mini` | 108.4s | ±23.6s |
| `intent` | `gpt-5` | 97.4s | ±nans |
| `simple-raw` | `claude-sonnet-4.5` | 945.9s | ±1834.9s |
| `simple-raw` | `google-gemini-2.5-pro` | 111.9s | ±nans |
| `simple-raw` | `gpt-4.1` | 88.6s | ±15.1s |
| `simple-raw` | `gpt-4.1-mini` | 99.9s | ±19.0s |
| `simple-raw` | `gpt-5` | 181.2s | ±nans |
| `simple-summarization` | `claude-sonnet-4.5` | 189.5s | ±61.5s |
| `simple-summarization` | `google-gemini-2.5-pro` | 123.4s | ±nans |
| `simple-summarization` | `gpt-4.1` | 51.6s | ±9.3s |
| `simple-summarization` | `gpt-4.1-mini` | 108.6s | ±30.6s |
| `simple-summarization` | `gpt-5` | 227.2s | ±nans |

### Step Count

![Step Count](step_count.png)

| Agent Type | Model | Average Steps | Std Dev |
|------------|-------|---------------|----------|
| `intent` | `claude-sonnet-4.5` | 17.4 | ±3.2 |
| `intent` | `google-gemini-2.5-pro` | 18.0 | ±nan |
| `intent` | `gpt-4.1` | 22.0 | ±11.3 |
| `intent` | `gpt-4.1-mini` | 15.5 | ±3.7 |
| `intent` | `gpt-5` | 12.0 | ±nan |
| `simple-raw` | `claude-sonnet-4.5` | 46.0 | ±5.1 |
| `simple-raw` | `google-gemini-2.5-pro` | 20.0 | ±nan |
| `simple-raw` | `gpt-4.1` | 56.0 | ±31.1 |
| `simple-raw` | `gpt-4.1-mini` | 89.5 | ±13.7 |
| `simple-raw` | `gpt-5` | 34.0 | ±nan |
| `simple-summarization` | `claude-sonnet-4.5` | 46.0 | ±6.2 |
| `simple-summarization` | `google-gemini-2.5-pro` | 24.0 | ±nan |
| `simple-summarization` | `gpt-4.1` | 67.0 | ±0.0 |
| `simple-summarization` | `gpt-4.1-mini` | 63.2 | ±6.2 |
| `simple-summarization` | `gpt-5` | 41.0 | ±nan |

### Token Usage

![Token Usage](token_usage.png)

| Agent Type | Model | Input Tokens | Output Tokens | Total Tokens |
|------------|-------|--------------|---------------|-------------|
| `intent` | `claude-sonnet-4.5` | 168361 | 10242 | 178604 |
| `intent` | `google-gemini-2.5-pro` | 96056 | 18008 | 114064 |
| `intent` | `gpt-4.1` | 124312 | 11144 | 135456 |
| `intent` | `gpt-4.1-mini` | 69216 | 7054 | 76269 |
| `intent` | `gpt-5` | 47398 | 5976 | 53374 |
| `simple-raw` | `claude-sonnet-4.5` | 251165 | 6184 | 257349 |
| `simple-raw` | `google-gemini-2.5-pro` | 25278 | 9018 | 34296 |
| `simple-raw` | `gpt-4.1` | 134408 | 6092 | 140501 |
| `simple-raw` | `gpt-4.1-mini` | 222522 | 4203 | 226725 |
| `simple-raw` | `gpt-5` | 150796 | 9851 | 160647 |
| `simple-summarization` | `claude-sonnet-4.5` | 156529 | 6496 | 163025 |
| `simple-summarization` | `google-gemini-2.5-pro` | 32588 | 11767 | 44355 |
| `simple-summarization` | `gpt-4.1` | 127148 | 1825 | 128972 |
| `simple-summarization` | `gpt-4.1-mini` | 187664 | 4066 | 191731 |
| `simple-summarization` | `gpt-5` | 198961 | 12099 | 211060 |

### Tokens vs Steps Relationship

![Tokens vs Steps](tokens_vs_steps.png)

### Per-Step Latency

![Per-Step Latency](per_step_latency.png)

| Agent Type | Model | Avg Latency per Step | Std Dev |
|------------|-------|----------------------|----------|
| `intent` | `claude-sonnet-4.5` | 11.99s | ±0.90s |
| `intent` | `google-gemini-2.5-pro` | 10.93s | ±nans |
| `intent` | `gpt-4.1` | 11.29s | ±0.84s |
| `intent` | `gpt-4.1-mini` | 7.41s | ±2.83s |
| `intent` | `gpt-5` | 8.12s | ±nans |
| `simple-raw` | `claude-sonnet-4.5` | 20.54s | ±39.90s |
| `simple-raw` | `google-gemini-2.5-pro` | 5.59s | ±nans |
| `simple-raw` | `gpt-4.1` | 1.78s | ±0.72s |
| `simple-raw` | `gpt-4.1-mini` | 1.15s | ±0.34s |
| `simple-raw` | `gpt-5` | 5.33s | ±nans |
| `simple-summarization` | `claude-sonnet-4.5` | 4.04s | ±0.88s |
| `simple-summarization` | `google-gemini-2.5-pro` | 5.14s | ±nans |
| `simple-summarization` | `gpt-4.1` | 0.77s | ±0.14s |
| `simple-summarization` | `gpt-4.1-mini` | 1.74s | ±0.56s |
| `simple-summarization` | `gpt-5` | 5.54s | ±nans |

### Token Processing Throughput

![Tokens per Second](tokens_per_second.png)

| Agent Type | Model | Tokens/Second | Std Dev |
|------------|-------|---------------|----------|
| `intent` | `claude-sonnet-4.5` | 855 | ±54 |
| `intent` | `google-gemini-2.5-pro` | 580 | ±nan |
| `intent` | `gpt-4.1` | 542 | ±26 |
| `intent` | `gpt-4.1-mini` | 733 | ±299 |
| `intent` | `gpt-5` | 548 | ±nan |
| `simple-raw` | `claude-sonnet-4.5` | 1724 | ±1121 |
| `simple-raw` | `google-gemini-2.5-pro` | 307 | ±nan |
| `simple-raw` | `gpt-4.1` | 1508 | ±918 |
| `simple-raw` | `gpt-4.1-mini` | 2308 | ±481 |
| `simple-raw` | `gpt-5` | 887 | ±nan |
| `simple-summarization` | `claude-sonnet-4.5` | 882 | ±115 |
| `simple-summarization` | `google-gemini-2.5-pro` | 359 | ±nan |
| `simple-summarization` | `gpt-4.1` | 2548 | ±556 |
| `simple-summarization` | `gpt-4.1-mini` | 2033 | ±1744 |
| `simple-summarization` | `gpt-5` | 929 | ±nan |

### Latency vs Token Usage

![Latency vs Tokens](latency_vs_tokens.png)

This scatter plot shows the relationship between tokens per step and latency per step, helping identify efficiency patterns across different agent configurations.

### Token Growth Scaling Analysis

![Token Growth Regression](token_growth_regression.png)

Polynomial regression (degree 2-3) showing how **tokens per step** changes as total steps increase. This reveals whether agents become more/less efficient with more steps. Curves are color-coded: 🟢 **green** = improving efficiency, 🔴 **red** = degrading efficiency, 🔵 **blue** = stable. Solid curves show fitted trend, dotted lines extrapolate beyond observed data (constrained to positive values).

#### Model Fit Parameters

| Agent Type | Model | Degree | R² | Equation |
|------------|-------|--------|-----|----------|
| `intent` | `claude-sonnet-4.5` | 3 | 0.951 | `-112x^3 + 6136x^2 - 110306x + 661485` |
| `intent` | `gpt-4.1-mini` | 3 | 1.000 | `1.89x^3 + 49.42x^2 - 2866x + 29081` |
| `simple-raw` | `claude-sonnet-4.5` | 3 | 0.853 | `-23.27x^3 + 3309x^2 - 155409x + 2417500` |
| `simple-raw` | `gpt-4.1-mini` | 2 | 0.515 | `4.50x^2 - 814x + 38675` |
| `simple-summarization` | `claude-sonnet-4.5` | 2 | 0.998 | `0.93x^2 - 5.50x + 1752` |
| `simple-summarization` | `gpt-4.1-mini` | 3 | 1.000 | `-33.27x^3 + 6202x^2 - 383819x + 7888651` |

**Interpretation:**
- **Degree**: Polynomial degree (2 or 3) selected for best fit
- **R²**: Goodness of fit (higher = better, 1.0 = perfect fit)
- **Equation**: Polynomial function describing tokens/step as function of total steps (x)

#### Efficiency Rankings

Ranked by efficiency change from 50 to 100 steps (negative = improving, positive = degrading):

🥇 **`simple-raw`** (claude-sonnet-4.5): 🟢 -33534.0% (improving)  
🥈 **`simple-summarization`** (gpt-4.1-mini): 🟢 -4162.4% (improving)  
🥉 **`simple-raw`** (gpt-4.1-mini): 🟢 -74.6% (improving)  
4. **`simple-summarization`** (claude-sonnet-4.5): 🔴 +176.2% (degrading)  
5. **`intent`** (gpt-4.1-mini): 🔴 +765.9% (degrading)  

#### Predicted Tokens per Step at Different Scales

| Agent Type | Model | @ 50 steps | @ 100 steps | @ 200 steps | @ 500 steps |
|------------|-------|------------|-------------|-------------|-------------|
| `intent` | `claude-sonnet-4.5` | 0 | 0 | 0 | 0 |
| `intent` | `gpt-4.1-mini` | 245,574 | 2,126,527 | 16,551,168 | 247,175,484 |
| `simple-raw` | `claude-sonnet-4.5` | 9,893 | 0 | 0 | 0 |
| `simple-raw` | `gpt-4.1-mini` | 9,249 | 2,345 | 56,100 | 757,881 |
| `simple-summarization` | `claude-sonnet-4.5` | 3,801 | 10,499 | 37,844 | 231,459 |
| `simple-summarization` | `gpt-4.1-mini` | 42,997 | 0 | 0 | 0 |

#### Predicted Total Token Usage at Different Scales

| Agent Type | Model | @ 50 steps | @ 100 steps | @ 200 steps | @ 500 steps |
|------------|-------|------------|-------------|-------------|-------------|
| `intent` | `claude-sonnet-4.5` | 0 | 0 | 0 | 0 |
| `intent` | `gpt-4.1-mini` | 12,278,735 | 212,652,708 | 3,310,233,736 | 123,587,742,226 |
| `simple-raw` | `claude-sonnet-4.5` | 494,660 | 0 | 0 | 0 |
| `simple-raw` | `gpt-4.1-mini` | 462,485 | 234,533 | 11,220,173 | 378,940,833 |
| `simple-summarization` | `claude-sonnet-4.5` | 190,060 | 1,049,984 | 7,568,933 | 115,729,775 |
| `simple-summarization` | `gpt-4.1-mini` | 2,149,877 | 0 | 0 | 0 |

### Accuracy Score

![Accuracy Score](accuracy_score.png)

| Agent Type | Model | Average Accuracy | Std Dev |
|------------|-------|------------------|----------|
| `intent` | `claude-sonnet-4.5` | 73.33% | ±14.91% |
| `intent` | `google-gemini-2.5-pro` | 83.33% | ±nan% |
| `intent` | `gpt-4.1` | 16.67% | ±0.00% |
| `intent` | `gpt-4.1-mini` | 62.50% | ±34.36% |
| `simple-raw` | `claude-sonnet-4.5` | 80.00% | ±13.94% |
| `simple-raw` | `google-gemini-2.5-pro` | 66.67% | ±nan% |
| `simple-raw` | `gpt-4.1` | 25.00% | ±35.36% |
| `simple-raw` | `gpt-4.1-mini` | 33.33% | ±nan% |
| `simple-summarization` | `claude-sonnet-4.5` | 77.78% | ±9.62% |
| `simple-summarization` | `google-gemini-2.5-pro` | 66.67% | ±nan% |
| `simple-summarization` | `gpt-4.1-mini` | 25.00% | ±11.79% |

### Field-Level Accuracy Analysis

#### Field Accuracy Heatmap

![Field Accuracy Heatmap](field_accuracy_heatmap.png)

#### Proximity Score Heatmap

![Field Proximity Heatmap](field_proximity_heatmap.png)

#### Field Accuracy Rates

| Field | intent (claude-sonnet-4.5) | intent (google-gemini-2.5-pro) | intent (gpt-4.1) | intent (gpt-4.1-mini) | simple-raw (claude-sonnet-4.5) | simple-raw (google-gemini-2.5-pro) | simple-raw (gpt-4.1) | simple-raw (gpt-4.1-mini) | simple-summarization (claude-sonnet-4.5) | simple-summarization (google-gemini-2.5-pro) | simple-summarization (gpt-4.1-mini) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 0% | 100% | 0% | 50% | 20% | 0% | 0% | 0% | 33% | 0% | 0% |
| `best_revenue_hour` | 80% | 100% | 0% | 100% | 100% | 100% | 50% | 0% | 100% | 100% | 50% |
| `best_revenue_zone` | 80% | 100% | 100% | 75% | 100% | 100% | 50% | 100% | 100% | 100% | 100% |
| `optimal_distance_bracket` | 100% | 0% | 0% | 50% | 60% | 0% | 50% | 100% | 33% | 0% | 0% |
| `trips_above_max_distance` | 100% | 100% | 0% | 50% | 100% | 100% | 0% | 0% | 100% | 100% | 0% |
| `trips_below_min_fare` | 80% | 100% | 0% | 50% | 100% | 100% | 0% | 0% | 100% | 100% | 0% |

#### Percentage Error (Numeric Fields)

![Percentage Error](field_percentage_error.png)

| Field | intent (claude-sonnet-4.5) | intent (google-gemini-2.5-pro) | intent (gpt-4.1) | intent (gpt-4.1-mini) | simple-raw (claude-sonnet-4.5) | simple-raw (google-gemini-2.5-pro) | simple-raw (gpt-4.1) | simple-raw (gpt-4.1-mini) | simple-summarization (claude-sonnet-4.5) | simple-summarization (google-gemini-2.5-pro) | simple-summarization (gpt-4.1-mini) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 40.8% | 0.0% | 6.6% | 4.0% | 35.0% | 39.7% | 25.8% | 8.0% | 29.2% | 43.7% | 35.1% |
| `best_revenue_hour` | 1.2% | 0.0% | 5.9% | 0.0% | 0.0% | 0.0% | 2.9% | 5.9% | 0.0% | 0.0% | 2.9% |
| `trips_above_max_distance` | 0.0% | 0.0% | 87.7% | 46.4% | 0.0% | 0.0% | 53.8% | 92.7% | 0.0% | 0.0% | 84.0% |
| `trips_below_min_fare` | 11.1% | 0.0% | 87.5% | 46.6% | 0.0% | 0.0% | 94.8% | 93.2% | 0.0% | 0.0% | 90.6% |

---

## Detailed Analysis

### `intent` (anthropic-claude-sonnet-4.5)

![Runs](https://img.shields.io/badge/runs-13-blue) ![Success](https://img.shields.io/badge/success-12-green) ![Failed](https://img.shields.io/badge/failed-1-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 17.6
- **Average Cost:** $0.24
- **Average Time:** 181.6s
- **Average Tokens:** 131923
- **Tokens per Step:** 7460
- **Cost per Step:** $0.0130
- **Time per Step:** 10.26s
- **Average Accuracy:** 61.11%

**Note:** This agent had failed runs. Check detailed metrics for more information.

### `simple-raw` (anthropic-claude-sonnet-4.5)

![Runs](https://img.shields.io/badge/runs-13-blue) ![Success](https://img.shields.io/badge/success-9-green) ![Failed](https://img.shields.io/badge/failed-4-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 48.4
- **Average Cost:** $0.57
- **Average Time:** 570.0s
- **Average Tokens:** 203699
- **Tokens per Step:** 4088
- **Cost per Step:** $0.0120
- **Time per Step:** 12.60s
- **Average Accuracy:** 61.11%

**Note:** This agent had failed runs. Check detailed metrics for more information.

### `simple-summarization` (anthropic-claude-sonnet-4.5)

![Runs](https://img.shields.io/badge/runs-13-blue) ![Success](https://img.shields.io/badge/success-6-green) ![Failed](https://img.shields.io/badge/failed-7-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 45.2
- **Average Cost:** $0.31
- **Average Time:** 146.4s
- **Average Tokens:** 127808
- **Tokens per Step:** 2787
- **Cost per Step:** $0.0074
- **Time per Step:** 3.45s
- **Average Accuracy:** 58.33%

**Note:** This agent had failed runs. Check detailed metrics for more information.

---

## Key Insights

### Rankings

#### Success Rate

🥇 **`intent`** (claude-sonnet-4.5): 100.0%  
🥈 **`intent`** (google-gemini-2.5-pro): 100.0%  
🥉 **`intent`** (gpt-4.1): 100.0%  
4. **`intent`** (gpt-4.1-mini): 100.0%  
5. **`simple-raw`** (claude-sonnet-4.5): 100.0%  
6. **`simple-raw`** (google-gemini-2.5-pro): 100.0%  
7. **`simple-raw`** (gpt-4.1): 100.0%  
8. **`simple-summarization`** (google-gemini-2.5-pro): 100.0%  
9. **`simple-summarization`** (claude-sonnet-4.5): 60.0%  
10. **`simple-summarization`** (gpt-4.1-mini): 50.0%  
11. **`simple-raw`** (gpt-4.1-mini): 25.0%  
12. **`intent`** (gpt-5): 0.0%  
13. **`simple-raw`** (gpt-5): 0.0%  
14. **`simple-summarization`** (gpt-4.1): 0.0%  
15. **`simple-summarization`** (gpt-5): 0.0%  

#### Cost Efficiency (Lower is Better)

🥇 **`intent`** (gpt-4.1-mini): $0.05  
🥈 **`simple-summarization`** (gpt-4.1-mini): $0.06  
🥉 **`simple-raw`** (gpt-4.1-mini): $0.10  
4. **`simple-raw`** (google-gemini-2.5-pro): $0.12  
5. **`intent`** (google-gemini-2.5-pro): $0.15  
6. **`simple-summarization`** (google-gemini-2.5-pro): $0.16  
7. **`simple-raw`** (gpt-4.1): $0.32  
8. **`intent`** (gpt-4.1): $0.32  
9. **`intent`** (claude-sonnet-4.5): $0.38  
10. **`simple-summarization`** (claude-sonnet-4.5): $0.52  
11. **`simple-raw`** (claude-sonnet-4.5): $0.85  

#### Speed (Lower is Better)

🥇 **`simple-raw`** (gpt-4.1): 88.6s  
🥈 **`intent`** (gpt-4.1-mini): 108.4s  
🥉 **`simple-raw`** (gpt-4.1-mini): 111.3s  
4. **`simple-raw`** (google-gemini-2.5-pro): 111.9s  
5. **`simple-summarization`** (google-gemini-2.5-pro): 123.4s  
6. **`simple-summarization`** (gpt-4.1-mini): 129.1s  
7. **`simple-summarization`** (claude-sonnet-4.5): 165.6s  
8. **`intent`** (google-gemini-2.5-pro): 196.7s  
9. **`intent`** (claude-sonnet-4.5): 208.7s  
10. **`intent`** (gpt-4.1): 253.2s  
11. **`simple-raw`** (claude-sonnet-4.5): 945.9s  

#### Accuracy (Higher is Better)

🥇 **`intent`** (google-gemini-2.5-pro): 83.33%  
🥈 **`simple-raw`** (claude-sonnet-4.5): 80.00%  
🥉 **`simple-summarization`** (claude-sonnet-4.5): 77.78%  
4. **`intent`** (claude-sonnet-4.5): 73.33%  
5. **`simple-raw`** (google-gemini-2.5-pro): 66.67%  
6. **`simple-summarization`** (google-gemini-2.5-pro): 66.67%  
7. **`intent`** (gpt-4.1-mini): 62.50%  
8. **`simple-raw`** (gpt-4.1-mini): 33.33%  
9. **`simple-raw`** (gpt-4.1): 25.00%  
10. **`simple-summarization`** (gpt-4.1-mini): 25.00%  
11. **`intent`** (gpt-4.1): 16.67%  

---

## Recommendations

### Best Agent for Different Use Cases

- **💰 Most Cost-Efficient:** `intent` (gpt-4.1-mini) - $0.05 per run
- **⚡ Fastest:** `simple-raw` (gpt-4.1) - 88.6s per run
- **🎯 Most Accurate:** `intent` (google-gemini-2.5-pro) - 83.33% accuracy
- **✅ Most Reliable:** `intent` (claude-sonnet-4.5) - 100.0% success rate

### Overall Assessment

Based on the analysis:

The data suggests different agents excel in different areas. Choose based on your priorities:

- If **budget is critical**, prioritize the most cost-efficient agent
- If **speed is essential**, choose the fastest agent
- If **accuracy matters most**, select the most accurate agent
- If **reliability is key**, go with the highest success rate

---

*Report generated on 2025-11-07 17:47:46*
