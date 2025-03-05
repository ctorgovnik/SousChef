#!/bin/bash

set -eo pipefail

TEST_DIR="tests"
VERBOSE=false
EXIT_CODE=0
TEST_TYPE="all"

usage() {
    echo "Usage: $0 [options] [test_name...]"
    echo "Options:"
    echo "  -h, --help           Display this help message"
    echo "  -v, --verbose        Run tests with verbose output"
    echo "  -d, --dir DIR        Specify test directory (default: tests)"
    echo "  -i, --integration    Run only integration tests"
    echo "  -u, --unit           Run only unit tests (non-integration)"
    echo ""
    echo "If no test_name is provided, all tests will be run."
    exit 1
}

TESTS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dir)
            TEST_DIR="$2"
            shift 2
            ;;
        -i|--integration)
            TEST_TYPE="integration"
            shift
            ;;
        -u|--unit)
            TEST_TYPE="unit"
            shift
            ;;
        *)
            TESTS+=("$1")
            shift
            ;;
    esac
done

add_tests() {
    if [ "$TEST_TYPE" = "all" ]; then
       continue
    elif [ "$TEST_TYPE" = "integration" ]; then
        TESTS+=("test_chat_integration")
    elif [ "$TEST_TYPE" = "unit" ]; then
        TESTS+=("test_chat_endpoints" "test_settings")
    fi
}
    
run_tests() {
    local test_pattern=$1
    echo "Running tests matching pattern: $test_pattern"
    if [ "$VERBOSE" = true ]; then
        if python -m pytest "$TEST_DIR" -v -k "$test_pattern"; then
            echo "✅ Tests for '$test_pattern' passed successfully"
        else
            echo "❌ Tests for '$test_pattern' failed"
            EXIT_CODE=1
        fi
    else
        if python -m pytest "$TEST_DIR" -k "$test_pattern"; then
            echo "✅ Tests for '$test_pattern' passed successfully"
        else
            echo "❌ Tests for '$test_pattern' failed"
            EXIT_CODE=1
        fi
    fi
    echo ""
}

echo "=== Running Tests ==="

set +e

# Add tests based on test type
add_tests

if [ ${#TESTS[@]} -eq 0 ]; then
    # Run all tests if none specified
    echo "Running all tests in $TEST_DIR"
    if [ "$VERBOSE" = true ]; then
        if python -m pytest "$TEST_DIR" -v; then
            echo "✅ All tests passed successfully"
        else
            echo "❌ Some tests failed"
            EXIT_CODE=1
        fi
    else
        if python -m pytest "$TEST_DIR"; then
            echo "✅ All tests passed successfully"
        else
            echo "❌ Some tests failed"
            EXIT_CODE=1
        fi
    fi
else
    # Run specified tests
    for test in "${TESTS[@]}"; do
        run_tests "$test"
    done
fi

echo "=== Tests Complete ==="

exit $EXIT_CODE