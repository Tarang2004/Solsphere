# Solsphere System Utility

A cross-platform system health monitoring utility that collects system health data and reports it to a central API endpoint.

## Features

- **Cross-platform support**: Windows, macOS, and Linux
- **Comprehensive health checks**:
  - Disk encryption status (BitLocker, FileVault, LUKS)
  - OS update status
  - Antivirus presence and status
  - Inactivity sleep settings
  - System metrics (CPU, memory, disk usage)
- **Background daemon mode**: Runs periodic checks every 15-60 minutes
- **Change detection**: Only reports data when there are changes
- **Minimal resource usage**: Lightweight and efficient
- **Secure communication**: HTTP API integration

## Requirements

- Python 3.8 or higher
- Operating system: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+, CentOS 7+)

## Installation

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/solsphere/system-utility.git
cd system-utility

# Install dependencies
pip install -r requirements.txt

# Install the utility
pip install -e .
```

### Option 2: Install directly with pip

```bash
pip install solsphere-utility
```

## Usage

### Single Health Check

Run a one-time health check:

```bash
python main.py --single-check
```

Or if installed:

```bash
solsphere-utility --single-check
```

### Background Daemon Mode

Start the utility as a background daemon that runs periodic checks:

```bash
python main.py --daemon --check-interval 30
```

Or if installed:

```bash
solsphere-utility --daemon --check-interval 30
```

### Command Line Options

- `--api-endpoint`: API endpoint URL (default: http://localhost:8000)
- `--check-interval`: Check interval in minutes (default: 30)
- `--daemon`: Run as background daemon
- `--single-check`: Run single health check

## Configuration

### Environment Variables

You can configure the utility using environment variables:

```bash
export SOLSPHERE_API_ENDPOINT="https://your-api.example.com"
export SOLSPHERE_CHECK_INTERVAL="45"
```

### API Endpoint

The utility sends health data to the configured API endpoint. Make sure your Solsphere backend is running and accessible.

## Health Checks

### Disk Encryption

- **Windows**: Checks BitLocker status using `manage-bde` command
- **macOS**: Checks FileVault status using `fdesetup` command
- **Linux**: Checks for LUKS encryption using `lsblk` command

### OS Updates

- **Windows**: Checks Windows Update status
- **macOS**: Checks for available software updates
- **Linux**: Checks for available package updates (apt-based systems)

### Antivirus

- **Windows**: Checks Windows Security Center for active antivirus
- **macOS**: Checks for common antivirus tools (ClamAV, Sophos, Malwarebytes)
- **Linux**: Checks for common antivirus tools (ClamAV, chkrootkit, rkhunter)

### Sleep Settings

- **Windows**: Checks power configuration settings
- **macOS**: Checks sleep settings using `pmset`
- **Linux**: Checks systemd sleep target configuration

## System Metrics

The utility collects real-time system metrics:

- CPU usage percentage
- Memory usage percentage
- Disk usage percentage
- Network connection status

## Logging

The utility logs all activities to:

- Console output
- `solsphere_utility.log` file in the current directory

Log levels: INFO, WARNING, ERROR

## Troubleshooting

### Common Issues

1. **Permission denied errors**: Run with appropriate privileges for system checks
2. **API connection failed**: Verify the API endpoint is accessible and the backend is running
3. **Command not found**: Some system commands may not be available on all systems

### Debug Mode

Enable debug logging by modifying the logging level in `main.py`:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Formatting

```bash
black main.py
flake8 main.py
```

## Security Considerations

- The utility runs with system privileges to access system information
- Health data is sent over HTTP (consider HTTPS in production)
- No sensitive data is collected or transmitted
- Log files may contain system information

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:

- Create an issue on GitHub
- Contact: admin@solsphere.com
- Documentation: https://solsphere.com/docs

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog

### Version 1.0.0
- Initial release
- Cross-platform support
- Comprehensive health checks
- Background daemon mode
- API integration
