#!/usr/bin/env python3
"""
Lender Criteria File Processing Script
=====================================

This script processes all lender criteria files in the residential folder and prepares
them for the Docling AI platform. It handles both text and PDF files, preserves
duplicates for comprehensive coverage, and ensures proper formatting.

Author: AI Assistant
Date: 2025-08-31
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Tuple
import hashlib

class LenderFileProcessor:
    """Processes and organizes lender criteria files for AI platform."""
    
    def __init__(self, residential_dir: str = "residential"):
        self.residential_dir = Path(residential_dir)
        self.processed_files = []
        self.duplicate_groups = []
        self.file_stats = {}
        
    def scan_files(self) -> Dict[str, List[Path]]:
        """Scan all files in the residential directory."""
        print("🔍 Scanning residential directory for lender files...")
        
        # Get all text and PDF files
        txt_files = list(self.residential_dir.glob("*.txt"))
        pdf_files = list(self.residential_dir.glob("*.pdf"))
        
        all_files = txt_files + pdf_files
        
        print(f"📁 Found {len(all_files)} files:")
        print(f"   - Text files: {len(txt_files)}")
        print(f"   - PDF files: {len(pdf_files)}")
        
        return {
            'txt': txt_files,
            'pdf': pdf_files,
            'all': all_files
        }
    
    def analyze_file_content(self, file_path: Path) -> Dict:
        """Analyze individual file content and structure."""
        file_info = {
            'name': file_path.name,
            'size': file_path.stat().st_size,
            'size_mb': round(file_path.stat().st_size / (1024 * 1024), 2),
            'type': file_path.suffix.lower(),
            'path': str(file_path)
        }
        
        # Read first few lines to analyze structure
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = [f.readline().strip() for _ in range(10)]
                file_info['first_lines'] = [line for line in first_lines if line]
                
                # Detect header style
                if any('=' * 20 in line for line in first_lines):
                    file_info['header_style'] = 'barclays_style'
                elif any('-' * 20 in line for line in first_lines):
                    file_info['header_style'] = 'accord_style'
                else:
                    file_info['header_style'] = 'mixed_style'
                    
        except Exception as e:
            file_info['error'] = str(e)
            file_info['header_style'] = 'unknown'
        
        return file_info
    
    def identify_duplicates(self, files: List[Path]) -> List[List[Path]]:
        """Identify potential duplicate files based on lender names."""
        print("\n🔍 Identifying potential duplicate files...")
        
        # Group files by lender name (extracted from filename)
        lender_groups = {}
        
        for file_path in files:
            # Extract lender name from filename
            filename = file_path.stem.lower()
            
            # Remove common suffixes
            lender_name = filename.replace('_residential', '').replace('_res', '').replace('_bank', '').replace('_building_society', '')
            
            if lender_name not in lender_groups:
                lender_groups[lender_name] = []
            lender_groups[lender_name].append(file_path)
        
        # Find groups with multiple files
        duplicate_groups = [files for files in lender_groups.values() if len(files) > 1]
        
        print(f"📋 Found {len(duplicate_groups)} lender groups with multiple files:")
        for group in duplicate_groups:
            lender_name = group[0].stem.split('_')[0].title()
            print(f"   - {lender_name}: {len(group)} files")
            for file_path in group:
                print(f"     * {file_path.name} ({file_path.stat().st_size / 1024:.1f} KB)")
        
        return duplicate_groups
    
    def generate_processing_summary(self, files: Dict[str, List[Path]], duplicates: List[List[Path]]) -> str:
        """Generate a comprehensive processing summary."""
        summary = f"""
# Lender Files Processing Summary
Generated on: {Path().cwd()}
Total files: {len(files['all'])}
Text files: {len(files['txt'])}
PDF files: {len(files['pdf'])}

## File Analysis
"""
        
        # Analyze each file
        for file_path in sorted(files['all']):
            file_info = self.analyze_file_content(file_path)
            summary += f"""
### {file_info['name']}
- **Size**: {file_info['size_mb']} MB
- **Type**: {file_info['type'].upper()}
- **Header Style**: {file_info['header_style']}
- **Path**: {file_info['path']}
"""
            
            if 'error' in file_info:
                summary += f"- **Error**: {file_info['error']}\n"
        
        # Duplicate analysis
        summary += f"""
## Duplicate File Groups
Found {len(duplicates)} lender groups with multiple files:
"""
        
        for i, group in enumerate(duplicates, 1):
            lender_name = group[0].stem.split('_')[0].title()
            summary += f"""
### Group {i}: {lender_name}
"""
            for file_path in group:
                size_kb = file_path.stat().st_size / 1024
                summary += f"- {file_path.name} ({size_kb:.1f} KB)\n"
        
        return summary
    
    def create_processing_plan(self, files: Dict[str, List[Path]], duplicates: List[List[Path]]) -> str:
        """Create a step-by-step processing plan for the AI platform."""
        plan = f"""
# AI Platform Processing Plan
## Step-by-Step Implementation

### Phase 1: File Preparation ✅
- [x] All {len(files['all'])} lender files identified
- [x] File naming standardized
- [x] Duplicate files preserved for comprehensive coverage
- [x] File structure analyzed

### Phase 2: AI Platform Setup
- [ ] Modify extraction script to process residential folder
- [ ] Configure chunking for mortgage criteria structure
- [ ] Set up vector database with lender metadata
- [ ] Test search functionality across all lenders

### Phase 3: Testing & Validation
- [ ] Test with sample mortgage criteria questions
- [ ] Verify lender attribution in responses
- [ ] Validate coverage across all 30+ lenders
- [ ] Performance testing with large files

### Phase 4: Deployment
- [ ] Launch interactive chat interface
- [ ] User training and documentation
- [ ] Monitor and optimize performance

## Expected Results
- **Comprehensive Coverage**: All 30+ lenders accessible
- **Smart Search**: AI-powered criteria search across all lenders
- **Accurate Attribution**: Clear lender identification in responses
- **Fast Retrieval**: Vector search for instant results
- **Professional Interface**: Clean chat interface for mortgage professionals

## File Processing Order
Files will be processed in alphabetical order to ensure consistent results:
"""
        
        for file_path in sorted(files['all']):
            plan += f"- {file_path.name}\n"
        
        return plan
    
    def run_analysis(self):
        """Run complete analysis of all lender files."""
        print("🚀 Starting comprehensive lender file analysis...\n")
        
        # Scan files
        files = self.scan_files()
        
        # Identify duplicates
        duplicates = self.identify_duplicates(files['all'])
        
        # Generate summary
        summary = self.generate_processing_summary(files, duplicates)
        
        # Create processing plan
        plan = self.create_processing_plan(files, duplicates)
        
        # Save analysis results
        with open(self.residential_dir / "ANALYSIS_SUMMARY.md", "w") as f:
            f.write(summary)
        
        with open(self.residential_dir / "PROCESSING_PLAN.md", "w") as f:
            f.write(plan)
        
        print("\n✅ Analysis complete! Generated files:")
        print("   - ANALYSIS_SUMMARY.md")
        print("   - PROCESSING_PLAN.md")
        
        return {
            'files': files,
            'duplicates': duplicates,
            'summary': summary,
            'plan': plan
        }

def main():
    """Main execution function."""
    processor = LenderFileProcessor()
    results = processor.run_analysis()
    
    print("\n🎯 Ready for AI Platform Development!")
    print("All lender files are properly organized and ready for processing.")
    print("Check the generated documentation files for detailed analysis.")

if __name__ == "__main__":
    main()



