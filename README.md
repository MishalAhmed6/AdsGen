# Input Layer Module

A modular input processing system for competitor analysis that handles competitor names, hashtags, and ZIP codes with cleaning, validation, and normalization capabilities.

## Features

- **Competitor Name Processing**: Clean and validate business names with case normalization and character filtering
- **Hashtag Processing**: Extract, clean, and normalize hashtags with duplicate removal and validation
- **ZIP Code Processing**: Validate and format ZIP codes with support for multiple formats
- **Modular Architecture**: Easy to extend and integrate with APIs or UI
- **Batch Processing**: Process multiple items efficiently
- **Configuration Management**: Flexible configuration system
- **Statistics Tracking**: Built-in processing statistics and monitoring

## Installation

```bash
# Clone or copy the input_layer module to your project
# No external dependencies required (uses only Python standard library)
```

## Quick Start

```python
from input_layer import InputLayer, InputType

# Initialize with default configuration
input_layer = InputLayer()

# Process competitor name
result = input_layer.process_single("apple inc.", InputType.COMPETITOR_NAME)
print(result.processed_data)  # "Apple Inc."

# Process hashtags
result = input_layer.process_single("#marketing #digital", InputType.HASHTAG)
print(result.processed_data)  # "#Marketing #Digital"

# Process ZIP code
result = input_layer.process_single("12345-6789", InputType.ZIP_CODE)
print(result.processed_data)  # "12345-6789"
```

## Configuration

```python
from input_layer import InputLayer

config = {
    "competitor_handler": {
        "min_length": 3,
        "max_length": 50,
        "normalize_case": True
    },
    "hashtag_handler": {
        "max_hashtags": 10,
        "forbidden_words": ["spam", "fake"]
    }
}

input_layer = InputLayer(config)
```

## API Reference

### InputLayer Class

Main orchestrator class for processing input data.

#### Methods

- `process_single(data, input_type)`: Process a single input item
- `process_batch(data_list, input_type)`: Process multiple items of the same type
- `validate_single(data, input_type)`: Validate without processing
- `get_statistics()`: Get processing statistics
- `export_results(results, format)`: Export results to JSON or CSV

### Input Types

- `InputType.COMPETITOR_NAME`: Business/company names
- `InputType.HASHTAG`: Social media hashtags
- `InputType.ZIP_CODE`: Postal/ZIP codes

## Examples

See `examples/basic_usage.py` for comprehensive usage examples.

## Testing

```bash
python -m pytest tests/
```

## Architecture

The module is organized into:

- `core/`: Main orchestrator and core functionality
- `handlers/`: Type-specific data handlers
- `models/`: Data models and base classes
- `config.py`: Configuration management
- `exceptions.py`: Custom exception classes

## License

MIT License - see LICENSE file for details.
