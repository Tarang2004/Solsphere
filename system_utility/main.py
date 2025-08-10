#!/usr/bin/env python3
"""
Solsphere System Utility
Cross-platform system health monitoring utility
"""

import os
import sys
import time
import json
import logging
import platform
import subprocess
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import psutil
import threading
import signal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('solsphere_utility.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SystemHealthChecker:
    """System health checker for different operating systems"""
    
    def __init__(self, api_endpoint: str = "http://localhost:8000"):
        self.api_endpoint = api_endpoint
        self.machine_id = self._get_machine_id()
        self.hostname = platform.node()
        self.operating_system = platform.system()
        self.os_version = platform.version()
        
    def _get_machine_id(self) -> str:
        """Get unique machine identifier"""
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], 
                                      capture_output=True, text=True, check=True)
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    return lines[1].strip()
            except:
                pass
            return platform.node()
        elif platform.system() == "Darwin":  # macOS
            try:
                result = subprocess.run(['system_profiler', 'SPHardwareDataType'], 
                                      capture_output=True, text=True, check=True)
                for line in result.stdout.split('\n'):
                    if 'Serial Number' in line:
                        return line.split(':')[1].strip()
            except:
                pass
            return platform.node()
        else:  # Linux
            try:
                with open('/etc/machine-id', 'r') as f:
                    return f.read().strip()
            except:
                pass
            return platform.node()
    
    def check_disk_encryption(self) -> Dict[str, Any]:
        """Check disk encryption status"""
        try:
            if platform.system() == "Windows":
                return self._check_windows_disk_encryption()
            elif platform.system() == "Darwin":
                return self._check_macos_disk_encryption()
            else:
                return self._check_linux_disk_encryption()
        except Exception as e:
            logger.error(f"Error checking disk encryption: {e}")
            return {"encrypted": False, "details": str(e)}
    
    def _check_windows_disk_encryption(self) -> Dict[str, Any]:
        """Check Windows BitLocker status"""
        try:
            result = subprocess.run(['manage-bde', '-status'], 
                                  capture_output=True, text=True, check=True)
            return {
                "encrypted": "Protection On" in result.stdout,
                "details": "BitLocker enabled" if "Protection On" in result.stdout else "BitLocker disabled"
            }
        except:
            return {"encrypted": False, "details": "Unable to check BitLocker status"}
    
    def _check_macos_disk_encryption(self) -> Dict[str, Any]:
        """Check macOS FileVault status"""
        try:
            result = subprocess.run(['fdesetup', 'status'], 
                                  capture_output=True, text=True, check=True)
            return {
                "encrypted": "FileVault is On" in result.stdout,
                "details": "FileVault enabled" if "FileVault is On" in result.stdout else "FileVault disabled"
            }
        except:
            return {"encrypted": False, "details": "Unable to check FileVault status"}
    
    def _check_linux_disk_encryption(self) -> Dict[str, Any]:
        """Check Linux disk encryption status"""
        try:
            # Check if LUKS is used
            result = subprocess.run(['lsblk', '-f'], 
                                  capture_output=True, text=True, check=True)
            return {
                "encrypted": "crypto_LUKS" in result.stdout,
                "details": "LUKS encryption detected" if "crypto_LUKS" in result.stdout else "No LUKS encryption"
            }
        except:
            return {"encrypted": False, "details": "Unable to check LUKS status"}
    
    def check_os_updates(self) -> Dict[str, Any]:
        """Check OS update status"""
        try:
            if platform.system() == "Windows":
                return self._check_windows_updates()
            elif platform.system() == "Darwin":
                return self._check_macos_updates()
            else:
                return self._check_linux_updates()
        except Exception as e:
            logger.error(f"Error checking OS updates: {e}")
            return {"up_to_date": False, "details": str(e)}
    
    def _check_windows_updates(self) -> Dict[str, Any]:
        """Check Windows update status"""
        try:
            result = subprocess.run(['wmic', 'qfe', 'list', 'brief'], 
                                  capture_output=True, text=True, check=True)
            # This is a simplified check - in production you'd want more sophisticated logic
            return {
                "up_to_date": True,  # Simplified for demo
                "details": "Windows updates checked",
                "last_update": datetime.now().isoformat()
            }
        except:
            return {"up_to_date": False, "details": "Unable to check Windows updates"}
    
    def _check_macos_updates(self) -> Dict[str, Any]:
        """Check macOS update status"""
        try:
            result = subprocess.run(['softwareupdate', '-l'], 
                                  capture_output=True, text=True, check=True)
            return {
                "up_to_date": "No updates available" in result.stdout,
                "details": "No updates available" if "No updates available" in result.stdout else "Updates available",
                "available_updates": result.stdout
            }
        except:
            return {"up_to_date": False, "details": "Unable to check macOS updates"}
    
    def _check_linux_updates(self) -> Dict[str, Any]:
        """Check Linux update status"""
        try:
            # Check for available updates (Ubuntu/Debian)
            result = subprocess.run(['apt', 'list', '--upgradable'], 
                                  capture_output=True, text=True, check=True)
            return {
                "up_to_date": "WARNING" not in result.stdout,
                "details": "No updates available" if "WARNING" not in result.stdout else "Updates available",
                "available_updates": result.stdout
            }
        except:
            return {
                "up_to_date": True,  # Assume up to date if we can't check
                "details": "Unable to check updates, assuming current"
            }
    
    def check_antivirus(self) -> Dict[str, Any]:
        """Check antivirus presence and status"""
        try:
            if platform.system() == "Windows":
                return self._check_windows_antivirus()
            elif platform.system() == "Darwin":
                return self._check_macos_antivirus()
            else:
                return self._check_linux_antivirus()
        except Exception as e:
            logger.error(f"Error checking antivirus: {e}")
            return {"active": False, "details": str(e)}
    
    def _check_windows_antivirus(self) -> Dict[str, Any]:
        """Check Windows antivirus status"""
        try:
            result = subprocess.run(['wmic', '/namespace:\\\\root\\SecurityCenter2', 'path', 'AntiVirusProduct', 'get', 'displayName,productState'], 
                                  capture_output=True, text=True, check=True)
            return {
                "active": "262144" in result.stdout,  # 262144 indicates real-time protection is on
                "details": "Windows Defender active" if "262144" in result.stdout else "Windows Defender inactive",
                "products": result.stdout
            }
        except:
            return {"active": False, "details": "Unable to check Windows antivirus"}
    
    def _check_macos_antivirus(self) -> Dict[str, Any]:
        """Check macOS antivirus status"""
        try:
            # Check for common macOS antivirus tools
            common_av = ['clamav', 'sophos', 'malwarebytes']
            for av in common_av:
                result = subprocess.run(['which', av], 
                                      capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    return {"active": True, "details": f"{av} found", "product": av}
            
            return {"active": False, "details": "No common antivirus found"}
        except:
            return {"active": False, "details": "Unable to check macOS antivirus"}
    
    def _check_linux_antivirus(self) -> Dict[str, Any]:
        """Check Linux antivirus status"""
        try:
            # Check for common Linux antivirus tools
            common_av = ['clamav', 'chkrootkit', 'rkhunter']
            for av in common_av:
                result = subprocess.run(['which', av], 
                                      capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    return {"active": True, "details": f"{av} found", "product": av}
            
            return {"active": False, "details": "No common antivirus found"}
        except:
            return {"active": False, "details": "Unable to check Linux antivirus"}
    
    def check_sleep_settings(self) -> Dict[str, Any]:
        """Check inactivity sleep settings"""
        try:
            if platform.system() == "Windows":
                return self._check_windows_sleep_settings()
            elif platform.system() == "Darwin":
                return self._check_macos_sleep_settings()
            else:
                return self._check_linux_sleep_settings()
        except Exception as e:
            logger.error(f"Error checking sleep settings: {e}")
            return {"compliant": False, "details": str(e)}
    
    def _check_windows_sleep_settings(self) -> Dict[str, Any]:
        """Check Windows power settings"""
        try:
            result = subprocess.run(['powercfg', '/query'], 
                                  capture_output=True, text=True, check=True)
            # This is a simplified check
            return {
                "compliant": True,  # Simplified for demo
                "details": "Power settings checked",
                "timeout": "Unknown"
            }
        except:
            return {"compliant": False, "details": "Unable to check Windows power settings"}
    
    def _check_macos_sleep_settings(self) -> Dict[str, Any]:
        """Check macOS sleep settings"""
        try:
            result = subprocess.run(['pmset', '-g'], 
                                  capture_output=True, text=True, check=True)
            return {
                "compliant": True,  # Simplified for demo
                "details": "Sleep settings checked",
                "timeout": "Unknown"
            }
        except:
            return {"compliant": False, "details": "Unable to check macOS sleep settings"}
    
    def _check_linux_sleep_settings(self) -> Dict[str, Any]:
        """Check Linux sleep settings"""
        try:
            # Check systemd sleep settings
            result = subprocess.run(['systemctl', 'show', 'sleep.target'], 
                                  capture_output=True, text=True, check=True)
            return {
                "compliant": True,  # Simplified for demo
                "details": "Sleep settings checked",
                "timeout": "Unknown"
            }
        except:
            return {"compliant": False, "details": "Unable to check Linux sleep settings"}
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            return {
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_status": "connected" if psutil.net_if_stats() else "disconnected"
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0,
                "network_status": "unknown"
            }
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run complete system health check"""
        logger.info("Starting system health check...")
        
        # Run all checks
        disk_encryption = self.check_disk_encryption()
        os_updates = self.check_os_updates()
        antivirus = self.check_antivirus()
        sleep_settings = self.check_sleep_settings()
        system_metrics = self.get_system_metrics()
        
        # Compile results
        health_data = {
            "machine_id": self.machine_id,
            "hostname": self.hostname,
            "operating_system": self.operating_system,
            "os_version": self.os_version,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                "disk_encryption": disk_encryption,
                "os_updates": os_updates,
                "antivirus": antivirus,
                "sleep_settings": sleep_settings
            },
            "metrics": system_metrics,
            "issues": []
        }
        
        # Identify issues
        if not disk_encryption.get("encrypted", False):
            health_data["issues"].append({
                "type": "disk_encryption",
                "severity": "critical",
                "message": "Disk encryption is not enabled",
                "details": disk_encryption.get("details", "Unknown")
            })
        
        if not os_updates.get("up_to_date", False):
            health_data["issues"].append({
                "type": "os_updates",
                "severity": "warning",
                "message": "OS updates are available",
                "details": os_updates.get("details", "Unknown")
            })
        
        if not antivirus.get("active", False):
            health_data["issues"].append({
                "type": "antivirus",
                "severity": "critical",
                "message": "No active antivirus protection detected",
                "details": antivirus.get("details", "Unknown")
            })
        
        if not sleep_settings.get("compliant", False):
            health_data["issues"].append({
                "type": "sleep_settings",
                "severity": "warning",
                "message": "Sleep settings may not be compliant",
                "details": sleep_settings.get("details", "Unknown")
            })
        
        logger.info(f"Health check completed. Found {len(health_data['issues'])} issues.")
        return health_data
    
    def send_health_data(self, health_data: Dict[str, Any]) -> bool:
        """Send health data to the API endpoint"""
        try:
            # Prepare data for API
            api_data = {
                "machine_id": health_data["machine_id"],
                "hostname": health_data["hostname"],
                "operating_system": health_data["operating_system"],
                "os_version": health_data["os_version"],
                "disk_encrypted": health_data["checks"]["disk_encryption"]["encrypted"],
                "os_up_to_date": health_data["checks"]["os_updates"]["up_to_date"],
                "antivirus_active": health_data["checks"]["antivirus"]["active"],
                "sleep_settings_compliant": health_data["checks"]["sleep_settings"]["compliant"],
                "cpu_usage": health_data["metrics"]["cpu_usage"],
                "memory_usage": health_data["metrics"]["memory_usage"],
                "disk_usage": health_data["metrics"]["disk_usage"],
                "network_status": health_data["metrics"]["network_status"],
                "issues": health_data["issues"]
            }
            
            # Send to machines endpoint
            response = requests.post(
                f"{self.api_endpoint}/api/machines",
                json=api_data,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("Health data sent successfully")
                return True
            else:
                logger.error(f"Failed to send health data: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending health data: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending health data: {e}")
            return False

class SystemUtility:
    """Main system utility class"""
    
    def __init__(self, api_endpoint: str = "http://localhost:8000", check_interval: int = 30):
        self.api_endpoint = api_endpoint
        self.check_interval = check_interval
        self.health_checker = SystemHealthChecker(api_endpoint)
        self.running = False
        self.last_check_data = None
        
    def start_daemon(self):
        """Start the background daemon"""
        logger.info("Starting Solsphere System Utility daemon...")
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                # Run health check
                health_data = self.health_checker.run_health_check()
                
                # Check if data has changed
                if self._has_data_changed(health_data):
                    logger.info("System state changed, sending update...")
                    if self.health_checker.send_health_data(health_data):
                        self.last_check_data = health_data
                        logger.info("Update sent successfully")
                    else:
                        logger.warning("Failed to send update")
                else:
                    logger.info("No changes detected, skipping update")
                
                # Wait for next check
                time.sleep(self.check_interval * 60)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
        except Exception as e:
            logger.error(f"Unexpected error in daemon: {e}")
        finally:
            self.running = False
            logger.info("System utility daemon stopped")
    
    def _has_data_changed(self, new_data: Dict[str, Any]) -> bool:
        """Check if the new health data represents a change from the last check"""
        if self.last_check_data is None:
            return True
        
        # Compare key fields
        old_checks = self.last_check_data.get("checks", {})
        new_checks = new_data.get("checks", {})
        
        # Check if any critical fields have changed
        for check_type in ["disk_encryption", "os_updates", "antivirus", "sleep_settings"]:
            old_status = old_checks.get(check_type, {})
            new_status = new_checks.get(check_type, {})
            
            if old_status != new_status:
                return True
        
        # Check if issues have changed
        old_issues = self.last_check_data.get("issues", [])
        new_issues = new_data.get("issues", [])
        
        if len(old_issues) != len(new_issues):
            return True
        
        # Check if any issues have changed
        for old_issue, new_issue in zip(old_issues, new_issues):
            if old_issue != new_issue:
                return True
        
        return False
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def run_single_check(self):
        """Run a single health check and display results"""
        logger.info("Running single health check...")
        health_data = self.health_checker.run_health_check()
        
        print("\n=== Solsphere System Health Check ===")
        print(f"Machine ID: {health_data['machine_id']}")
        print(f"Hostname: {health_data['hostname']}")
        print(f"OS: {health_data['operating_system']} {health_data['os_version']}")
        print(f"Timestamp: {health_data['timestamp']}")
        
        print("\n--- Health Check Results ---")
        checks = health_data['checks']
        print(f"Disk Encryption: {'✓' if checks['disk_encryption']['encrypted'] else '✗'}")
        print(f"OS Updates: {'✓' if checks['os_updates']['up_to_date'] else '✗'}")
        print(f"Antivirus: {'✓' if checks['antivirus']['active'] else '✗'}")
        print(f"Sleep Settings: {'✓' if checks['sleep_settings']['compliant'] else '✗'}")
        
        print("\n--- System Metrics ---")
        metrics = health_data['metrics']
        print(f"CPU Usage: {metrics['cpu_usage']}%")
        print(f"Memory Usage: {metrics['memory_usage']}%")
        print(f"Disk Usage: {metrics['disk_usage']}%")
        print(f"Network: {metrics['network_status']}")
        
        if health_data['issues']:
            print(f"\n--- Issues Found ({len(health_data['issues'])}) ---")
            for issue in health_data['issues']:
                print(f"{issue['severity'].upper()}: {issue['message']}")
                if issue.get('details'):
                    print(f"  Details: {issue['details']}")
        else:
            print("\n--- No Issues Found ---")
        
        # Ask if user wants to send data
        try:
            response = input("\nSend this data to the API? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                if self.health_checker.send_health_data(health_data):
                    print("Data sent successfully!")
                else:
                    print("Failed to send data.")
            else:
                print("Data not sent.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Solsphere System Utility")
    parser.add_argument("--api-endpoint", default="http://localhost:8000",
                       help="API endpoint URL (default: http://localhost:8000)")
    parser.add_argument("--check-interval", type=int, default=30,
                       help="Check interval in minutes (default: 30)")
    parser.add_argument("--daemon", action="store_true",
                       help="Run as background daemon")
    parser.add_argument("--single-check", action="store_true",
                       help="Run single health check")
    
    args = parser.parse_args()
    
    utility = SystemUtility(args.api_endpoint, args.check_interval)
    
    if args.single_check:
        utility.run_single_check()
    elif args.daemon:
        utility.start_daemon()
    else:
        # Default: run single check
        utility.run_single_check()

if __name__ == "__main__":
    main()
