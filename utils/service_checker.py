"""
Service availability checker for validating dependencies before workflow execution.
"""

import os
import requests
from typing import Dict, List, Tuple


class ServiceChecker:
    """Check availability of required services"""
    
    @staticmethod
    def check_watsonx_api() -> Tuple[bool, str]:
        """
        Check if IBM WatsonX API is accessible and credentials are configured.
        
        Returns:
            (is_available, message)
        """
        api_key = os.getenv('IBM_API_KEY')
        project_id = os.getenv('IBM_PROJECT_ID')
        
        if not api_key:
            return False, "IBM_API_KEY environment variable is not set"
        
        if not project_id:
            return False, "IBM_PROJECT_ID environment variable is not set"
        
        try:
            # Import WatsonX SDK
            from ibm_watsonx_ai.foundation_models import Model
            
            # Test API with minimal request
            model = Model(
                model_id="ibm/granite-13b-chat-v2",
                params={
                    "decoding_method": "greedy",
                    "max_new_tokens": 5,
                    "temperature": 0.5
                },
                credentials={
                    "apikey": api_key,
                    "url": os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
                },
                project_id=project_id
            )
            
            # Try a minimal generation
            response = model.generate_text("test")
            
            if response:
                return True, "WatsonX API is accessible"
            else:
                return False, "WatsonX API returned empty response"
                
        except ImportError:
            return False, "ibm-watsonx-ai package not installed. Run: pip install ibm-watsonx-ai"
        except Exception as e:
            error_msg = str(e)
            # Mask sensitive information in error messages
            if api_key and api_key in error_msg:
                error_msg = error_msg.replace(api_key, "***")
            return False, f"WatsonX API check failed: {error_msg}"
    
    @staticmethod
    def check_database(db_path: str) -> Tuple[bool, str]:
        """
        Check if database file exists and is accessible.
        
        Args:
            db_path: Path to the database file
            
        Returns:
            (is_available, message)
        """
        if not os.path.exists(db_path):
            return False, f"Database file not found at {db_path}"
        
        if not os.access(db_path, os.R_OK):
            return False, f"Database file at {db_path} is not readable"
        
        # Try to open with sqlite3
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            if not tables:
                return False, f"Database at {db_path} has no tables"
            
            return True, f"Database accessible with {len(tables)} table(s)"
            
        except Exception as e:
            return False, f"Database check failed: {str(e)}"
    
    @staticmethod
    def check_documents_directory(docs_path: str) -> Tuple[bool, str]:
        """
        Check if documents directory exists and contains files.
        
        Args:
            docs_path: Path to documents directory
            
        Returns:
            (is_available, message)
        """
        if not os.path.exists(docs_path):
            return False, f"Documents directory not found at {docs_path}"
        
        if not os.path.isdir(docs_path):
            return False, f"{docs_path} is not a directory"
        
        files = [f for f in os.listdir(docs_path) if os.path.isfile(os.path.join(docs_path, f))]
        
        if not files:
            return False, f"Documents directory at {docs_path} is empty"
        
        return True, f"Documents directory accessible with {len(files)} file(s)"
    
    @staticmethod
    def check_all_services() -> Dict[str, Tuple[bool, str]]:
        """
        Check all required services.
        
        Returns:
            Dict mapping service name to (is_available, message)
        """
        from app.config import Config
        
        results = {
            "watsonx_api": ServiceChecker.check_watsonx_api(),
            "database": ServiceChecker.check_database(Config.DB_PATH),
            "documents": ServiceChecker.check_documents_directory("data/documents")
        }
        
        return results
    
    @staticmethod
    def get_service_report() -> str:
        """
        Get a formatted report of all service statuses.
        
        Returns:
            Formatted string report
        """
        results = ServiceChecker.check_all_services()
        
        report_lines = ["Service Availability Report", "=" * 50]
        
        all_available = True
        for service, (available, message) in results.items():
            status = "✓ AVAILABLE" if available else "✗ UNAVAILABLE"
            report_lines.append(f"{service.upper()}: {status}")
            report_lines.append(f"  → {message}")
            if not available:
                all_available = False
        
        report_lines.append("=" * 50)
        
        if all_available:
            report_lines.append("All services are available ✓")
        else:
            report_lines.append("Some services are unavailable ✗")
        
        return "\n".join(report_lines)
    
    @staticmethod
    def validate_or_exit() -> None:
        """
        Check all services and exit if any are unavailable.
        Useful for startup validation.
        """
        import sys
        
        print("Checking service availability...")
        results = ServiceChecker.check_all_services()
        
        failed_services = []
        for service, (available, message) in results.items():
            if available:
                print(f"✓ {service}: {message}")
            else:
                print(f"✗ {service}: {message}")
                failed_services.append(service)
        
        if failed_services:
            print(f"\nError: The following services are unavailable: {', '.join(failed_services)}")
            print("Please fix the issues above before running the application.")
            sys.exit(1)
        
        print("\nAll services are available. Starting application...\n")

# Made with Bob
