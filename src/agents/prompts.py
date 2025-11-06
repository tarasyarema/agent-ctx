USER_PROMPT = """
Using the NYC taxi trip dataset, analyze the market and create a fleet deployment recommendation analysis.

**Required Deliverables:**

You will need to create the following files with the specified content:

1. **`data_profile.txt`**: Document the dataset (row count, date range, key columns, any data quality issues)

2. **`zone_rankings.csv`**: Top 10 zones by profitability with columns:
   - zone_name
   - total_trips
   - total_revenue
   - avg_fare
   - avg_trip_duration_minutes

3. **`temporal_analysis.csv`**: Hourly performance (0-23) with columns:
   - hour
   - avg_trips_per_day
   - avg_fare
   - revenue_per_hour

4. **`route_matrix.csv`**: Top 15 pickup-dropoff pairs with columns:
   - pickup_zone
   - dropoff_zone  
   - trip_count
   - total_revenue
   - avg_fare
   - avg_distance_miles

5. **`efficiency_metrics.json`**: Key performance indicators:
```json
   {
     "best_revenue_zone": "zone_name",    // Name, not ID
     "best_revenue_hour": 18,
     "avg_revenue_per_trip": 15.50,
     "optimal_distance_bracket": "2-5mi",
     "trips_below_min_fare": 1234,        // I.e. trips with fare <= $2.50
     "trips_above_max_distance": 56       // I.e. trips > 100 miles
   }
```

**Constraints for the efficiency analysis:**
- Consider only trips with fare > $2.50 (minimum viable)
- Filter out trips > 100 miles (data errors)
- Use zone names, not IDs

Document your exploration process. I'll validate the CSVs and JSON can be parsed and matched against expected results.
"""
