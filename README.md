# kerfi-1
Test kerfi fyrir autopull

## AutoPull Test Script

This repository contains a simple Python script to test autopull functionality for a Python batch server running on miniforge3.

### Usage

Run the test script:

```bash
python3 test_autopull.py
```

Or with a specific repository path:

```bash
python3 test_autopull.py /path/to/repo
```

Or make it executable and run directly:

```bash
chmod +x test_autopull.py
./test_autopull.py
```

### Features

The script tests the following:

- **Git Repository Check**: Verifies that the directory is a git repository
- **Miniforge3 Environment Check**: Detects if running in a miniforge3 environment
- **Current Commit Check**: Retrieves the current git commit hash
- **Remote Updates Check**: Checks if there are updates available from remote
- **Autopull Simulation**: Simulates a git pull operation (dry-run)
- **Batch Server Status**: Tests batch server status and environment

### Requirements

- Python 3.x
- Git
- (Optional) Miniforge3 environment for full functionality

### Output

The script provides detailed logs with timestamps and a summary of test results at the end.
