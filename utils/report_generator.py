import os
import json
import datetime
import logging
from typing import Dict, Any, Optional, List, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Report Generator for test results.
    
    This class provides methods for generating test reports in various formats
    such as HTML, JSON, and CSV.
    """
    
    def __init__(self, report_dir: str = None):
        """
        Initialize the ReportGenerator.
        
        Args:
            report_dir: Directory to save reports. If None, uses the default path.
        """
        if report_dir is None:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the project root
            project_root = os.path.dirname(current_dir)
            # Default report directory
            report_dir = os.path.join(project_root, 'reports')
        
        self.report_dir = report_dir
        
        # Create report directory if it doesn't exist
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_json_report(self, test_results: Dict[str, Any], 
                            report_name: str = None) -> str:
        """
        Generate a JSON report from test results.
        
        Args:
            test_results: Dictionary containing test results
            report_name: Name of the report file (without extension)
            
        Returns:
            Path to the generated report file
        """
        if report_name is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            report_name = f"test_report_{timestamp}"
        
        # Ensure the filename has .json extension
        if not report_name.endswith('.json'):
            report_name += '.json'
        
        report_path = os.path.join(self.report_dir, report_name)
        
        # Add timestamp to the report
        test_results['timestamp'] = datetime.datetime.now().isoformat()
        
        try:
            with open(report_path, 'w') as f:
                json.dump(test_results, f, indent=2)
            
            logger.info(f"JSON report generated: {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Error generating JSON report: {e}")
            return ""
    
    def generate_html_report(self, test_results: Dict[str, Any], 
                           report_name: str = None) -> str:
        """
        Generate an HTML report from test results.
        
        Args:
            test_results: Dictionary containing test results
            report_name: Name of the report file (without extension)
            
        Returns:
            Path to the generated report file
        """
        if report_name is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            report_name = f"test_report_{timestamp}"
        
        # Ensure the filename has .html extension
        if not report_name.endswith('.html'):
            report_name += '.html'
        
        report_path = os.path.join(self.report_dir, report_name)
        
        try:
            # Create HTML content
            html_content = self._create_html_content(test_results)
            
            with open(report_path, 'w') as f:
                f.write(html_content)
            
            logger.info(f"HTML report generated: {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            return ""
    
    def generate_csv_report(self, test_results: Dict[str, Any], 
                          report_name: str = None) -> str:
        """
        Generate a CSV report from test results.
        
        Args:
            test_results: Dictionary containing test results
            report_name: Name of the report file (without extension)
            
        Returns:
            Path to the generated report file
        """
        if report_name is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            report_name = f"test_report_{timestamp}"
        
        # Ensure the filename has .csv extension
        if not report_name.endswith('.csv'):
            report_name += '.csv'
        
        report_path = os.path.join(self.report_dir, report_name)
        
        try:
            # Extract test cases
            test_cases = test_results.get('test_cases', [])
            
            if not test_cases:
                logger.warning("No test cases found in test results")
                return ""
            
            # Create CSV content
            csv_content = "Test Name,Status,Duration,Error Message\n"
            
            for test_case in test_cases:
                test_name = test_case.get('name', 'Unknown')
                status = test_case.get('status', 'Unknown')
                duration = test_case.get('duration', 0)
                error_message = test_case.get('error_message', '')
                
                # Escape commas in fields
                test_name = f'"{test_name}"' if ',' in test_name else test_name
                error_message = f'"{error_message}"' if ',' in error_message else error_message
                
                csv_content += f"{test_name},{status},{duration},{error_message}\n"
            
            with open(report_path, 'w') as f:
                f.write(csv_content)
            
            logger.info(f"CSV report generated: {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Error generating CSV report: {e}")
            return ""
    
    def _create_html_content(self, test_results: Dict[str, Any]) -> str:
        """
        Create HTML content from test results.
        
        Args:
            test_results: Dictionary containing test results
            
        Returns:
            HTML content as a string
        """
        # Extract test summary
        summary = test_results.get('summary', {})
        total = summary.get('total', 0)
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        skipped = summary.get('skipped', 0)
        duration = summary.get('duration', 0)
        
        # Calculate pass rate
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # Extract test cases
        test_cases = test_results.get('test_cases', [])
        
        # Create HTML content
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ margin: 20px 0; padding: 10px; background-color: #f5f5f5; border-radius: 5px; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .skipped {{ color: orange; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <h1>Test Report</h1>
            <div class="summary">
                <h2>Test Summary</h2>
                <p>Total Tests: <strong>{total}</strong></p>
                <p>Passed: <strong class="passed">{passed}</strong></p>
                <p>Failed: <strong class="failed">{failed}</strong></p>
                <p>Skipped: <strong class="skipped">{skipped}</strong></p>
                <p>Pass Rate: <strong>{pass_rate:.2f}%</strong></p>
                <p>Duration: <strong>{duration:.2f} seconds</strong></p>
                <p>Timestamp: <strong>{test_results.get('timestamp', datetime.datetime.now().isoformat())}</strong></p>
            </div>
            
            <h2>Test Results</h2>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                    <th>Error Message</th>
                </tr>
        """
        
        # Add test cases to the table
        for test_case in test_cases:
            test_name = test_case.get('name', 'Unknown')
            status = test_case.get('status', 'Unknown')
            duration = test_case.get('duration', 0)
            error_message = test_case.get('error_message', '')
            
            status_class = ''
            if status.lower() == 'passed':
                status_class = 'passed'
            elif status.lower() == 'failed':
                status_class = 'failed'
            elif status.lower() == 'skipped':
                status_class = 'skipped'
            
            html += f"""
                <tr>
                    <td>{test_name}</td>
                    <td class="{status_class}">{status}</td>
                    <td>{duration:.2f}</td>
                    <td>{error_message}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html
    
    def combine_reports(self, report_paths: List[str], 
                       output_name: str = "combined_report") -> str:
        """
        Combine multiple HTML reports into a single report.
        
        Args:
            report_paths: List of paths to HTML reports
            output_name: Name of the combined report file (without extension)
            
        Returns:
            Path to the combined report file
        """
        if not report_paths:
            logger.warning("No reports to combine")
            return ""
        
        # Ensure the output filename has .html extension
        if not output_name.endswith('.html'):
            output_name += '.html'
        
        output_path = os.path.join(self.report_dir, output_name)
        
        try:
            # Create combined HTML content
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Combined Test Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #333; }}
                    .report-container {{ margin: 20px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                    iframe {{ width: 100%; height: 600px; border: none; }}
                </style>
            </head>
            <body>
                <h1>Combined Test Report</h1>
                <p>Generated on: {datetime.datetime.now().isoformat()}</p>
                
                <h2>Individual Reports</h2>
            """
            
            # Add links to individual reports
            for i, report_path in enumerate(report_paths):
                report_name = os.path.basename(report_path)
                html += f"""
                <div class="report-container">
                    <h3>Report {i+1}: {report_name}</h3>
                    <iframe src="{report_path}"></iframe>
                </div>
                """
            
            html += """
            </body>
            </html>
            """
            
            with open(output_path, 'w') as f:
                f.write(html)
            
            logger.info(f"Combined report generated: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating combined report: {e}")
            return ""
