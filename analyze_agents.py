"""
Agent Performance Analysis Script

Analyzes agent outputs from the outputs/ directory and generates:
- Visualizations (PNG images)
- CSV files with metrics
- Markdown summary report
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Source of truth for accuracy comparison
GROUND_TRUTH = {
    "best_revenue_zone": "Zone 132",
    "best_revenue_hour": 17,
    "avg_revenue_per_trip": 19.94,
    "optimal_distance_bracket": "10+mi",
    "trips_below_min_fare": 2176876,
    "trips_above_max_distance": 2221
}

@dataclass
class AgentRun:
    """Represents a single agent run with all metrics"""
    run_id: str
    agent_type: str
    model_name: str

    # Performance metrics
    total_messages: int
    total_time_seconds: float
    total_cost: float

    # Token metrics
    total_tokens: int
    input_tokens: int
    output_tokens: int

    # Derived metrics
    avg_tokens_per_step: float
    avg_time_per_step: float
    cost_per_step: float

    # Success and accuracy
    is_success: bool
    metrics: Dict[str, Any]
    accuracy_score: float = 0.0

    @classmethod
    def from_json(cls, filepath: Path, agent_type: str) -> 'AgentRun':
        """Load agent run data from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Extract model name from filename
        model_name = filepath.stem.replace(f"-{agent_type}", "")

        # Get token data for the primary model
        tokens_data = data.get('tokens', {})
        primary_model = list(tokens_data.keys())[0] if tokens_data else None

        if primary_model:
            token_info = tokens_data[primary_model]
            total_tokens = token_info.get('total_tokens', 0)
            input_tokens = token_info.get('input_tokens', 0)
            output_tokens = token_info.get('output_tokens', 0)
        else:
            total_tokens = input_tokens = output_tokens = 0

        # Get cost data
        costs_data = data.get('costs', {})
        total_cost = 0.0
        if primary_model and primary_model in costs_data:
            total_cost = costs_data[primary_model].get('total_cost', 0.0)

        # Get metrics and check if successful
        metrics = data.get('metrics', {})
        is_success = bool(metrics)  # Empty dict = failure

        # Calculate accuracy if successful
        accuracy_score = 0.0
        if is_success:
            accuracy_score = calculate_accuracy(metrics, GROUND_TRUTH)

        total_messages = data.get('total_messages', 0)
        total_time = data.get('total_time_seconds', 0.0)

        # Calculate derived metrics
        avg_tokens_per_step = total_tokens / total_messages if total_messages > 0 else 0
        avg_time_per_step = total_time / total_messages if total_messages > 0 else 0
        cost_per_step = total_cost / total_messages if total_messages > 0 else 0

        return cls(
            run_id=data.get('run_id', 'unknown'),
            agent_type=agent_type,
            model_name=model_name,
            total_messages=total_messages,
            total_time_seconds=total_time,
            total_cost=total_cost,
            total_tokens=total_tokens,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            avg_tokens_per_step=avg_tokens_per_step,
            avg_time_per_step=avg_time_per_step,
            cost_per_step=cost_per_step,
            is_success=is_success,
            metrics=metrics,
            accuracy_score=accuracy_score
        )


def calculate_accuracy(metrics: Dict[str, Any], ground_truth: Dict[str, Any]) -> float:
    """
    Calculate accuracy score by comparing metrics to ground truth.
    Returns a score between 0.0 and 1.0
    """
    if not metrics:
        return 0.0

    total_fields = len(ground_truth)
    correct_fields = 0

    for key, true_value in ground_truth.items():
        if key not in metrics:
            continue

        pred_value = metrics[key]

        # For numeric values, allow small tolerance
        if isinstance(true_value, (int, float)):
            # Allow 5% tolerance for numeric values
            tolerance = abs(true_value * 0.05) if true_value != 0 else 0.01
            if abs(pred_value - true_value) <= tolerance:
                correct_fields += 1
        else:
            # Exact match for strings
            if pred_value == true_value:
                correct_fields += 1

    return correct_fields / total_fields


def calculate_field_accuracy(pred_value: Any, true_value: Any) -> Dict[str, Any]:
    """
    Calculate detailed accuracy metrics for a single field.
    Returns dict with is_correct, error, and proximity score.
    """
    result = {
        'is_correct': False,
        'error': None,
        'proximity_score': 0.0,
        'percentage_error': None
    }

    if pred_value is None:
        return result

    if isinstance(true_value, (int, float)):
        # Numeric field
        error = pred_value - true_value
        percentage_error = (abs(error) / abs(true_value) * 100) if true_value != 0 else 0.0

        result['error'] = error
        result['percentage_error'] = percentage_error

        # Proximity score: 1.0 for exact match, decreases with error
        # 0.95+ for <5% error, 0.0 for >50% error
        if percentage_error == 0:
            result['proximity_score'] = 1.0
        elif percentage_error <= 5:
            result['proximity_score'] = 1.0 - (percentage_error / 100)
        elif percentage_error <= 50:
            result['proximity_score'] = max(0, 1.0 - (percentage_error / 50))
        else:
            result['proximity_score'] = 0.0

        # Tolerance check (5%)
        tolerance = abs(true_value * 0.05) if true_value != 0 else 0.01
        result['is_correct'] = abs(error) <= tolerance
    else:
        # String field
        result['is_correct'] = pred_value == true_value
        result['proximity_score'] = 1.0 if result['is_correct'] else 0.0

    return result


def load_all_runs(outputs_dir: str = "outputs") -> List[AgentRun]:
    """Load all agent runs from the outputs directory"""
    runs = []
    outputs_path = Path(outputs_dir)

    if not outputs_path.exists():
        print(f"Error: {outputs_dir} directory not found")
        return runs

    # Iterate through run directories
    for run_dir in outputs_path.iterdir():
        if not run_dir.is_dir():
            continue

        # Look for different agent type files
        agent_types = {
            'simple-raw': 'simple-raw',
            'simple-summarization': 'simple-summarization',
            'intent': 'intent'
        }

        for agent_type, suffix in agent_types.items():
            # Find matching files
            matching_files = list(run_dir.glob(f"*-{suffix}.json"))

            for filepath in matching_files:
                try:
                    run = AgentRun.from_json(filepath, agent_type)
                    runs.append(run)
                    print(f"Loaded: {run.agent_type} from {run.run_id}")
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")

    return runs


