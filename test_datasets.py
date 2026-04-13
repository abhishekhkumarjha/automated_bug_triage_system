from datasets import load_dataset

try:
    print("Trying to load GitHub issues dataset with streaming...")
    dataset = load_dataset('bigcode/the-stack-github-issues', split='train', streaming=True)
    print('Dataset loaded successfully with streaming')

    print("First few examples:")
    for i, example in enumerate(dataset):
        if i >= 3:
            break
        print(f'Example {i+1}:')
        print(f'  Title: {example.get("title", "N/A")}')
        print(f'  Labels: {example.get("labels", [])}')
        print(f'  State: {example.get("state", "N/A")}')
        print()

except Exception as e:
    print(f'Error loading dataset: {e}')

    # Try alternative approach
    print("Trying alternative datasets...")

    # Try a different bug-related dataset
    try:
        print("Trying to load a different dataset...")
        # Let's try some other datasets that might be available
        alternative_datasets = [
            'code_search_net',
            'conala',
            'apps'
        ]

        for ds_name in alternative_datasets:
            try:
                print(f"Trying {ds_name}...")
                dataset = load_dataset(ds_name, split='train', streaming=True)
                print(f"Successfully loaded {ds_name}")
                for i, example in enumerate(dataset):
                    if i >= 2:
                        break
                    print(f"  {ds_name} example {i+1}: {str(example)[:200]}...")
                print()
                break
            except Exception as e2:
                print(f"  Failed {ds_name}: {e2}")

    except Exception as e3:
        print(f"Alternative datasets also failed: {e3}")