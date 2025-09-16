# Background Manager Tool

A Python tool for managing background images across LWSWG documentation pages before runtime.

## Overview

The Background Manager Tool allows you to automatically assign different background images to documentation pages based on categories, specific pages, or intelligent suggestions. This ensures consistent visual theming across your documentation while maintaining flexibility.

## Features

- **Category-based assignment**: Assign backgrounds to entire categories of pages
- **Page-specific assignment**: Target individual pages
- **Smart assignment**: Automatically assign appropriate backgrounds based on content category
- **Random assignment**: Randomly distribute backgrounds across all pages
- **Reset functionality**: Return all pages to default background
- **List and inspect**: View current background assignments

## Available Backgrounds

| Class | Description | Image File |
|-------|-------------|------------|
| `bg-forest` | Forest path with wildflowers | background2.png |
| `bg-park` | People walking in park | background3.png |
| `bg-urban` | Cityscape with walking path | background4.png |
| `bg-city-park` | Urban park with skyline | background5.png |
| `bg-original` | Original background | background.jpg |

## Available Categories

| Category | Files | Suggested Backgrounds |
|----------|-------|----------------------|
| `design` | 6 files | bg-park, bg-urban |
| `methods` | 6 files | bg-forest, bg-original |
| `place` | 8 files | bg-forest, bg-city-park |
| `systems` | 6 files | bg-urban, bg-city-park |
| `resources` | 3 files | bg-original, bg-park |

## Usage

### Basic Commands

```bash
# Show help
python3 background_manager.py --help

# List all available backgrounds
python3 background_manager.py backgrounds

# List all available categories
python3 background_manager.py categories

# List current background assignments
python3 background_manager.py list
```

### Assignment Commands

#### Category-based Assignment
Assign a background to all pages in a specific category:

```bash
# Assign bg-park to all design pages
python3 background_manager.py assign --category design --background bg-park

# Assign bg-urban to all systems pages
python3 background_manager.py assign --category systems --background bg-urban
```

#### Page-specific Assignment
Assign a background to a specific page:

```bash
# Assign bg-city-park to visual-cues.html
python3 background_manager.py assign --page "visual-cues.html" --background bg-city-park

# Assign bg-forest to checklist.html
python3 background_manager.py assign --page "checklist.html" --background bg-forest
```

#### Smart Assignment
Automatically assign appropriate backgrounds based on content category:

```bash
python3 background_manager.py assign --smart
```

#### Random Assignment
Randomly assign backgrounds to all pages:

```bash
python3 background_manager.py assign --random
```

#### Reset
Reset all pages to the default background (bg-forest):

```bash
python3 background_manager.py reset
```

## Examples

### Scenario 1: Thematic Organization
You want to organize backgrounds by theme:

```bash
# Design pages get urban backgrounds
python3 background_manager.py assign --category design --background bg-urban

# Place-related pages get natural backgrounds
python3 background_manager.py assign --category place --background bg-forest

# Systems pages get city park backgrounds
python3 background_manager.py assign --category systems --background bg-city-park
```

### Scenario 2: Quick Randomization
You want to quickly randomize all backgrounds for variety:

```bash
python3 background_manager.py assign --random
```

### Scenario 3: Smart Theming
You want intelligent background assignment based on content:

```bash
python3 background_manager.py assign --smart
```

### Scenario 4: Individual Page Customization
You want to customize specific pages:

```bash
# Make the checklist page stand out
python3 background_manager.py assign --page "checklist.html" --background bg-city-park

# Give the main index a special background
python3 background_manager.py assign --page "index.html" --background bg-original
```

## Adding New Backgrounds

To add new background images:

1. **Add the image file** to the `/images/` directory (e.g., `background6.png`)

2. **Add CSS class** in `/css/custom.css`:
   ```css
   #main-header.bg-new-background {
       background-image: url("../images/background6.png");
   }
   ```

3. **Update the tool** by modifying `background_manager.py`:
   ```python
   self.backgrounds = {
       # ... existing backgrounds ...
       "bg-new-background": "Description of new background (background6.png)"
   }
   ```

4. **Update documentation** in the CSS file comments

## File Structure

```
LWSWG/
├── background_manager.py          # Main tool script
├── css/
│   └── custom.css                # Background CSS definitions
├── documentation/                 # Target directory for background changes
│   ├── design/                   # Design category pages
│   ├── methods-and-evaluation/   # Methods category pages
│   ├── place-and-walking/        # Place category pages
│   ├── leisure-walking-systems/   # Systems category pages
│   └── resources/                 # Resources category pages
└── images/                       # Background image files
    ├── background.jpg
    ├── background2.png
    ├── background3.png
    ├── background4.png
    └── background5.png
```

## Technical Details

- **File Detection**: Automatically finds all `.html` files in the documentation directory
- **Pattern Matching**: Uses regex to find and replace `id="main-header" class="..."` attributes
- **Backup Safety**: Original files are modified in-place (consider backing up before major changes)
- **Error Handling**: Gracefully handles file access errors and invalid inputs

## Troubleshooting

### Common Issues

1. **"Unknown category" error**: Check available categories with `python3 background_manager.py categories`

2. **"Unknown background" error**: Check available backgrounds with `python3 background_manager.py backgrounds`

3. **"Page not found" error**: Ensure the page name includes the `.html` extension

4. **Permission errors**: Ensure the script has write permissions to the documentation directory

### Verification

After running assignments, verify changes with:

```bash
python3 background_manager.py list
```

This will show all files and their current background classes.

## Integration

This tool is designed to be run before deploying your documentation site. Consider integrating it into your build process or running it manually when you want to change the visual theme of your documentation.

---

*Created for the Leisure Walking Systems Working Group (LWSWG) documentation system.*
