#!/bin/bash

# Soul Foods Dash Application Test Runner
# This script automatically runs the test suite for the Soul Foods application
# Designed for CI/CD integration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        print_error "Virtual environment 'venv' not found!"
        print_status "Please create a virtual environment first:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
}

# Function to check if required files exist
check_files() {
    local missing_files=()
    
    if [ ! -f "app.py" ]; then
        missing_files+=("app.py")
    fi
    
    if [ ! -f "simple_test.py" ]; then
        missing_files+=("simple_test.py")
    fi
    
    if [ ! -f "formatted_sales_data.csv" ]; then
        missing_files+=("formatted_sales_data.csv")
    fi
    
    if [ ${#missing_files[@]} -ne 0 ]; then
        print_error "Missing required files: ${missing_files[*]}"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    print_status "Running Soul Foods Dash Application Test Suite..."
    echo "============================================================"
    
    # Activate virtual environment and run tests
    if source venv/bin/activate && python simple_test.py; then
        print_success "All tests passed successfully!"
        echo "============================================================"
        return 0
    else
        print_error "Tests failed!"
        echo "============================================================"
        return 1
    fi
}

# Function to run comprehensive tests (optional)
run_comprehensive_tests() {
    if [ "$1" = "--comprehensive" ]; then
        print_status "Running comprehensive test suite..."
        echo "============================================================"
        
        if source venv/bin/activate && python test_app.py; then
            print_success "All comprehensive tests passed successfully!"
            echo "============================================================"
            return 0
        else
            print_error "Comprehensive tests failed!"
            echo "============================================================"
            return 1
        fi
    fi
}

# Main execution
main() {
    echo "🧪 Soul Foods Dash Application Test Runner"
    echo "============================================================"
    
    # Check if we're in the right directory
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found. Please run this script from the project root directory."
        exit 1
    fi
    
    # Check for required files
    print_status "Checking for required files..."
    check_files
    print_success "All required files found"
    
    # Check virtual environment
    print_status "Checking virtual environment..."
    check_venv
    print_success "Virtual environment found"
    
    # Run comprehensive tests if requested
    if [ "$1" = "--comprehensive" ]; then
        run_comprehensive_tests "$1"
        exit $?
    fi
    
    # Run standard tests
    run_tests
    exit $?
}

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --comprehensive    Run comprehensive test suite (includes advanced tests)"
    echo "  --help, -h         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                 Run standard test suite"
    echo "  $0 --comprehensive Run comprehensive test suite"
    echo ""
    echo "Exit Codes:"
    echo "  0                  All tests passed"
    echo "  1                  Tests failed or error occurred"
}

# Parse command line arguments
case "$1" in
    --help|-h)
        show_help
        exit 0
        ;;
    --comprehensive)
        main "$1"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac 