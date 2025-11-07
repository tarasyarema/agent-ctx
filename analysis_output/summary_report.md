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

**Total Runs Analyzed:** 36  
**Agent Types:** 3  
**Date:** 2025-11-07

**Models Tested:** `anthropic-claude-sonnet-4.5`, `openai-gpt-4.1-mini`, `google-gemini-2.5-pro`, `openai-gpt-4.1`

### Quick Stats

| Agent Type | Model | Runs | Success Rate | Avg Cost | Avg Time | Avg Steps |
|------------|-------|------|--------------|----------|----------|----------|
| `intent` | `claude-sonnet-4.5` | 4 | 100.0% | $0.34 | 193.5s | 16.0 |
| `intent` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.15 | 196.7s | 18.0 |
| `intent` | `gpt-4.1` | 3 | 100.0% | $0.32 | 230.2s | 21.7 |
| `intent` | `gpt-4.1-mini` | 4 | 100.0% | $0.05 | 108.4s | 15.5 |
| `simple-raw` | `claude-sonnet-4.5` | 4 | 100.0% | $0.92 | 125.5s | 46.0 |
| `simple-raw` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.12 | 111.9s | 20.0 |
| `simple-raw` | `gpt-4.1` | 3 | 100.0% | $0.39 | 101.6s | 68.7 |
| `simple-raw` | `gpt-4.1-mini` | 4 | 25.0% | $0.10 | 99.9s | 89.5 |
| `simple-summarization` | `claude-sonnet-4.5` | 4 | 50.0% | $0.58 | 202.9s | 46.5 |
| `simple-summarization` | `google-gemini-2.5-pro` | 1 | 100.0% | $0.16 | 123.4s | 24.0 |
| `simple-summarization` | `gpt-4.1` | 3 | 33.3% | $0.26 | 59.5s | 61.3 |
| `simple-summarization` | `gpt-4.1-mini` | 4 | 50.0% | $0.08 | 108.6s | 63.2 |

---

## Success Rate

![Success Rate](success_rate.png)

