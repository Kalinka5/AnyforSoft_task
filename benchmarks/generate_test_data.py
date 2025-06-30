"""
Generates large-scale test data for benchmarking.
"""
import argparse
import json
import random

def generate_test_data(num_partners: int, max_depth: int) -> list:
    """
    Generates a large, random hierarchy of partners.

    Args:
        num_partners: The total number of partners to generate.
        max_depth: The maximum depth of the hierarchy.

    Returns:
        A list of partner dictionaries.
    """
    if num_partners <= 0:
        return []

    partners = []
    partners.append({"id": 1, "parent_id": None, "name": "Partner1", "monthly_revenue": random.randint(1000, 10000)})
    
    # Keep track of the depth of each partner
    depth_map = {1: 0}
    
    next_id = 2
    while next_id <= num_partners:
        # Choose a random existing partner to be the parent
        parent_id = random.randint(1, next_id - 1)
        
        # Ensure max depth is respected
        if depth_map[parent_id] < max_depth:
            parent_depth = depth_map[parent_id]
        else:
            # If the chosen parent is at max depth, find one that isn't
            # This is not perfectly efficient but good enough for test data generation
            potential_parents = [pid for pid, depth in depth_map.items() if depth < max_depth]
            if not potential_parents:
                # If all existing nodes are at max_depth, we can't add more levels.
                # Attach to a random existing node.
                parent_id = random.randint(1, next_id - 1)
                parent_depth = depth_map[parent_id]
            else:
                parent_id = random.choice(potential_parents)
                parent_depth = depth_map[parent_id]

        partners.append({
            "id": next_id,
            "parent_id": parent_id,
            "name": f"Partner{next_id}",
            "monthly_revenue": random.randint(500, 8000)
        })
        depth_map[next_id] = parent_depth + 1
        next_id += 1
        
    return partners

def main():
    """Main function to generate test data."""
    parser = argparse.ArgumentParser(description="Generate large test datasets for the MLM commission engine.")
    parser.add_argument(
        "--num-partners", type=int, default=50000, help="Number of partners to generate."
    )
    parser.add_argument(
        "--max-depth", type=int, default=15, help="Maximum depth of the hierarchy."
    )
    parser.add_argument(
        "--output", default="large_partners.json", help="Output file path."
    )
    args = parser.parse_args()

    print(f"Generating {args.num_partners} partners with max depth {args.max_depth}...")
    data = generate_test_data(args.num_partners, args.max_depth)
    
    with open(args.output, 'w') as f:
        json.dump(data, f)
        
    print(f"Successfully generated test data and saved to '{args.output}'")

if __name__ == "__main__":
    main()
