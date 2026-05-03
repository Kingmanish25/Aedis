"""
Service availability checker for validating dependencies before workflow execution.
"""

import os
import requests
from typing import Dict, List, Tuple


class ServiceChecker:
    """Check availability of required services"""
    
    @staticmethod
    def check_groq_api() -> Tuple[bool, str]:
        """
        Check if Groq API is accessible and API key is configured.
        
        Returns:
            (is_available, message)
        """
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            return False, "GROQ_API_KEY environment variable is not set"
        
        try:
            # Test API with a minimal request
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 5
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Groq API is accessible"
            elif response.status_code == 401:
                return False, "Groq API key is invalid"
            else:
                return False, f"Groq API returned status code {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Groq API request timed out"
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to Groq API - check internet connection"
        except Exception as e:
            return False, f"Groq API check failed: {str(e)}"
    
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
            "groq_api": ServiceChecker.check_groq_api(),
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
