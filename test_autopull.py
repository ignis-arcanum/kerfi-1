#!/usr/bin/env python3
"""
Simple Python script to test autopull for a Python batch server running on miniforge3.

This script simulates a batch server that can perform autopull operations,
useful for testing automatic updates and deployments in a miniforge3 environment.
"""

import os
import sys
import time
import subprocess
from datetime import datetime


class AutoPullTester:
    """Test class for autopull functionality on a Python batch server."""
    
    def __init__(self, repo_path=None):
        """
        Initialize the AutoPullTester.
        
        Args:
            repo_path: Path to the git repository. Defaults to current directory.
        """
        self.repo_path = repo_path or os.getcwd()
        self.log_prefix = "[AutoPull Test]"
        
    def log(self, message):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {self.log_prefix} {message}")
        
    def check_git_repo(self):
        """Check if the current directory is a git repository."""
        self.log("Checking if directory is a git repository...")
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            self.log(f"✓ Git repository found: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError:
            self.log("✗ Not a git repository")
            return False
            
    def check_miniforge3(self):
        """Check if running in a miniforge3 environment."""
        self.log("Checking for miniforge3 environment...")
        conda_prefix = os.environ.get("CONDA_PREFIX", "")
        
        # Check if conda_prefix contains miniforge3 as a directory component
        if conda_prefix and ("/miniforge3/" in conda_prefix or conda_prefix.endswith("/miniforge3")):
            self.log(f"✓ Running in miniforge3 environment: {conda_prefix}")
            return True
        else:
            self.log(f"⚠ Not detected as miniforge3 (CONDA_PREFIX: {conda_prefix or 'not set'})")
            return False
            
    def get_current_commit(self):
        """Get the current commit hash."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            commit = result.stdout.strip()
            self.log(f"Current commit: {commit[:8]}")
            return commit
        except subprocess.CalledProcessError as e:
            self.log(f"✗ Failed to get current commit: {e}")
            return None
            
    def check_remote_updates(self):
        """Check if there are remote updates available."""
        self.log("Checking remote updates...")
        try:
            subprocess.run(
                ["git", "fetch"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if upstream tracking branch exists
            check_upstream = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "@{u}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if check_upstream.returncode != 0:
                self.log("⚠ No upstream tracking branch configured")
                return False
            
            result = subprocess.run(
                ["git", "rev-list", "HEAD...@{u}", "--count"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            count = int(result.stdout.strip())
            if count > 0:
                self.log(f"✓ {count} update(s) available on remote")
                return True
            else:
                self.log("✓ No updates available, already up to date")
                return False
                
        except subprocess.CalledProcessError as e:
            self.log(f"✗ Failed to check remote updates: {e}")
            return False
        except ValueError:
            self.log("⚠ Could not determine update count")
            return False
            
    def simulate_autopull(self):
        """Simulate an autopull operation."""
        self.log("Simulating autopull operation...")
        
        try:
            # Get current branch
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()
            self.log(f"Current branch: {branch}")
            
            # Simulate pull (using fetch to avoid actually changing files)
            self.log("Performing git pull (dry-run)...")
            result = subprocess.run(
                ["git", "pull", "--dry-run"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("✓ Autopull simulation successful")
                return True
            else:
                self.log(f"✗ Autopull simulation failed with return code: {result.returncode}")
                return False
                
        except subprocess.CalledProcessError as e:
            self.log(f"✗ Autopull simulation failed: {e}")
            return False
            
    def test_batch_server_status(self):
        """Test batch server status."""
        self.log("Testing batch server status...")
        
        # Simulate batch server checks
        checks = {
            "Python version": sys.version.split()[0],
            "Platform": sys.platform,
            "Working directory": os.getcwd(),
        }
        
        for check, value in checks.items():
            self.log(f"  {check}: {value}")
            
        self.log("✓ Batch server status check complete")
        return True
        
    def run_full_test(self):
        """Run the full autopull test suite."""
        self.log("="*60)
        self.log("Starting AutoPull Test for Python Batch Server")
        self.log("="*60)
        
        results = {
            "Git Repository Check": self.check_git_repo(),
            "Miniforge3 Environment Check": self.check_miniforge3(),
            "Current Commit Check": self.get_current_commit() is not None,
            "Remote Updates Check": self.check_remote_updates(),
            "Autopull Simulation": self.simulate_autopull(),
            "Batch Server Status": self.test_batch_server_status(),
        }
        
        self.log("="*60)
        self.log("Test Results Summary:")
        self.log("="*60)
        
        passed = 0
        for test_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            self.log(f"  {test_name}: {status}")
            if result:
                passed += 1
                
        self.log("="*60)
        self.log(f"Tests completed: {passed}/{len(results)} passed")
        self.log("="*60)
        
        return passed == len(results)


def main():
    """Main entry point for the autopull test script."""
    print("\n" + "="*60)
    print("AutoPull Test Script for Python Batch Server (Miniforge3)")
    print("="*60 + "\n")
    
    # Parse command line arguments
    repo_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Create tester instance and run tests
    tester = AutoPullTester(repo_path)
    success = tester.run_full_test()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
