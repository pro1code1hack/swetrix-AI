import json
import re


def serialise_predictions(data):
    """Process predictions from a list of dictionaries after the result of model's prediction"""

    results = []

    # Function to split the key and categorize
    def categorize_key(key):
        match = re.match(r"(\w+)_([\w-]+)_next_(\d+)_hr", key)
        if match:
            category, field, hour = match.groups()
            return category, field, f"next_{hour}_hour"
        return None, None, None

    for record in data:
        pid = record.get("pid")

        hours = {}
        for key, value in record.items():
            if value == 0:
                continue
            category, field, hour = categorize_key(key)
            if category and field and hour:
                if hour not in hours:
                    hours[hour] = {}
                if category not in hours[hour]:
                    hours[hour][category] = {}
                hours[hour][category][field] = value

        result = {"pid": pid, **hours}

        results.append(result)

    return results

def serialise_data_for_clickhouse(data):
    """Serialise the processed data for ClickHouse insertion"""
    serialized_data = []

    for record in data:
        pid = record["pid"]
        next_hours = []
        cumulative_data = {}

        for hr in range(1, 25):
            current_hour_data = record.get(f"next_{hr}_hour", {})
            for key, value in current_hour_data.items():
                if key in cumulative_data:
                    if isinstance(value, dict) and isinstance(cumulative_data[key], dict):
                        for sub_key, sub_value in value.items():
                            if sub_key in cumulative_data[key]:
                                cumulative_data[key][sub_key] += sub_value
                            else:
                                cumulative_data[key][sub_key] = sub_value
                    else:
                        cumulative_data[key] += value
                else:
                    cumulative_data[key] = value

            next_n_hour = json.dumps(cumulative_data)
            next_hours.append(next_n_hour)

        serialized_data.append(
            (
                pid,
                *next_hours
            )
        )

    return serialized_data