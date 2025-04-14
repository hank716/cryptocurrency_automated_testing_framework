import argparse
import os
import sys
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command):
    """
    Run a shell command and return the output.
    
    Args:
        command: Command to run
        
    Returns:
        Command output
    """
    logger.info(f"Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with error: {e}")
        logger.error(f"Error output: {e.stderr}")
        return None

def check_dependencies():
    """
    Check if all required dependencies are installed.
    
    Returns:
        True if all dependencies are installed, False otherwise
    """
    logger.info("Checking dependencies...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        logger.error(f"Python 3.8+ is required. Found: {python_version.major}.{python_version.minor}")
        return False
    
    # Check if pip is installed
    if run_command("pip --version") is None:
        logger.error("pip is not installed")
        return False
    
    # Check if required packages are installed
    required_packages = [
        "pytest", "pytest-html", "requests", "selenium", "webdriver-manager", 
        "locust", "pyyaml", "jinja2"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.warning(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Installing missing packages...")
        
        for package in missing_packages:
            if run_command(f"pip install {package}") is None:
                logger.error(f"Failed to install {package}")
                return False
    
    # Check if Chrome is installed (for web tests)
    if run_command("google-chrome --version") is None:
        logger.warning("Google Chrome is not installed. Web tests may fail.")
    
    logger.info("All dependencies are installed")
    return True

def run_api_tests(output_dir):
    """
    Run API tests.
    
    Args:
        output_dir: Directory to store test reports
        
    Returns:
        True if tests passed, False otherwise
    """
    logger.info("Running API tests...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Run API tests
    command = f"pytest api_tests/ -v --html={output_dir}/api_test_report.html"
    output = run_command(command)
    
    if output is None:
        return False
    
    # Check if tests passed
    if "failed" in output and "failed" not in output.split()[-1]:
        logger.error("API tests failed")
        return False
    
    logger.info("API tests passed")
    return True

def run_web_tests(output_dir):
    """
    Run Web UI tests.
    
    Args:
        output_dir: Directory to store test reports
        
    Returns:
        True if tests passed, False otherwise
    """
    logger.info("Running Web UI tests...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/screenshots", exist_ok=True)
    
    # Run Web UI tests
    command = f"pytest web_tests/ -v --html={output_dir}/web_test_report.html"
    output = run_command(command)
    
    if output is None:
        return False
    
    # Check if tests passed
    if "failed" in output and "failed" not in output.split()[-1]:
        logger.error("Web UI tests failed")
        return False
    
    logger.info("Web UI tests passed")
    return True

def run_performance_tests(output_dir, host, users=10, spawn_rate=1, duration="1m"):
    """
    Run performance tests.
    
    Args:
        output_dir: Directory to store test reports
        host: API host URL
        users: Number of users to simulate
        spawn_rate: Rate at which users are spawned
        duration: Test duration
        
    Returns:
        True if tests passed, False otherwise
    """
    logger.info("Running performance tests...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Run API load tests
    logger.info("Running API load tests...")
    command = (f"cd performance_tests && "
               f"locust -f locustfiles/api_load_test.py --headless "
               f"-u {users} -r {spawn_rate} -t {duration} "
               f"--html={output_dir}/api_load_test_report.html "
               f"--host={host}")
    
    if run_command(command) is None:
        return False
    
    # Run Web load tests (if Chrome is installed)
    if run_command("google-chrome --version") is not None:
        logger.info("Running Web load tests...")
        command = (f"cd performance_tests && "
                   f"locust -f locustfiles/web_load_test.py --headless "
                   f"-u {users // 2} -r {spawn_rate} -t {duration} "
                   f"--html={output_dir}/web_load_test_report.html")
        
        if run_command(command) is None:
            return False
    
    # Run stress tests
    logger.info("Running stress tests...")
    command = (f"cd performance_tests && "
               f"locust -f locustfiles/stress_test.py --headless "
               f"-u {users * 2} -r {spawn_rate * 5} -t {duration} "
               f"--html={output_dir}/stress_test_report.html "
               f"--host={host}")
    
    if run_command(command) is None:
        return False
    
    logger.info("Performance tests completed")
    return True

def main():
    """
    Main function to run tests.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Crypto QA Framework tests")
    parser.add_argument("--test-type", choices=["api", "web", "performance", "all"], 
                        default="all", help="Type of tests to run")
    parser.add_argument("--output-dir", default="reports", 
                        help="Directory to store test reports")
    parser.add_argument("--api-host", default="https://sandbox-api.coinmarketcap.com", 
                        help="API host URL for performance tests")
    parser.add_argument("--users", type=int, default=10, 
                        help="Number of users to simulate in performance tests")
    parser.add_argument("--spawn-rate", type=int, default=1, 
                        help="Rate at which users are spawned in performance tests")
    parser.add_argument("--duration", default="1m", 
                        help="Duration of performance tests")
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed. Please install required dependencies.")
        sys.exit(1)
    
    # Create timestamp for reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{args.output_dir}/{timestamp}"
    
    # Run tests based on test type
    success = True
    
    if args.test_type in ["api", "all"]:
        if not run_api_tests(output_dir):
            success = False
    
    if args.test_type in ["web", "all"]:
        if not run_web_tests(output_dir):
            success = False
    
    if args.test_type in ["performance", "all"]:
        if not run_performance_tests(output_dir, args.api_host, 
                                    args.users, args.spawn_rate, args.duration):
            success = False
    
    # Print summary
    logger.info(f"Test reports saved to: {output_dir}")
    
    if success:
        logger.info("All tests completed successfully")
        sys.exit(0)
    else:
        logger.error("Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