- **`intent`** (claude-sonnet-4.5): 4/4 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (gpt-4.1): 3/3 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`intent`** (gpt-4.1-mini): 4/4 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (claude-sonnet-4.5): 4/4 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (gpt-4.1): 3/3 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-raw`** (gpt-4.1-mini): 1/4 successful (25.0%) ![25%](https://img.shields.io/badge/success-25%25-red)
- **`simple-summarization`** (claude-sonnet-4.5): 2/4 successful (50.0%) ![50%](https://img.shields.io/badge/success-50%25-yellow)
- **`simple-summarization`** (google-gemini-2.5-pro): 1/1 successful (100.0%) ![100%](https://img.shields.io/badge/success-100%25-green)
- **`simple-summarization`** (gpt-4.1): 1/3 successful (33.3%) ![33%](https://img.shields.io/badge/success-33%25-red)
- **`simple-summarization`** (gpt-4.1-mini): 2/4 successful (50.0%) ![50%](https://img.shields.io/badge/success-50%25-yellow)

---

## Performance Metrics

### Cost Comparison

![Cost Comparison](cost_comparison.png)

| Agent Type | Model | Average Cost | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | $0.34 | ±$0.04 |
| `intent` | `google-gemini-2.5-pro` | $0.15 | ±$nan |
| `intent` | `gpt-4.1` | $0.32 | ±$0.11 |
| `intent` | `gpt-4.1-mini` | $0.05 | ±$0.01 |
| `simple-raw` | `claude-sonnet-4.5` | $0.92 | ±$0.49 |
| `simple-raw` | `google-gemini-2.5-pro` | $0.12 | ±$nan |
| `simple-raw` | `gpt-4.1` | $0.39 | ±$0.20 |
| `simple-raw` | `gpt-4.1-mini` | $0.10 | ±$nan |
| `simple-summarization` | `claude-sonnet-4.5` | $0.52 | ±$0.20 |
| `simple-summarization` | `google-gemini-2.5-pro` | $0.16 | ±$nan |
| `simple-summarization` | `gpt-4.1` | $0.23 | ±$nan |
| `simple-summarization` | `gpt-4.1-mini` | $0.06 | ±$0.02 |

### Execution Time

![Execution Time](execution_time.png)

| Agent Type | Model | Average Time | Std Dev |
|------------|-------|--------------|----------|
| `intent` | `claude-sonnet-4.5` | 193.5s | ±25.6s |
| `intent` | `google-gemini-2.5-pro` | 196.7s | ±nans |
| `intent` | `gpt-4.1` | 230.2s | ±110.7s |
| `intent` | `gpt-4.1-mini` | 108.4s | ±23.6s |
| `simple-raw` | `claude-sonnet-4.5` | 125.5s | ±33.3s |
| `simple-raw` | `google-gemini-2.5-pro` | 111.9s | ±nans |
| `simple-raw` | `gpt-4.1` | 101.6s | ±25.1s |
| `simple-raw` | `gpt-4.1-mini` | 99.9s | ±19.0s |
| `simple-summarization` | `claude-sonnet-4.5` | 202.9s | ±62.0s |
| `simple-summarization` | `google-gemini-2.5-pro` | 123.4s | ±nans |
| `simple-summarization` | `gpt-4.1` | 59.5s | ±15.1s |
| `simple-summarization` | `gpt-4.1-mini` | 108.6s | ±30.6s |

### Step Count

![Step Count](step_count.png)

| Agent Type | Model | Average Steps | Std Dev |
|------------|-------|---------------|----------|
| `intent` | `claude-sonnet-4.5` | 16.0 | ±0.8 |
| `intent` | `google-gemini-2.5-pro` | 18.0 | ±nan |
| `intent` | `gpt-4.1` | 21.7 | ±8.0 |
| `intent` | `gpt-4.1-mini` | 15.5 | ±3.7 |
| `simple-raw` | `claude-sonnet-4.5` | 46.0 | ±5.9 |
| `simple-raw` | `google-gemini-2.5-pro` | 20.0 | ±nan |
| `simple-raw` | `gpt-4.1` | 68.7 | ±31.1 |
| `simple-raw` | `gpt-4.1-mini` | 89.5 | ±13.7 |
| `simple-summarization` | `claude-sonnet-4.5` | 46.5 | ±7.0 |
| `simple-summarization` | `google-gemini-2.5-pro` | 24.0 | ±nan |
| `simple-summarization` | `gpt-4.1` | 61.3 | ±9.8 |
| `simple-summarization` | `gpt-4.1-mini` | 63.2 | ±6.2 |

### Token Usage

![Token Usage](token_usage.png)

| Agent Type | Model | Input Tokens | Output Tokens | Total Tokens |
|------------|-------|--------------|---------------|-------------|
| `intent` | `claude-sonnet-4.5` | 151892 | 9637 | 161529 |
| `intent` | `google-gemini-2.5-pro` | 96056 | 18008 | 114064 |
| `intent` | `gpt-4.1` | 125661 | 10797 | 136458 |
| `intent` | `gpt-4.1-mini` | 69216 | 7054 | 76269 |
| `simple-raw` | `claude-sonnet-4.5` | 276856 | 5887 | 282742 |
| `simple-raw` | `google-gemini-2.5-pro` | 25278 | 9018 | 34296 |
| `simple-raw` | `gpt-4.1` | 170659 | 6512 | 177171 |
| `simple-raw` | `gpt-4.1-mini` | 222522 | 4203 | 226725 |
| `simple-summarization` | `claude-sonnet-4.5` | 161116 | 6258 | 167374 |
| `simple-summarization` | `google-gemini-2.5-pro` | 32588 | 11767 | 44355 |
| `simple-summarization` | `gpt-4.1` | 118396 | 2295 | 120691 |
| `simple-summarization` | `gpt-4.1-mini` | 187664 | 4066 | 191731 |

### Tokens vs Steps Relationship

![Tokens vs Steps](tokens_vs_steps.png)

### Per-Step Latency

![Per-Step Latency](per_step_latency.png)

| Agent Type | Model | Avg Latency per Step | Std Dev |
|------------|-------|----------------------|----------|
| `intent` | `claude-sonnet-4.5` | 12.06s | ±1.02s |
| `intent` | `google-gemini-2.5-pro` | 10.93s | ±nans |
| `intent` | `gpt-4.1` | 10.46s | ±1.57s |
| `intent` | `gpt-4.1-mini` | 7.41s | ±2.83s |
| `simple-raw` | `claude-sonnet-4.5` | 2.70s | ±0.40s |
| `simple-raw` | `google-gemini-2.5-pro` | 5.59s | ±nans |
| `simple-raw` | `gpt-4.1` | 1.64s | ±0.56s |
| `simple-raw` | `gpt-4.1-mini` | 1.15s | ±0.34s |
| `simple-summarization` | `claude-sonnet-4.5` | 4.27s | ±0.82s |
| `simple-summarization` | `google-gemini-2.5-pro` | 5.14s | ±nans |
| `simple-summarization` | `gpt-4.1` | 1.01s | ±0.43s |
| `simple-summarization` | `gpt-4.1-mini` | 1.74s | ±0.56s |

### Token Processing Throughput

![Tokens per Second](tokens_per_second.png)

| Agent Type | Model | Tokens/Second | Std Dev |
|------------|-------|---------------|----------|
| `intent` | `claude-sonnet-4.5` | 839 | ±48 |
| `intent` | `google-gemini-2.5-pro` | 580 | ±nan |
| `intent` | `gpt-4.1` | 612 | ±122 |
| `intent` | `gpt-4.1-mini` | 733 | ±299 |
| `simple-raw` | `claude-sonnet-4.5` | 2146 | ±699 |
| `simple-raw` | `google-gemini-2.5-pro` | 307 | ±nan |
| `simple-raw` | `gpt-4.1` | 1659 | ±700 |
| `simple-raw` | `gpt-4.1-mini` | 2308 | ±481 |
| `simple-summarization` | `claude-sonnet-4.5` | 835 | ±51 |
| `simple-summarization` | `google-gemini-2.5-pro` | 359 | ±nan |
| `simple-summarization` | `gpt-4.1` | 2161 | ±777 |
| `simple-summarization` | `gpt-4.1-mini` | 2033 | ±1744 |

### Latency vs Token Usage

![Latency vs Tokens](latency_vs_tokens.png)

This scatter plot shows the relationship between tokens per step and latency per step, helping identify efficiency patterns across different agent configurations.

### Token Growth Scaling Analysis

![Token Growth Regression](token_growth_regression.png)

Polynomial regression (degree 2-3) showing how **tokens per step** changes as total steps increase. This reveals whether agents become more/less efficient with more steps. Curves are color-coded: 🟢 **green** = improving efficiency, 🔴 **red** = degrading efficiency, 🔵 **blue** = stable. Solid curves show fitted trend, dotted lines extrapolate beyond observed data (constrained to positive values).

#### Model Fit Parameters

| Agent Type | Model | Degree | R² | Equation |
|------------|-------|--------|-----|----------|
| `intent` | `claude-sonnet-4.5` | 2 | 0.926 | `772x^2 - 24583x + 205490` |
| `intent` | `gpt-4.1` | 2 | 1.000 | `-7.82x^2 + 359x + 2511` |
| `intent` | `gpt-4.1-mini` | 3 | 1.000 | `1.89x^3 + 49.42x^2 - 2866x + 29081` |
| `simple-raw` | `claude-sonnet-4.5` | 3 | 1.000 | `-37.63x^3 + 5291x^2 - 245836x + 3782527` |
| `simple-raw` | `gpt-4.1` | 2 | 1.000 | `-0.38x^2 + 60.12x + 360` |
| `simple-raw` | `gpt-4.1-mini` | 2 | 0.515 | `4.50x^2 - 814x + 38675` |
| `simple-summarization` | `claude-sonnet-4.5` | 2 | 0.998 | `0.57x^2 + 25.75x + 1098` |
| `simple-summarization` | `gpt-4.1` | 2 | 0.744 | `-0.16x^2 + 9.48x + 2009` |
| `simple-summarization` | `gpt-4.1-mini` | 3 | 1.000 | `-33.27x^3 + 6202x^2 - 383819x + 7888651` |

**Interpretation:**
- **Degree**: Polynomial degree (2 or 3) selected for best fit
- **R²**: Goodness of fit (higher = better, 1.0 = perfect fit)
- **Equation**: Polynomial function describing tokens/step as function of total steps (x)

#### Efficiency Rankings

Ranked by efficiency change from 50 to 100 steps (negative = improving, positive = degrading):

🥇 **`simple-raw`** (claude-sonnet-4.5): 🟢 -41535.5% (improving)  
🥈 **`intent`** (gpt-4.1): 🟢 -4589.9% (improving)  
🥉 **`simple-summarization`** (gpt-4.1-mini): 🟢 -4162.4% (improving)  
4. **`simple-raw`** (gpt-4.1-mini): 🟢 -74.6% (improving)  
5. **`simple-summarization`** (gpt-4.1): 🟢 -35.0% (improving)  
6. **`simple-raw`** (gpt-4.1): 🔴 +6.8% (degrading)  
7. **`simple-summarization`** (claude-sonnet-4.5): 🔴 +145.6% (degrading)  
8. **`intent`** (claude-sonnet-4.5): 🔴 +503.4% (degrading)  
9. **`intent`** (gpt-4.1-mini): 🔴 +765.9% (degrading)  

#### Predicted Tokens per Step at Different Scales

| Agent Type | Model | @ 50 steps | @ 100 steps | @ 200 steps | @ 500 steps |
|------------|-------|------------|-------------|-------------|-------------|
| `intent` | `claude-sonnet-4.5` | 905,480 | 5,463,751 | 26,155,132 | 180,827,997 |
| `intent` | `gpt-4.1` | 887 | 0 | 0 | 0 |
| `intent` | `gpt-4.1-mini` | 245,574 | 2,126,527 | 16,551,168 | 247,175,484 |
| `simple-raw` | `claude-sonnet-4.5` | 13,340 | 0 | 0 | 0 |
| `simple-raw` | `gpt-4.1` | 2,419 | 2,584 | 0 | 0 |
| `simple-raw` | `gpt-4.1-mini` | 9,249 | 2,345 | 56,100 | 757,881 |
| `simple-summarization` | `claude-sonnet-4.5` | 3,801 | 9,337 | 28,905 | 155,588 |
| `simple-summarization` | `gpt-4.1` | 2,082 | 1,354 | 0 | 0 |
| `simple-summarization` | `gpt-4.1-mini` | 42,997 | 0 | 0 | 0 |

#### Predicted Total Token Usage at Different Scales

| Agent Type | Model | @ 50 steps | @ 100 steps | @ 200 steps | @ 500 steps |
|------------|-------|------------|-------------|-------------|-------------|
| `intent` | `claude-sonnet-4.5` | 45,274,037 | 546,375,138 | 5,231,026,540 | 90,413,998,631 |
| `intent` | `gpt-4.1` | 44,380 | 0 | 0 | 0 |
| `intent` | `gpt-4.1-mini` | 12,278,735 | 212,652,708 | 3,310,233,736 | 123,587,742,226 |
| `simple-raw` | `claude-sonnet-4.5` | 667,012 | 0 | 0 | 0 |
| `simple-raw` | `gpt-4.1` | 120,971 | 258,488 | 0 | 0 |
| `simple-raw` | `gpt-4.1-mini` | 462,485 | 234,533 | 11,220,173 | 378,940,833 |
| `simple-summarization` | `claude-sonnet-4.5` | 190,060 | 933,707 | 5,781,175 | 77,794,419 |
| `simple-summarization` | `gpt-4.1` | 104,126 | 135,465 | 0 | 0 |
| `simple-summarization` | `gpt-4.1-mini` | 2,149,877 | 0 | 0 | 0 |

### Accuracy Score

![Accuracy Score](accuracy_score.png)

| Agent Type | Model | Average Accuracy | Std Dev |
|------------|-------|------------------|----------|
| `intent` | `claude-sonnet-4.5` | 70.83% | ±15.96% |
| `intent` | `google-gemini-2.5-pro` | 83.33% | ±nan% |
| `intent` | `gpt-4.1` | 38.89% | ±38.49% |
| `intent` | `gpt-4.1-mini` | 62.50% | ±34.36% |
| `simple-raw` | `claude-sonnet-4.5` | 83.33% | ±13.61% |
| `simple-raw` | `google-gemini-2.5-pro` | 66.67% | ±nan% |
| `simple-raw` | `gpt-4.1` | 44.44% | ±41.94% |
| `simple-raw` | `gpt-4.1-mini` | 33.33% | ±nan% |
| `simple-summarization` | `claude-sonnet-4.5` | 75.00% | ±11.79% |
| `simple-summarization` | `google-gemini-2.5-pro` | 66.67% | ±nan% |
| `simple-summarization` | `gpt-4.1` | 50.00% | ±nan% |
| `simple-summarization` | `gpt-4.1-mini` | 25.00% | ±11.79% |

### Field-Level Accuracy Analysis

#### Field Accuracy Heatmap

![Field Accuracy Heatmap](field_accuracy_heatmap.png)

#### Proximity Score Heatmap

![Field Proximity Heatmap](field_proximity_heatmap.png)

#### Field Accuracy Rates

| Field | intent (claude-sonnet-4.5) | intent (google-gemini-2.5-pro) | intent (gpt-4.1) | intent (gpt-4.1-mini) | simple-raw (claude-sonnet-4.5) | simple-raw (google-gemini-2.5-pro) | simple-raw (gpt-4.1) | simple-raw (gpt-4.1-mini) | simple-summarization (claude-sonnet-4.5) | simple-summarization (google-gemini-2.5-pro) | simple-summarization (gpt-4.1) | simple-summarization (gpt-4.1-mini) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 0% | 100% | 33% | 50% | 25% | 0% | 33% | 0% | 0% | 0% | 0% | 0% |
| `best_revenue_hour` | 75% | 100% | 33% | 100% | 100% | 100% | 67% | 0% | 100% | 100% | 100% | 50% |
| `best_revenue_zone` | 75% | 100% | 100% | 75% | 100% | 100% | 67% | 100% | 100% | 100% | 100% | 100% |
| `optimal_distance_bracket` | 100% | 0% | 0% | 50% | 75% | 0% | 33% | 100% | 50% | 0% | 100% | 0% |
| `trips_above_max_distance` | 100% | 100% | 33% | 50% | 100% | 100% | 33% | 0% | 100% | 100% | 0% | 0% |
| `trips_below_min_fare` | 75% | 100% | 33% | 50% | 100% | 100% | 33% | 0% | 100% | 100% | 0% | 0% |

#### Percentage Error (Numeric Fields)

![Percentage Error](field_percentage_error.png)

| Field | intent (claude-sonnet-4.5) | intent (google-gemini-2.5-pro) | intent (gpt-4.1) | intent (gpt-4.1-mini) | simple-raw (claude-sonnet-4.5) | simple-raw (google-gemini-2.5-pro) | simple-raw (gpt-4.1) | simple-raw (gpt-4.1-mini) | simple-summarization (claude-sonnet-4.5) | simple-summarization (google-gemini-2.5-pro) | simple-summarization (gpt-4.1) | simple-summarization (gpt-4.1-mini) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `avg_revenue_per_trip` | 40.1% | 0.0% | 4.4% | 4.0% | 32.8% | 39.7% | 17.2% | 8.0% | 43.7% | 43.7% | 8.0% | 35.1% |
| `best_revenue_hour` | 1.5% | 0.0% | 3.9% | 0.0% | 0.0% | 0.0% | 2.0% | 5.9% | 0.0% | 0.0% | 0.0% | 2.9% |
| `trips_above_max_distance` | 0.0% | 0.0% | 58.4% | 46.4% | 0.0% | 0.0% | 35.9% | 92.7% | 0.0% | 0.0% | 92.7% | 84.0% |
| `trips_below_min_fare` | 13.8% | 0.0% | 58.3% | 46.6% | 0.0% | 0.0% | 63.2% | 93.2% | 0.0% | 0.0% | 93.2% | 90.6% |

---

## Detailed Analysis

### `intent` (anthropic-claude-sonnet-4.5)

![Runs](https://img.shields.io/badge/runs-12-blue) ![Success](https://img.shields.io/badge/success-12-green) 

**Performance (Successful Runs Only):**

- **Average Steps:** 17.4
- **Average Cost:** $0.22
- **Average Time:** 174.6s
- **Average Tokens:** 122886
- **Tokens per Step:** 7115
- **Cost per Step:** $0.0124
- **Time per Step:** 10.01s
- **Average Accuracy:** 61.11%

### `simple-raw` (anthropic-claude-sonnet-4.5)

![Runs](https://img.shields.io/badge/runs-12-blue) ![Success](https://img.shields.io/badge/success-9-green) ![Failed](https://img.shields.io/badge/failed-3-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 53.8
- **Average Cost:** $0.56
- **Average Time:** 114.4s
- **Average Tokens:** 214225
- **Tokens per Step:** 4008
- **Cost per Step:** $0.0113
- **Time per Step:** 2.54s
- **Average Accuracy:** 62.96%

**Note:** This agent had failed runs. Check detailed metrics for more information.

### `simple-summarization` (anthropic-claude-sonnet-4.5)

![Runs](https://img.shields.io/badge/runs-12-blue) ![Success](https://img.shields.io/badge/success-6-green) ![Failed](https://img.shields.io/badge/failed-6-red)

**Performance (Successful Runs Only):**

- **Average Steps:** 46.2
- **Average Cost:** $0.26
- **Average Time:** 136.3s
- **Average Tokens:** 120891
- **Tokens per Step:** 2583
- **Cost per Step:** $0.0062
- **Time per Step:** 3.19s
- **Average Accuracy:** 52.78%

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
9. **`simple-summarization`** (claude-sonnet-4.5): 50.0%  
10. **`simple-summarization`** (gpt-4.1-mini): 50.0%  
11. **`simple-summarization`** (gpt-4.1): 33.3%  
12. **`simple-raw`** (gpt-4.1-mini): 25.0%  

#### Cost Efficiency (Lower is Better)

🥇 **`intent`** (gpt-4.1-mini): $0.05  
🥈 **`simple-summarization`** (gpt-4.1-mini): $0.06  
🥉 **`simple-raw`** (gpt-4.1-mini): $0.10  
4. **`simple-raw`** (google-gemini-2.5-pro): $0.12  
5. **`intent`** (google-gemini-2.5-pro): $0.15  
6. **`simple-summarization`** (google-gemini-2.5-pro): $0.16  
7. **`simple-summarization`** (gpt-4.1): $0.23  
8. **`intent`** (gpt-4.1): $0.32  
9. **`intent`** (claude-sonnet-4.5): $0.34  
10. **`simple-raw`** (gpt-4.1): $0.39  
11. **`simple-summarization`** (claude-sonnet-4.5): $0.52  
12. **`simple-raw`** (claude-sonnet-4.5): $0.92  

#### Speed (Lower is Better)

🥇 **`simple-summarization`** (gpt-4.1): 75.1s  
🥈 **`simple-raw`** (gpt-4.1): 101.6s  
🥉 **`intent`** (gpt-4.1-mini): 108.4s  
4. **`simple-raw`** (gpt-4.1-mini): 111.3s  
5. **`simple-raw`** (google-gemini-2.5-pro): 111.9s  
6. **`simple-summarization`** (google-gemini-2.5-pro): 123.4s  
7. **`simple-raw`** (claude-sonnet-4.5): 125.5s  
8. **`simple-summarization`** (gpt-4.1-mini): 129.1s  
9. **`simple-summarization`** (claude-sonnet-4.5): 180.5s  
10. **`intent`** (claude-sonnet-4.5): 193.5s  
11. **`intent`** (google-gemini-2.5-pro): 196.7s  
12. **`intent`** (gpt-4.1): 230.2s  

#### Accuracy (Higher is Better)

🥇 **`intent`** (google-gemini-2.5-pro): 83.33%  
🥈 **`simple-raw`** (claude-sonnet-4.5): 83.33%  
🥉 **`simple-summarization`** (claude-sonnet-4.5): 75.00%  
4. **`intent`** (claude-sonnet-4.5): 70.83%  
5. **`simple-raw`** (google-gemini-2.5-pro): 66.67%  
6. **`simple-summarization`** (google-gemini-2.5-pro): 66.67%  
7. **`intent`** (gpt-4.1-mini): 62.50%  
8. **`simple-summarization`** (gpt-4.1): 50.00%  
9. **`simple-raw`** (gpt-4.1): 44.44%  
10. **`intent`** (gpt-4.1): 38.89%  
11. **`simple-raw`** (gpt-4.1-mini): 33.33%  
12. **`simple-summarization`** (gpt-4.1-mini): 25.00%  

---

## Recommendations

### Best Agent for Different Use Cases

- **💰 Most Cost-Efficient:** `intent` (gpt-4.1-mini) - $0.05 per run
- **⚡ Fastest:** `simple-summarization` (gpt-4.1) - 75.1s per run
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

*Report generated on 2025-11-07 18:04:56*