def generate_visualizations(runs: List[AgentRun], output_dir: str = "analysis_output"):
    """Generate all visualization charts"""
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame([asdict(run) for run in runs])

    # Create a combined column for agent + model
    df['agent_model'] = df['agent_type'] + '\n(' + df['model_name'].str.replace('anthropic-', '').str.replace('openai-', '') + ')'

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 7)

    # Color palette for models
    model_colors = {
        'anthropic-claude-sonnet-4.5': '#5D4E87',
        'openai-gpt-4.1-mini': '#10A37F'
    }

    # 1. Success Rate by Agent Type and Model
    plt.figure(figsize=(14, 7))
    success_data = df.groupby(['agent_type', 'model_name'])['is_success'].agg(['sum', 'count']).reset_index()
    success_data['rate'] = (success_data['sum'] / success_data['count']) * 100

    # Create grouped bar chart
    agent_types = sorted(df['agent_type'].unique())
    models = sorted(df['model_name'].unique())
    x = np.arange(len(agent_types))
    width = 0.35

    fig, ax = plt.subplots(figsize=(14, 7))

    for i, model in enumerate(models):
        model_data = success_data[success_data['model_name'] == model]
        rates = [model_data[model_data['agent_type'] == agent]['rate'].values[0]
                if len(model_data[model_data['agent_type'] == agent]) > 0 else 0
                for agent in agent_types]

        offset = width * (i - len(models)/2 + 0.5)
        bars = ax.bar(x + offset, rates, width, label=model.replace('anthropic-', '').replace('openai-', ''),
                     color=model_colors.get(model, 'steelblue'))

        # Add value labels
        for j, (bar, rate) in enumerate(zip(bars, rates)):
            if rate > 0:
                ax.text(bar.get_x() + bar.get_width()/2, rate + 2, f'{rate:.0f}%',
                       ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Agent Type', fontsize=12)
    ax.set_ylabel('Success Rate (%)', fontsize=12)
    ax.set_title('Success Rate by Agent Type and Model', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(agent_types, rotation=45, ha='right')
    ax.set_ylim(0, 110)
    ax.legend(title='Model')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/success_rate.png", dpi=300)
    plt.close()

    # 2. Cost Comparison
    successful_runs = df[df['is_success'] == True]

    if not successful_runs.empty:
        fig, ax = plt.subplots(figsize=(14, 7))
        cost_data = successful_runs.groupby(['agent_type', 'model_name'])['total_cost'].mean().reset_index()

        for i, model in enumerate(models):
            model_data = cost_data[cost_data['model_name'] == model]
            costs = [model_data[model_data['agent_type'] == agent]['total_cost'].values[0]
                    if len(model_data[model_data['agent_type'] == agent]) > 0 else 0
                    for agent in agent_types]

            offset = width * (i - len(models)/2 + 0.5)
            bars = ax.bar(x + offset, costs, width, label=model.replace('anthropic-', '').replace('openai-', ''),
                         color=model_colors.get(model, 'coral'))

            # Add value labels
            for bar, cost in zip(bars, costs):
                if cost > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, cost, f'${cost:.2f}',
                           ha='center', va='bottom', fontsize=9)

        ax.set_xlabel('Agent Type', fontsize=12)
        ax.set_ylabel('Cost ($)', fontsize=12)
        ax.set_title('Average Total Cost by Agent Type and Model (Successful Runs Only)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(agent_types, rotation=45, ha='right')
        ax.legend(title='Model')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/cost_comparison.png", dpi=300)
        plt.close()

    # 3. Step Count Comparison
    fig, ax = plt.subplots(figsize=(14, 7))
    step_data = df.groupby(['agent_type', 'model_name'])['total_messages'].mean().reset_index()

    for i, model in enumerate(models):
        model_data = step_data[step_data['model_name'] == model]
        steps = [model_data[model_data['agent_type'] == agent]['total_messages'].values[0]
                if len(model_data[model_data['agent_type'] == agent]) > 0 else 0
                for agent in agent_types]

        offset = width * (i - len(models)/2 + 0.5)
        bars = ax.bar(x + offset, steps, width, label=model.replace('anthropic-', '').replace('openai-', ''),
                     color=model_colors.get(model, 'seagreen'))

        # Add value labels
        for bar, step in zip(bars, steps):
            if step > 0:
                ax.text(bar.get_x() + bar.get_width()/2, step, f'{step:.0f}',
                       ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Agent Type', fontsize=12)
    ax.set_ylabel('Number of Steps', fontsize=12)
    ax.set_title('Average Number of Steps by Agent Type and Model', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(agent_types, rotation=45, ha='right')
    ax.legend(title='Model')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/step_count.png", dpi=300)
    plt.close()

    # 4. Token Usage Breakdown (Grouped Stacked Bar)
    fig, ax = plt.subplots(figsize=(14, 7))

    for i, model in enumerate(models):
        model_df = df[df['model_name'] == model]
        token_data = model_df.groupby('agent_type')[['input_tokens', 'output_tokens']].mean()

        offset = width * (i - len(models)/2 + 0.5)

        # Plot stacked bars for this model
        bottom = np.zeros(len(agent_types))
        for j, token_type in enumerate(['input_tokens', 'output_tokens']):
            values = [token_data.loc[agent, token_type] if agent in token_data.index else 0
                     for agent in agent_types]

            color_base = model_colors.get(model, 'steelblue')
            # Make output tokens slightly lighter
            alpha_val = 0.5 if token_type == 'output_tokens' else 1.0

            ax.bar(x + offset, values, width, bottom=bottom,
                  label=f'{model.replace("anthropic-", "").replace("openai-", "")} - {token_type.replace("_", " ").title()}',
                  color=color_base, alpha=alpha_val)
            bottom += values

    ax.set_xlabel('Agent Type', fontsize=12)
    ax.set_ylabel('Tokens', fontsize=12)
    ax.set_title('Average Token Usage by Agent Type and Model', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(agent_types, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/token_usage.png", dpi=300)
    plt.close()

    # 5. Speed/Time Comparison
    fig, ax = plt.subplots(figsize=(14, 7))
    time_data = df.groupby(['agent_type', 'model_name'])['total_time_seconds'].mean().reset_index()

    for i, model in enumerate(models):
        model_data = time_data[time_data['model_name'] == model]
        times = [model_data[model_data['agent_type'] == agent]['total_time_seconds'].values[0]
                if len(model_data[model_data['agent_type'] == agent]) > 0 else 0
                for agent in agent_types]

        offset = width * (i - len(models)/2 + 0.5)
        bars = ax.bar(x + offset, times, width, label=model.replace('anthropic-', '').replace('openai-', ''),
                     color=model_colors.get(model, 'mediumpurple'))

        # Add value labels
        for bar, time in zip(bars, times):
            if time > 0:
                ax.text(bar.get_x() + bar.get_width()/2, time, f'{time:.0f}s',
                       ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Agent Type', fontsize=12)
    ax.set_ylabel('Time (seconds)', fontsize=12)
    ax.set_title('Average Execution Time by Agent Type and Model', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(agent_types, rotation=45, ha='right')
    ax.legend(title='Model')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/execution_time.png", dpi=300)
    plt.close()

    # 6. Tokens per Step Scatter Plot
    fig, ax = plt.subplots(figsize=(12, 7))

    # Different markers for models, different colors for agent types
    markers = {'anthropic-claude-sonnet-4.5': 'o', 'openai-gpt-4.1-mini': 's'}
    agent_colors = {
        'intent': '#E74C3C',
        'simple-raw': '#3498DB',
        'simple-summarization': '#2ECC71'
    }

    for agent_type in agent_types:
        for model in models:
            agent_model_data = df[(df['agent_type'] == agent_type) & (df['model_name'] == model)]
            if not agent_model_data.empty:
                model_short = model.replace("anthropic-", "").replace("openai-", "")
                plt.scatter(agent_model_data['total_messages'], agent_model_data['total_tokens'],
                           label=f'{agent_type} ({model_short})',
                           alpha=0.7, s=150,
                           marker=markers.get(model, 'o'),
                           color=agent_colors.get(agent_type, 'steelblue'),
                           edgecolors='black', linewidths=1.5)

    plt.title('Total Tokens vs Number of Steps', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Steps', fontsize=12)
    plt.ylabel('Total Tokens', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/tokens_vs_steps.png", dpi=300)
    plt.close()

    # 7. Per-Step Latency Comparison
    fig, ax = plt.subplots(figsize=(14, 7))
    latency_data = df.groupby(['agent_type', 'model_name'])['avg_time_per_step'].mean().reset_index()

    for i, model in enumerate(models):
        model_data = latency_data[latency_data['model_name'] == model]
        latencies = [model_data[model_data['agent_type'] == agent]['avg_time_per_step'].values[0]
                    if len(model_data[model_data['agent_type'] == agent]) > 0 else 0
                    for agent in agent_types]

        offset = width * (i - len(models)/2 + 0.5)
        bars = ax.bar(x + offset, latencies, width, label=model.replace('anthropic-', '').replace('openai-', ''),
                     color=model_colors.get(model, 'orange'))

        # Add value labels
        for bar, lat in zip(bars, latencies):
            if lat > 0:
                ax.text(bar.get_x() + bar.get_width()/2, lat, f'{lat:.2f}s',
                       ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Agent Type', fontsize=12)
    ax.set_ylabel('Average Time per Step (seconds)', fontsize=12)
    ax.set_title('Per-Step Latency by Agent Type and Model', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(agent_types, rotation=45, ha='right')
    ax.legend(title='Model')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/per_step_latency.png", dpi=300)
    plt.close()

    # 8. Throughput: Tokens per Second
    df['tokens_per_second'] = df['total_tokens'] / df['total_time_seconds']

    fig, ax = plt.subplots(figsize=(14, 7))
    throughput_data = df.groupby(['agent_type', 'model_name'])['tokens_per_second'].mean().reset_index()

    for i, model in enumerate(models):
        model_data = throughput_data[throughput_data['model_name'] == model]
        throughputs = [model_data[model_data['agent_type'] == agent]['tokens_per_second'].values[0]
                      if len(model_data[model_data['agent_type'] == agent]) > 0 else 0
                      for agent in agent_types]

        offset = width * (i - len(models)/2 + 0.5)
        bars = ax.bar(x + offset, throughputs, width, label=model.replace('anthropic-', '').replace('openai-', ''),
                     color=model_colors.get(model, 'teal'))

        # Add value labels
        for bar, thr in zip(bars, throughputs):
            if thr > 0:
                ax.text(bar.get_x() + bar.get_width()/2, thr, f'{thr:.0f}',
                       ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Agent Type', fontsize=12)
    ax.set_ylabel('Tokens per Second', fontsize=12)
    ax.set_title('Token Processing Throughput by Agent Type and Model', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(agent_types, rotation=45, ha='right')
    ax.legend(title='Model')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/tokens_per_second.png", dpi=300)
    plt.close()

    # 9. Latency vs Token Usage scatter
    fig, ax = plt.subplots(figsize=(12, 7))

    for agent_type in agent_types:
        for model in models:
            agent_model_data = df[(df['agent_type'] == agent_type) & (df['model_name'] == model)]
            if not agent_model_data.empty:
                model_short = model.replace("anthropic-", "").replace("openai-", "")
                plt.scatter(agent_model_data['avg_tokens_per_step'], agent_model_data['avg_time_per_step'],
                           label=f'{agent_type} ({model_short})',
                           alpha=0.7, s=150,
                           marker=markers.get(model, 'o'),
                           color=agent_colors.get(agent_type, 'steelblue'),
                           edgecolors='black', linewidths=1.5)

    plt.title('Per-Step Latency vs Tokens per Step', fontsize=14, fontweight='bold')
    plt.xlabel('Average Tokens per Step', fontsize=12)
    plt.ylabel('Average Time per Step (seconds)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/latency_vs_tokens.png", dpi=300)
    plt.close()

    # 10. Accuracy Score (for successful runs)
    if not successful_runs.empty and successful_runs['accuracy_score'].sum() > 0:
        fig, ax = plt.subplots(figsize=(14, 7))
        accuracy_data = successful_runs.groupby(['agent_type', 'model_name'])['accuracy_score'].mean().reset_index()

        for i, model in enumerate(models):
            model_data = accuracy_data[accuracy_data['model_name'] == model]
            scores = [model_data[model_data['agent_type'] == agent]['accuracy_score'].values[0]
                     if len(model_data[model_data['agent_type'] == agent]) > 0 else 0
                     for agent in agent_types]

            offset = width * (i - len(models)/2 + 0.5)
            bars = ax.bar(x + offset, scores, width, label=model.replace('anthropic-', '').replace('openai-', ''),
                         color=model_colors.get(model, 'green'))

            # Add value labels
            for bar, score in zip(bars, scores):
                if score > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, score + 0.02, f'{score:.1%}',
                           ha='center', va='bottom', fontsize=9)

        ax.set_xlabel('Agent Type', fontsize=12)
        ax.set_ylabel('Accuracy Score', fontsize=12)
        ax.set_title('Average Accuracy Score by Agent Type and Model (Successful Runs)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(agent_types, rotation=45, ha='right')
        ax.set_ylim(0, 1.1)
        ax.legend(title='Model')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/accuracy_score.png", dpi=300)
        plt.close()

    # 8. Field-level accuracy analysis
    accuracy_records = []
    for run in runs:
        if not run.is_success:
            continue

        for key, true_value in GROUND_TRUTH.items():
            pred_value = run.metrics.get(key, None)
            field_metrics = calculate_field_accuracy(pred_value, true_value)

            accuracy_records.append({
                'agent_type': run.agent_type,
                'model_name': run.model_name,
                'agent_model': f"{run.agent_type}\n({run.model_name.replace('anthropic-', '').replace('openai-', '')})",
                'field': key,
                'is_correct': field_metrics['is_correct'],
                'proximity_score': field_metrics['proximity_score'],
                'percentage_error': field_metrics['percentage_error']
            })

    if accuracy_records:
        acc_df = pd.DataFrame(accuracy_records)

        # 8a. Field-level accuracy heatmap
        plt.figure(figsize=(14, 8))
        pivot_correct = acc_df.pivot_table(
            values='is_correct',
            index='field',
            columns='agent_model',
            aggfunc='mean'
        )

        sns.heatmap(pivot_correct, annot=True, fmt='.0%', cmap='RdYlGn',
                   vmin=0, vmax=1, cbar_kws={'label': 'Accuracy Rate'},
                   linewidths=0.5, linecolor='gray')
        plt.title('Field-Level Accuracy by Agent Type and Model', fontsize=14, fontweight='bold')
        plt.xlabel('Agent Type (Model)', fontsize=12)
        plt.ylabel('Field', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/field_accuracy_heatmap.png", dpi=300)
        plt.close()

        # 8b. Proximity score heatmap
        plt.figure(figsize=(14, 8))
        pivot_proximity = acc_df.pivot_table(
            values='proximity_score',
            index='field',
            columns='agent_model',
            aggfunc='mean'
        )

        sns.heatmap(pivot_proximity, annot=True, fmt='.2f', cmap='viridis',
                   vmin=0, vmax=1, cbar_kws={'label': 'Proximity Score'},
                   linewidths=0.5, linecolor='gray')
        plt.title('Field-Level Proximity Score by Agent Type and Model', fontsize=14, fontweight='bold')
        plt.xlabel('Agent Type (Model)', fontsize=12)
        plt.ylabel('Field', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/field_proximity_heatmap.png", dpi=300)
        plt.close()

        # 8c. Percentage error for numeric fields
        numeric_errors = acc_df[acc_df['percentage_error'].notna()]
        if not numeric_errors.empty:
            fig, ax = plt.subplots(figsize=(14, 7))
            pivot_error = numeric_errors.pivot_table(
                values='percentage_error',
                index='field',
                columns='agent_model',
                aggfunc='mean'
            )

            # Create grouped bar chart
            pivot_error.plot(kind='bar', width=0.8, ax=ax)
            ax.set_title('Average Percentage Error by Field (Numeric Fields Only)',
                     fontsize=14, fontweight='bold')
            ax.set_xlabel('Field', fontsize=12)
            ax.set_ylabel('Average % Error', fontsize=12)
            ax.legend(title='Agent Type (Model)', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            ax.axhline(y=5, color='r', linestyle='--', alpha=0.5, label='5% threshold')
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/field_percentage_error.png", dpi=300)
            plt.close()

    # 11. Token Growth Regression Analysis
    # Calculate regression for each agent_type and model combination
    regression_data = []

    fig, axes = plt.subplots(len(agent_types), len(models), figsize=(18, 5 * len(agent_types)), squeeze=False)

    for row_idx, agent_type in enumerate(agent_types):
        for col_idx, model in enumerate(models):
            ax = axes[row_idx, col_idx]
            agent_model_data = df[(df['agent_type'] == agent_type) & (df['model_name'] == model)]

            if not agent_model_data.empty and len(agent_model_data) >= 2:
                steps = agent_model_data['total_messages'].values
                tokens = agent_model_data['total_tokens'].values

                # Calculate linear regression
                slope, intercept, r_value, p_value, std_err = stats.linregress(steps, tokens)
                r_squared = r_value ** 2

                # Store regression data (only if not NaN)
                if not np.isnan(slope):
                    regression_data.append({
                        'agent_type': agent_type,
                        'model_name': model,
                        'slope': slope,
                        'intercept': intercept,
                        'r_squared': r_squared,
                        'std_error': std_err
                    })

                # Plot scatter points
                color = agent_colors.get(agent_type, 'steelblue')
                ax.scatter(steps, tokens, color=color, alpha=0.7, s=100,
                          edgecolors='black', linewidths=1)

                # Plot regression line
                x_line = np.array([steps.min(), steps.max()])
                y_line = slope * x_line + intercept
                ax.plot(x_line, y_line, 'r--', linewidth=2, label=f'y = {slope:.1f}x + {intercept:.0f}')

                # Add extrapolation
                x_extrap = np.array([steps.min(), max(steps.max(), 100)])
                y_extrap = slope * x_extrap + intercept
                ax.plot(x_extrap, y_extrap, 'r:', linewidth=1.5, alpha=0.5, label='Extrapolation')

                # Styling
                model_short = model.replace('anthropic-', '').replace('openai-', '').replace('google-', '')
                ax.set_title(f'{agent_type} ({model_short})\nR² = {r_squared:.3f}',
                           fontsize=11, fontweight='bold')
                ax.set_xlabel('Steps', fontsize=10)
                ax.set_ylabel('Total Tokens', fontsize=10)
                ax.legend(fontsize=9)
                ax.grid(True, alpha=0.3)
            elif not agent_model_data.empty and len(agent_model_data) == 1:
                # Plot single data point
                steps = agent_model_data['total_messages'].values
                tokens = agent_model_data['total_tokens'].values
                color = agent_colors.get(agent_type, 'steelblue')
                ax.scatter(steps, tokens, color=color, alpha=0.7, s=100,
                          edgecolors='black', linewidths=1)
                model_short = model.replace('anthropic-', '').replace('openai-', '').replace('google-', '')
                ax.set_title(f'{agent_type} ({model_short})\nInsufficient data for regression',
                           fontsize=11, fontweight='bold')
                ax.set_xlabel('Steps', fontsize=10)
                ax.set_ylabel('Total Tokens', fontsize=10)
                ax.grid(True, alpha=0.3)
            else:
                model_short = model.replace('anthropic-', '').replace('openai-', '').replace('google-', '')
                ax.text(0.5, 0.5, f'No data\n{agent_type} ({model_short})', ha='center', va='center',
                       transform=ax.transAxes, fontsize=10)
                ax.set_xticks([])
                ax.set_yticks([])

    plt.suptitle('Token Growth vs Steps with Linear Regression',
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/token_growth_regression.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Create regression summary CSV
    if regression_data:
        regression_df = pd.DataFrame(regression_data)

        # Add predictions at different step counts
        prediction_steps = [50, 100, 200, 500]
        for step_count in prediction_steps:
            regression_df[f'predicted_tokens_at_{step_count}_steps'] = (
                regression_df['slope'] * step_count + regression_df['intercept']
            ).astype(int)

        regression_df.to_csv(f"{output_dir}/token_growth_regression.csv", index=False)
        print(f"Exported: {output_dir}/token_growth_regression.csv")

    print(f"\nVisualizations saved to {output_dir}/")


def export_csvs(runs: List[AgentRun], output_dir: str = "analysis_output"):
    """Export CSV files with detailed metrics"""
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame([asdict(run) for run in runs])

    # Add calculated metrics
    df['tokens_per_second'] = df['total_tokens'] / df['total_time_seconds']

    # 1. Detailed metrics CSV
    df.to_csv(f"{output_dir}/detailed_metrics.csv", index=False)
    print(f"Exported: {output_dir}/detailed_metrics.csv")

    # 2. Agent comparison CSV (aggregated)
    comparison = df.groupby('agent_type').agg({
        'total_messages': ['mean', 'std'],
        'total_time_seconds': ['mean', 'std'],
        'total_cost': ['mean', 'std'],
        'total_tokens': ['mean', 'std'],
        'avg_tokens_per_step': ['mean', 'std'],
        'avg_time_per_step': ['mean', 'std'],
        'cost_per_step': ['mean', 'std'],
        'tokens_per_second': ['mean', 'std'],
        'is_success': ['sum', 'count'],
        'accuracy_score': ['mean', 'std']
    }).round(4)

    # Flatten column names
    comparison.columns = ['_'.join(col).strip() for col in comparison.columns.values]
    comparison['success_rate'] = (comparison['is_success_sum'] / comparison['is_success_count'] * 100).round(2)

    comparison.to_csv(f"{output_dir}/agent_comparison.csv")
    print(f"Exported: {output_dir}/agent_comparison.csv")

    # 3. Accuracy analysis CSV (field-by-field with detailed metrics)
    accuracy_records = []

    for run in runs:
        if not run.is_success:
            continue

        for key, true_value in GROUND_TRUTH.items():
            pred_value = run.metrics.get(key, None)

            # Calculate detailed accuracy metrics
            field_metrics = calculate_field_accuracy(pred_value, true_value)

            accuracy_records.append({
                'run_id': run.run_id,
                'agent_type': run.agent_type,
                'field': key,
                'true_value': true_value,
                'predicted_value': pred_value,
                'is_correct': field_metrics['is_correct'],
                'error': field_metrics['error'],
                'percentage_error': field_metrics['percentage_error'],
                'proximity_score': field_metrics['proximity_score']
            })

    if accuracy_records:
        accuracy_df = pd.DataFrame(accuracy_records)
        accuracy_df.to_csv(f"{output_dir}/accuracy_analysis.csv", index=False)
        print(f"Exported: {output_dir}/accuracy_analysis.csv")

        # 4. Field-level accuracy summary
        field_summary = accuracy_df.groupby(['agent_type', 'field']).agg({
            'is_correct': 'mean',
            'proximity_score': 'mean',
            'percentage_error': 'mean'
        }).round(4)
        field_summary.columns = ['accuracy_rate', 'avg_proximity_score', 'avg_percentage_error']
        field_summary.to_csv(f"{output_dir}/field_accuracy_summary.csv")
        print(f"Exported: {output_dir}/field_accuracy_summary.csv")


def generate_summary_report(runs: List[AgentRun], output_dir: str = "analysis_output"):
    """Generate a markdown summary report optimized for GitHub"""
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame([asdict(run) for run in runs])

    report = []

    # Title and overview
    report.append("# Agent Performance Analysis Report\n\n")
    report.append("> Comprehensive comparison of different agent architectures for data analysis tasks\n\n")

    # Table of contents
    report.append("## Table of Contents\n\n")
    report.append("- [Overview](#overview)\n")
    report.append("- [Success Rate](#success-rate)\n")
    report.append("- [Performance Metrics](#performance-metrics)\n")
    report.append("- [Detailed Analysis](#detailed-analysis)\n")
    report.append("- [Key Insights](#key-insights)\n")
    report.append("- [Recommendations](#recommendations)\n\n")

    report.append("---\n\n")

    # Overview section
    report.append("## Overview\n\n")
    report.append(f"**Total Runs Analyzed:** {len(runs)}  \n")
    report.append(f"**Agent Types:** {df['agent_type'].nunique()}  \n")
    report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")

    # Models used
    unique_models = df['model_name'].unique()
    report.append(f"**Models Tested:** {', '.join([f'`{m}`' for m in unique_models])}\n\n")

    # Quick stats table
    report.append("### Quick Stats\n\n")
    report.append("| Agent Type | Model | Runs | Success Rate | Avg Cost | Avg Time | Avg Steps |\n")
    report.append("|------------|-------|------|--------------|----------|----------|----------|\n")

    # Group by both agent_type and model
    for agent_type in sorted(df['agent_type'].unique()):
        for model_name in sorted(df[df['agent_type'] == agent_type]['model_name'].unique()):
            agent_data = df[(df['agent_type'] == agent_type) & (df['model_name'] == model_name)]
            successful = agent_data[agent_data['is_success'] == True]
            success_rate = len(successful) / len(agent_data) * 100 if len(agent_data) > 0 else 0

            short_model = model_name.replace('anthropic-', '').replace('openai-', '')
            report.append(f"| `{agent_type}` | `{short_model}` | {len(agent_data)} | {success_rate:.1f}% | ")
            report.append(f"${agent_data['total_cost'].mean():.2f} | ")
            report.append(f"{agent_data['total_time_seconds'].mean():.1f}s | ")
            report.append(f"{agent_data['total_messages'].mean():.1f} |\n")

    report.append("\n---\n\n")

    # Success Rate Section with embedded image
    report.append("## Success Rate\n\n")
    report.append("![Success Rate](success_rate.png)\n\n")

    success_rates = df.groupby(['agent_type', 'model_name'])['is_success'].agg(['sum', 'count'])
    success_rates['rate'] = (success_rates['sum'] / success_rates['count']) * 100

    for agent_type in sorted(df['agent_type'].unique()):
        for model_name in sorted(df[df['agent_type'] == agent_type]['model_name'].unique()):
            if (agent_type, model_name) not in success_rates.index:
                continue

            rate = success_rates.loc[(agent_type, model_name), 'rate']
            total = success_rates.loc[(agent_type, model_name), 'count']
            successful = success_rates.loc[(agent_type, model_name), 'sum']

            short_model = model_name.replace('anthropic-', '').replace('openai-', '')
            badge_color = "green" if rate == 100 else "yellow" if rate >= 50 else "red"
            report.append(f"- **`{agent_type}`** ({short_model}): {int(successful)}/{int(total)} successful ({rate:.1f}%) ")
            report.append(f"![{rate:.0f}%](https://img.shields.io/badge/success-{rate:.0f}%25-{badge_color})\n")

    report.append("\n---\n\n")

    # Performance Metrics with embedded images
    report.append("## Performance Metrics\n\n")

    report.append("### Cost Comparison\n\n")
    report.append("![Cost Comparison](cost_comparison.png)\n\n")

    successful_runs = df[df['is_success'] == True]
    if not successful_runs.empty:
        cost_data = successful_runs.groupby(['agent_type', 'model_name'])['total_cost'].agg(['mean', 'std'])
        report.append("| Agent Type | Model | Average Cost | Std Dev |\n")
        report.append("|------------|-------|--------------|----------|\n")
        for (agent, model) in cost_data.index:
            short_model = model.replace('anthropic-', '').replace('openai-', '')
            report.append(f"| `{agent}` | `{short_model}` | ${cost_data.loc[(agent, model), 'mean']:.2f} | ±${cost_data.loc[(agent, model), 'std']:.2f} |\n")
        report.append("\n")

    report.append("### Execution Time\n\n")
    report.append("![Execution Time](execution_time.png)\n\n")

    time_data = df.groupby(['agent_type', 'model_name'])['total_time_seconds'].agg(['mean', 'std'])
    report.append("| Agent Type | Model | Average Time | Std Dev |\n")
    report.append("|------------|-------|--------------|----------|\n")
    for (agent, model) in time_data.index:
        short_model = model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"| `{agent}` | `{short_model}` | {time_data.loc[(agent, model), 'mean']:.1f}s | ±{time_data.loc[(agent, model), 'std']:.1f}s |\n")
    report.append("\n")

    report.append("### Step Count\n\n")
    report.append("![Step Count](step_count.png)\n\n")

    step_data = df.groupby(['agent_type', 'model_name'])['total_messages'].agg(['mean', 'std'])
    report.append("| Agent Type | Model | Average Steps | Std Dev |\n")
    report.append("|------------|-------|---------------|----------|\n")
    for (agent, model) in step_data.index:
        short_model = model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"| `{agent}` | `{short_model}` | {step_data.loc[(agent, model), 'mean']:.1f} | ±{step_data.loc[(agent, model), 'std']:.1f} |\n")
    report.append("\n")

    report.append("### Token Usage\n\n")
    report.append("![Token Usage](token_usage.png)\n\n")

    token_data = df.groupby(['agent_type', 'model_name'])[['input_tokens', 'output_tokens', 'total_tokens']].mean()
    report.append("| Agent Type | Model | Input Tokens | Output Tokens | Total Tokens |\n")
    report.append("|------------|-------|--------------|---------------|-------------|\n")
    for (agent, model) in token_data.index:
        short_model = model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"| `{agent}` | `{short_model}` | {token_data.loc[(agent, model), 'input_tokens']:.0f} | ")
        report.append(f"{token_data.loc[(agent, model), 'output_tokens']:.0f} | ")
        report.append(f"{token_data.loc[(agent, model), 'total_tokens']:.0f} |\n")
    report.append("\n")

    report.append("### Tokens vs Steps Relationship\n\n")
    report.append("![Tokens vs Steps](tokens_vs_steps.png)\n\n")

    # Per-step latency
    report.append("### Per-Step Latency\n\n")
    report.append("![Per-Step Latency](per_step_latency.png)\n\n")

    latency_data = df.groupby(['agent_type', 'model_name'])['avg_time_per_step'].agg(['mean', 'std'])
    report.append("| Agent Type | Model | Avg Latency per Step | Std Dev |\n")
    report.append("|------------|-------|----------------------|----------|\n")
    for (agent, model) in latency_data.index:
        short_model = model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"| `{agent}` | `{short_model}` | {latency_data.loc[(agent, model), 'mean']:.2f}s | ±{latency_data.loc[(agent, model), 'std']:.2f}s |\n")
    report.append("\n")

    # Tokens per second (throughput)
    df['tokens_per_second'] = df['total_tokens'] / df['total_time_seconds']
    report.append("### Token Processing Throughput\n\n")
    report.append("![Tokens per Second](tokens_per_second.png)\n\n")

    throughput_data = df.groupby(['agent_type', 'model_name'])['tokens_per_second'].agg(['mean', 'std'])
    report.append("| Agent Type | Model | Tokens/Second | Std Dev |\n")
    report.append("|------------|-------|---------------|----------|\n")
    for (agent, model) in throughput_data.index:
        short_model = model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"| `{agent}` | `{short_model}` | {throughput_data.loc[(agent, model), 'mean']:.0f} | ±{throughput_data.loc[(agent, model), 'std']:.0f} |\n")
    report.append("\n")

    # Latency vs Tokens relationship
    report.append("### Latency vs Token Usage\n\n")
    report.append("![Latency vs Tokens](latency_vs_tokens.png)\n\n")
    report.append("This scatter plot shows the relationship between tokens per step and latency per step, "
                 "helping identify efficiency patterns across different agent configurations.\n\n")

    # Token Growth Regression Analysis
    report.append("### Token Growth Scaling Analysis\n\n")
    report.append("![Token Growth Regression](token_growth_regression.png)\n\n")
    report.append("Linear regression analysis showing how token usage scales with the number of steps. "
                 "The regression lines (dashed) show the trend, while dotted lines extrapolate beyond observed data.\n\n")

    # Load regression data if it exists
    regression_csv = f"{output_dir}/token_growth_regression.csv"
    if os.path.exists(regression_csv):
        regression_df = pd.read_csv(regression_csv)

        report.append("#### Regression Parameters\n\n")
        report.append("| Agent Type | Model | Tokens/Step (Slope) | Base Tokens (Intercept) | R² | Predicted @ 100 steps |\n")
        report.append("|------------|-------|---------------------|-------------------------|-----|----------------------|\n")

        for _, row in regression_df.iterrows():
            short_model = row['model_name'].replace('anthropic-', '').replace('openai-', '').replace('google-', '')
            report.append(f"| `{row['agent_type']}` | `{short_model}` | {row['slope']:.1f} | "
                        f"{row['intercept']:.0f} | {row['r_squared']:.3f} | "
                        f"{row['predicted_tokens_at_100_steps']:,} |\n")

        report.append("\n**Interpretation:**\n")
        report.append("- **Tokens/Step (Slope)**: Additional tokens consumed per additional step\n")
        report.append("- **Base Tokens (Intercept)**: Fixed overhead tokens\n")
        report.append("- **R²**: How well the linear model fits (1.0 = perfect fit)\n\n")

        report.append("#### Extrapolated Token Predictions\n\n")
        report.append("| Agent Type | Model | @ 50 steps | @ 100 steps | @ 200 steps | @ 500 steps |\n")
        report.append("|------------|-------|------------|-------------|-------------|-------------|\n")

        for _, row in regression_df.iterrows():
            short_model = row['model_name'].replace('anthropic-', '').replace('openai-', '').replace('google-', '')
            report.append(f"| `{row['agent_type']}` | `{short_model}` | "
                        f"{row['predicted_tokens_at_50_steps']:,} | "
                        f"{row['predicted_tokens_at_100_steps']:,} | "
                        f"{row['predicted_tokens_at_200_steps']:,} | "
                        f"{row['predicted_tokens_at_500_steps']:,} |\n")

        report.append("\n")

    if not successful_runs.empty and successful_runs['accuracy_score'].sum() > 0:
        report.append("### Accuracy Score\n\n")
        report.append("![Accuracy Score](accuracy_score.png)\n\n")

        accuracy_data = successful_runs.groupby(['agent_type', 'model_name'])['accuracy_score'].agg(['mean', 'std'])
        report.append("| Agent Type | Model | Average Accuracy | Std Dev |\n")
        report.append("|------------|-------|------------------|----------|\n")
        for (agent, model) in accuracy_data.index:
            short_model = model.replace('anthropic-', '').replace('openai-', '')
            report.append(f"| `{agent}` | `{short_model}` | {accuracy_data.loc[(agent, model), 'mean']:.2%} | ±{accuracy_data.loc[(agent, model), 'std']:.2%} |\n")
        report.append("\n")

    # Field-level accuracy analysis
    report.append("### Field-Level Accuracy Analysis\n\n")

    # Build field accuracy data
    accuracy_records = []
    for run in runs:
        if not run.is_success:
            continue

        for key, true_value in GROUND_TRUTH.items():
            pred_value = run.metrics.get(key, None)
            field_metrics = calculate_field_accuracy(pred_value, true_value)

            accuracy_records.append({
                'agent_type': run.agent_type,
                'model_name': run.model_name,
                'agent_model': f"{run.agent_type}\n({run.model_name.replace('anthropic-', '').replace('openai-', '')})",
                'field': key,
                'is_correct': field_metrics['is_correct'],
                'proximity_score': field_metrics['proximity_score'],
                'percentage_error': field_metrics['percentage_error']
            })

    if accuracy_records:
        acc_df = pd.DataFrame(accuracy_records)

        report.append("#### Field Accuracy Heatmap\n\n")
        report.append("![Field Accuracy Heatmap](field_accuracy_heatmap.png)\n\n")

        report.append("#### Proximity Score Heatmap\n\n")
        report.append("![Field Proximity Heatmap](field_proximity_heatmap.png)\n\n")

        # Table showing field-level accuracy
        pivot_correct = acc_df.pivot_table(
            values='is_correct',
            index='field',
            columns='agent_model',
            aggfunc='mean'
        )

        report.append("#### Field Accuracy Rates\n\n")
        # Create cleaner column headers without newlines
        clean_columns = [col.replace('\n', ' ') for col in pivot_correct.columns]
        report.append("| Field | " + " | ".join(clean_columns) + " |\n")
        report.append("|" + "---|" * (len(pivot_correct.columns) + 1) + "\n")
        for field in pivot_correct.index:
            report.append(f"| `{field}` |")
            for agent_model in pivot_correct.columns:
                val = pivot_correct.loc[field, agent_model]
                if pd.notna(val):
                    report.append(f" {val:.0%} |")
                else:
                    report.append(" N/A |")
            report.append("\n")
        report.append("\n")

        # Percentage error for numeric fields
        numeric_errors = acc_df[acc_df['percentage_error'].notna()]
        if not numeric_errors.empty:
            report.append("#### Percentage Error (Numeric Fields)\n\n")
            report.append("![Percentage Error](field_percentage_error.png)\n\n")

            pivot_error = numeric_errors.pivot_table(
                values='percentage_error',
                index='field',
                columns='agent_model',
                aggfunc='mean'
            )

            # Create cleaner column headers without newlines
            clean_error_columns = [col.replace('\n', ' ') for col in pivot_error.columns]
            report.append("| Field | " + " | ".join(clean_error_columns) + " |\n")
            report.append("|" + "---|" * (len(pivot_error.columns) + 1) + "\n")
            for field in pivot_error.index:
                report.append(f"| `{field}` |")
                for agent_model in pivot_error.columns:
                    val = pivot_error.loc[field, agent_model]
                    if pd.notna(val):
                        report.append(f" {val:.1f}% |")
                    else:
                        report.append(" N/A |")
                report.append("\n")
            report.append("\n")

    report.append("---\n\n")

    # Detailed Analysis
    report.append("## Detailed Analysis\n\n")

    for agent_type in sorted(df['agent_type'].unique()):
        agent_data = df[df['agent_type'] == agent_type]
        successful = agent_data[agent_data['is_success'] == True]
        model_name = agent_data['model_name'].iloc[0]

        report.append(f"### `{agent_type}` ({model_name})\n\n")

        # Status badges
        success_count = len(successful)
        total_count = len(agent_data)
        success_rate = success_count / total_count * 100 if total_count > 0 else 0

        report.append(f"![Runs](https://img.shields.io/badge/runs-{total_count}-blue) ")
        report.append(f"![Success](https://img.shields.io/badge/success-{success_count}-green) ")

        if total_count > success_count:
            report.append(f"![Failed](https://img.shields.io/badge/failed-{total_count - success_count}-red)")

        report.append("\n\n")

        if not successful.empty:
            report.append("**Performance (Successful Runs Only):**\n\n")
            report.append(f"- **Average Steps:** {successful['total_messages'].mean():.1f}\n")
            report.append(f"- **Average Cost:** ${successful['total_cost'].mean():.2f}\n")
            report.append(f"- **Average Time:** {successful['total_time_seconds'].mean():.1f}s\n")
            report.append(f"- **Average Tokens:** {successful['total_tokens'].mean():.0f}\n")
            report.append(f"- **Tokens per Step:** {successful['avg_tokens_per_step'].mean():.0f}\n")
            report.append(f"- **Cost per Step:** ${successful['cost_per_step'].mean():.4f}\n")
            report.append(f"- **Time per Step:** {successful['avg_time_per_step'].mean():.2f}s\n")

            if successful['accuracy_score'].sum() > 0:
                report.append(f"- **Average Accuracy:** {successful['accuracy_score'].mean():.2%}\n")

            report.append("\n")

        if total_count > success_count:
            report.append("**Note:** This agent had failed runs. Check detailed metrics for more information.\n\n")

    report.append("---\n\n")

    # Key Insights
    report.append("## Key Insights\n\n")

    # Rankings
    report.append("### Rankings\n\n")

    # Success rate (grouped by agent_type and model)
    success_rates = df.groupby(['agent_type', 'model_name'])['is_success'].mean().sort_values(ascending=False)
    report.append("#### Success Rate\n\n")
    for i, ((agent, model), rate) in enumerate(success_rates.items(), 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        model_short = model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"{medal} **`{agent}`** ({model_short}): {rate*100:.1f}%  \n")
    report.append("\n")

    if not successful_runs.empty:
        # Cost efficiency
        cost_efficiency = successful_runs.groupby(['agent_type', 'model_name'])['total_cost'].mean().sort_values()
        report.append("#### Cost Efficiency (Lower is Better)\n\n")
        for i, ((agent, model), cost) in enumerate(cost_efficiency.items(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            model_short = model.replace('anthropic-', '').replace('openai-', '')
            report.append(f"{medal} **`{agent}`** ({model_short}): ${cost:.2f}  \n")
        report.append("\n")

        # Speed
        speed_ranking = successful_runs.groupby(['agent_type', 'model_name'])['total_time_seconds'].mean().sort_values()
        report.append("#### Speed (Lower is Better)\n\n")
        for i, ((agent, model), time) in enumerate(speed_ranking.items(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            model_short = model.replace('anthropic-', '').replace('openai-', '')
            report.append(f"{medal} **`{agent}`** ({model_short}): {time:.1f}s  \n")
        report.append("\n")

        # Accuracy
        if successful_runs['accuracy_score'].sum() > 0:
            accuracy_ranking = successful_runs.groupby(['agent_type', 'model_name'])['accuracy_score'].mean().sort_values(ascending=False)
            report.append("#### Accuracy (Higher is Better)\n\n")
            for i, ((agent, model), acc) in enumerate(accuracy_ranking.items(), 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                model_short = model.replace('anthropic-', '').replace('openai-', '')
                report.append(f"{medal} **`{agent}`** ({model_short}): {acc:.2%}  \n")
            report.append("\n")

    report.append("---\n\n")

    # Recommendations
    report.append("## Recommendations\n\n")

    if not successful_runs.empty:
        # Find the best overall agent
        report.append("### Best Agent for Different Use Cases\n\n")

        # Most cost-efficient
        best_cost_idx = successful_runs.groupby(['agent_type', 'model_name'])['total_cost'].mean().idxmin()
        best_cost_value = successful_runs.groupby(['agent_type', 'model_name'])['total_cost'].mean().min()
        best_cost_agent, best_cost_model = best_cost_idx
        best_cost_model_short = best_cost_model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"- **💰 Most Cost-Efficient:** `{best_cost_agent}` ({best_cost_model_short}) - ${best_cost_value:.2f} per run\n")

        # Fastest
        fastest_idx = successful_runs.groupby(['agent_type', 'model_name'])['total_time_seconds'].mean().idxmin()
        fastest_value = successful_runs.groupby(['agent_type', 'model_name'])['total_time_seconds'].mean().min()
        fastest_agent, fastest_model = fastest_idx
        fastest_model_short = fastest_model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"- **⚡ Fastest:** `{fastest_agent}` ({fastest_model_short}) - {fastest_value:.1f}s per run\n")

        # Most accurate
        if successful_runs['accuracy_score'].sum() > 0:
            most_accurate_idx = successful_runs.groupby(['agent_type', 'model_name'])['accuracy_score'].mean().idxmax()
            accuracy_value = successful_runs.groupby(['agent_type', 'model_name'])['accuracy_score'].mean().max()
            most_accurate_agent, most_accurate_model = most_accurate_idx
            most_accurate_model_short = most_accurate_model.replace('anthropic-', '').replace('openai-', '')
            report.append(f"- **🎯 Most Accurate:** `{most_accurate_agent}` ({most_accurate_model_short}) - {accuracy_value:.2%} accuracy\n")

        # Most reliable (highest success rate)
        most_reliable_idx = success_rates.idxmax()
        reliable_rate = success_rates.max() * 100
        most_reliable_agent, most_reliable_model = most_reliable_idx
        most_reliable_model_short = most_reliable_model.replace('anthropic-', '').replace('openai-', '')
        report.append(f"- **✅ Most Reliable:** `{most_reliable_agent}` ({most_reliable_model_short}) - {reliable_rate:.1f}% success rate\n")

        report.append("\n")

    # Final thoughts
    report.append("### Overall Assessment\n\n")

    # Calculate a composite score
    if not successful_runs.empty:
        report.append("Based on the analysis:\n\n")

        # Normalize metrics for comparison (lower is better for cost and time, higher for accuracy and success)
        metrics_comparison = []
        for agent_type in df['agent_type'].unique():
            agent_successful = successful_runs[successful_runs['agent_type'] == agent_type]
            if len(agent_successful) > 0:
                success_rate = df[df['agent_type'] == agent_type]['is_success'].mean()
                avg_cost = agent_successful['total_cost'].mean()
                avg_time = agent_successful['total_time_seconds'].mean()
                avg_accuracy = agent_successful['accuracy_score'].mean()

                metrics_comparison.append({
                    'agent': agent_type,
                    'success_rate': success_rate,
                    'cost': avg_cost,
                    'time': avg_time,
                    'accuracy': avg_accuracy
                })

        if metrics_comparison:
            metrics_df = pd.DataFrame(metrics_comparison)

            # Find balanced agent (good across all metrics)
            report.append("The data suggests different agents excel in different areas. ")
            report.append("Choose based on your priorities:\n\n")
            report.append("- If **budget is critical**, prioritize the most cost-efficient agent\n")
            report.append("- If **speed is essential**, choose the fastest agent\n")
            report.append("- If **accuracy matters most**, select the most accurate agent\n")
            report.append("- If **reliability is key**, go with the highest success rate\n")

    report.append("\n---\n\n")
    report.append(f"*Report generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    # Write report
    report_path = f"{output_dir}/summary_report.md"
    with open(report_path, 'w') as f:
        f.write(''.join(report))

    print(f"Exported: {report_path}")


def main():
    """Main execution function"""
    print("=" * 60)
    print("Agent Performance Analysis")
    print("=" * 60)

    # Load all runs
    print("\nLoading agent runs...")
    runs = load_all_runs()

    if not runs:
        print("No runs found in outputs/ directory")
        return

    print(f"\nTotal runs loaded: {len(runs)}")

    # Generate outputs
    output_dir = "analysis_output"

    print("\nGenerating visualizations...")
    generate_visualizations(runs, output_dir)

    print("\nExporting CSV files...")
    export_csvs(runs, output_dir)

    print("\nGenerating summary report...")
    generate_summary_report(runs, output_dir)

    print("\n" + "=" * 60)
    print(f"Analysis complete! Results saved to {output_dir}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
