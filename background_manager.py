#!/usr/bin/env python3
"""
Background Manager Tool for LWSWG Documentation

This tool allows you to assign different background images to documentation pages
before runtime. It can assign backgrounds based on categories, specific pages,
or random assignment.

Usage:
    python background_manager.py --help
    python background_manager.py assign --category design --background bg-park
    python background_manager.py assign --page "visual-cues.html" --background bg-urban
    python background_manager.py assign --random
    python background_manager.py list
    python background_manager.py reset
"""

import os
import re
import argparse
import random
from pathlib import Path
from typing import Dict, List, Optional

class BackgroundManager:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.documentation_dir = self.project_root / "documentation"
        self.css_file = self.project_root / "css" / "custom.css"
        
        # Available background classes
        self.backgrounds = {
            "bg-forest": "Forest path with wildflowers (background2.png)",
            "bg-park": "People walking in park (background3.png)",
            "bg-urban": "Cityscape with walking path (background4.png)",
            "bg-city-park": "Urban park with skyline (background5.png)",
            "bg-original": "Original background (background.jpg)"
        }
        
        # Category mappings for automatic assignment
        self.categories = {
            "design": ["visual-cues.html", "accessibility.html", "use-case-comparison.html", 
                      "route-interfaces.html", "slowness-and-serendipity.html", "user-experience.html"],
            "methods": ["research-methodology.html", "checklist.html", "evaluation-framework.html",
                       "subjective-vs-objective.html", "capturing-place-qualities.html", 
                       "ethical-considerations.html"],
            "place": ["place-representation.html", "platial-gis.html", "technical-architecture.html",
                     "designing-for-place.html", "case-studies-by-region.html", 
                     "mapping-place-qualities.html", "platial-vs-spatial.html", "cultural-dimensions.html"],
            "systems": ["recommendation-systems.html", "geospatial-integration.html", "route-algorithms.html",
                      "contextual-factors.html", "walkability-metrics.html", "app-types-comparison.html"],
            "resources": ["data-sharing.html", "templates-and-scripts.html", "glossary.html"]
        }
        
        # Background suggestions by category
        self.category_backgrounds = {
            "design": ["bg-park", "bg-urban"],
            "methods": ["bg-forest", "bg-original"],
            "place": ["bg-forest", "bg-city-park"],
            "systems": ["bg-urban", "bg-city-park"],
            "resources": ["bg-original", "bg-park"]
        }

    def find_html_files(self) -> List[Path]:
        """Find all HTML files in the documentation directory."""
        html_files = []
        for root, dirs, files in os.walk(self.documentation_dir):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(Path(root) / file)
        return html_files

    def get_relative_path(self, file_path: Path) -> str:
        """Get the relative path from documentation root."""
        return str(file_path.relative_to(self.documentation_dir))

    def update_file_background(self, file_path: Path, background_class: str) -> bool:
        """Update the background class in a specific HTML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace the main-header class
            pattern = r'(<div id="main-header" class=")[^"]*(">)'
            replacement = f'\\1{background_class}\\2'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
            return False
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
            return False

    def assign_by_category(self, category: str, background: str) -> int:
        """Assign background to all files in a category."""
        if category not in self.categories:
            print(f"Unknown category: {category}")
            print(f"Available categories: {', '.join(self.categories.keys())}")
            return 0
        
        if background not in self.backgrounds:
            print(f"Unknown background: {background}")
            print(f"Available backgrounds: {', '.join(self.backgrounds.keys())}")
            return 0
        
        files_updated = 0
        category_files = self.categories[category]
        
        for html_file in self.find_html_files():
            relative_path = self.get_relative_path(html_file)
            filename = os.path.basename(relative_path)
            
            if filename in category_files:
                if self.update_file_background(html_file, background):
                    print(f"Updated: {relative_path}")
                    files_updated += 1
        
        return files_updated

    def assign_by_page(self, page_name: str, background: str) -> bool:
        """Assign background to a specific page."""
        if background not in self.backgrounds:
            print(f"Unknown background: {background}")
            print(f"Available backgrounds: {', '.join(self.backgrounds.keys())}")
            return False
        
        for html_file in self.find_html_files():
            if html_file.name == page_name:
                if self.update_file_background(html_file, background):
                    print(f"Updated: {self.get_relative_path(html_file)}")
                    return True
                else:
                    print(f"No changes needed for: {self.get_relative_path(html_file)}")
                    return True
        
        print(f"Page not found: {page_name}")
        return False

    def assign_random(self) -> int:
        """Assign random backgrounds to all files."""
        files_updated = 0
        background_list = list(self.backgrounds.keys())
        
        for html_file in self.find_html_files():
            random_bg = random.choice(background_list)
            if self.update_file_background(html_file, random_bg):
                print(f"Updated: {self.get_relative_path(html_file)} -> {random_bg}")
                files_updated += 1
        
        return files_updated

    def assign_smart(self) -> int:
        """Assign backgrounds based on category suggestions."""
        files_updated = 0
        
        for html_file in self.find_html_files():
            relative_path = self.get_relative_path(html_file)
            filename = os.path.basename(relative_path)
            
            # Find which category this file belongs to
            assigned_bg = None
            for category, files in self.categories.items():
                if filename in files:
                    suggested_bgs = self.category_backgrounds.get(category, ["bg-forest"])
                    assigned_bg = random.choice(suggested_bgs)
                    break
            
            # If not in any category, use default
            if not assigned_bg:
                assigned_bg = "bg-forest"
            
            if self.update_file_background(html_file, assigned_bg):
                print(f"Updated: {relative_path} -> {assigned_bg}")
                files_updated += 1
        
        return files_updated

    def reset_all(self) -> int:
        """Reset all files to default background."""
        files_updated = 0
        
        for html_file in self.find_html_files():
            if self.update_file_background(html_file, "bg-forest"):
                print(f"Reset: {self.get_relative_path(html_file)}")
                files_updated += 1
        
        return files_updated

    def list_files(self):
        """List all HTML files and their current background classes."""
        print("Documentation files and their backgrounds:")
        print("-" * 60)
        
        for html_file in self.find_html_files():
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract current background class
                match = re.search(r'<div id="main-header" class="([^"]*)"', content)
                current_bg = match.group(1) if match else "unknown"
                
                relative_path = self.get_relative_path(html_file)
                print(f"{relative_path:<40} -> {current_bg}")
                
            except Exception as e:
                print(f"Error reading {html_file}: {e}")

    def list_backgrounds(self):
        """List all available background options."""
        print("Available background classes:")
        print("-" * 40)
        for bg_class, description in self.backgrounds.items():
            print(f"{bg_class:<15} - {description}")

    def list_categories(self):
        """List all available categories."""
        print("Available categories:")
        print("-" * 30)
        for category, files in self.categories.items():
            print(f"{category:<12} - {len(files)} files")
            suggested = self.category_backgrounds.get(category, [])
            if suggested:
                print(f"             Suggested backgrounds: {', '.join(suggested)}")

def main():
    parser = argparse.ArgumentParser(
        description="Background Manager for LWSWG Documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s assign --category design --background bg-park
  %(prog)s assign --page "visual-cues.html" --background bg-urban
  %(prog)s assign --random
  %(prog)s assign --smart
  %(prog)s list
  %(prog)s reset
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Assign command
    assign_parser = subparsers.add_parser('assign', help='Assign backgrounds to pages')
    assign_group = assign_parser.add_mutually_exclusive_group(required=True)
    assign_group.add_argument('--category', help='Assign to all files in a category')
    assign_group.add_argument('--page', help='Assign to a specific page')
    assign_group.add_argument('--random', action='store_true', help='Assign random backgrounds')
    assign_group.add_argument('--smart', action='store_true', help='Assign based on category suggestions')
    assign_parser.add_argument('--background', help='Background class to assign (required for category/page)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List files and their backgrounds')
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset all files to default background')
    
    # Info commands
    backgrounds_parser = subparsers.add_parser('backgrounds', help='List available backgrounds')
    categories_parser = subparsers.add_parser('categories', help='List available categories')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = BackgroundManager()
    
    if args.command == 'assign':
        if args.random:
            count = manager.assign_random()
            print(f"\nUpdated {count} files with random backgrounds")
        elif args.smart:
            count = manager.assign_smart()
            print(f"\nUpdated {count} files with smart category-based backgrounds")
        elif args.category:
            if not args.background:
                print("Error: --background is required when using --category")
                return
            count = manager.assign_by_category(args.category, args.background)
            print(f"\nUpdated {count} files in category '{args.category}' with background '{args.background}'")
        elif args.page:
            if not args.background:
                print("Error: --background is required when using --page")
                return
            success = manager.assign_by_page(args.page, args.background)
            if success:
                print(f"\nUpdated page '{args.page}' with background '{args.background}'")
    
    elif args.command == 'list':
        manager.list_files()
    
    elif args.command == 'reset':
        count = manager.reset_all()
        print(f"\nReset {count} files to default background")
    
    elif args.command == 'backgrounds':
        manager.list_backgrounds()
    
    elif args.command == 'categories':
        manager.list_categories()

if __name__ == "__main__":
    main()
