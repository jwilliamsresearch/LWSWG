#!/bin/bash
# Background Manager Wrapper Script
# Provides convenient shortcuts for common background management tasks

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show usage
show_usage() {
    print_color $BLUE "Background Manager - Quick Commands"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Quick Commands:"
    echo "  smart          - Smart assignment based on categories"
    echo "  random         - Random background assignment"
    echo "  reset          - Reset all to default (bg-forest)"
    echo "  list           - List current assignments"
    echo "  design [bg]    - Assign background to design pages"
    echo "  place [bg]     - Assign background to place pages"
    echo "  systems [bg]   - Assign background to systems pages"
    echo "  methods [bg]   - Assign background to methods pages"
    echo "  resources [bg] - Assign background to resources pages"
    echo ""
    echo "Available backgrounds:"
    echo "  forest, park, urban, city-park, original"
    echo ""
    echo "Examples:"
    echo "  $0 smart"
    echo "  $0 design park"
    echo "  $0 place forest"
    echo "  $0 random"
    echo ""
    echo "For full options, run: python3 background_manager.py --help"
}

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    print_color $RED "Error: python3 is not installed or not in PATH"
    exit 1
fi

# Check if background_manager.py exists
if [ ! -f "background_manager.py" ]; then
    print_color $RED "Error: background_manager.py not found in current directory"
    exit 1
fi

# Handle commands
case "$1" in
    "smart")
        print_color $GREEN "Running smart background assignment..."
        python3 background_manager.py assign --smart
        ;;
    "random")
        print_color $GREEN "Running random background assignment..."
        python3 background_manager.py assign --random
        ;;
    "reset")
        print_color $YELLOW "Resetting all backgrounds to default..."
        python3 background_manager.py reset
        ;;
    "list")
        python3 background_manager.py list
        ;;
    "design")
        if [ -z "$2" ]; then
            print_color $RED "Error: Please specify a background (forest, park, urban, city-park, original)"
            exit 1
        fi
        print_color $GREEN "Assigning bg-$2 to design pages..."
        python3 background_manager.py assign --category design --background "bg-$2"
        ;;
    "place")
        if [ -z "$2" ]; then
            print_color $RED "Error: Please specify a background (forest, park, urban, city-park, original)"
            exit 1
        fi
        print_color $GREEN "Assigning bg-$2 to place pages..."
        python3 background_manager.py assign --category place --background "bg-$2"
        ;;
    "systems")
        if [ -z "$2" ]; then
            print_color $RED "Error: Please specify a background (forest, park, urban, city-park, original)"
            exit 1
        fi
        print_color $GREEN "Assigning bg-$2 to systems pages..."
        python3 background_manager.py assign --category systems --background "bg-$2"
        ;;
    "methods")
        if [ -z "$2" ]; then
            print_color $RED "Error: Please specify a background (forest, park, urban, city-park, original)"
            exit 1
        fi
        print_color $GREEN "Assigning bg-$2 to methods pages..."
        python3 background_manager.py assign --category methods --background "bg-$2"
        ;;
    "resources")
        if [ -z "$2" ]; then
            print_color $RED "Error: Please specify a background (forest, park, urban, city-park, original)"
            exit 1
        fi
        print_color $GREEN "Assigning bg-$2 to resources pages..."
        python3 background_manager.py assign --category resources --background "bg-$2"
        ;;
    "help"|"-h"|"--help"|"")
        show_usage
        ;;
    *)
        # Pass through to the main Python script
        python3 background_manager.py "$@"
        ;;
esac
