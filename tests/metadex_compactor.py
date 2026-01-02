#!/usr/bin/env python3
"""
StashKit MetaDex Compactor
Drag a JSON file onto this script to generate an ultra-compact, LLM-optimized version.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Union


class MetaDexCompactor:
    """Generate ultra-compact, deterministic, LLM-friendly format from JSON"""
    
    def __init__(self):
        self.indent = "  "
        
    def compact(self, json_path: Path) -> str:
        """Main compaction logic - deterministic output"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Sort all dicts for determinism
        data = self._sort_recursive(data)
        
        # Detect document type and use appropriate template
        if 'metadex' in data:
            return self._compact_metadex(data)
        else:
            return self._compact_generic(data)
    
    def _sort_recursive(self, obj: Any) -> Any:
        """Recursively sort all dicts for deterministic output"""
        if isinstance(obj, dict):
            return {k: self._sort_recursive(v) for k, v in sorted(obj.items())}
        elif isinstance(obj, list):
            return [self._sort_recursive(item) for item in obj]
        return obj
    
    # ═══════════════════════════════════════════════════════
    # MetaDex-Specific Compaction
    # ═══════════════════════════════════════════════════════
    
    def _compact_metadex(self, data: Dict) -> str:
        """Compact StashKit MetaDex format"""
        lines = []
        
        # Header
        meta = data.get('metadex', {})
        lines.append(f"# {meta.get('name', 'Unknown')} v{meta.get('version', '?')}")
        if 'scope' in meta:
            lines.append(f"Scope: {meta['scope']}")
        if 'purpose' in meta:
            lines.append(f"Purpose: {meta['purpose']}")
        if 'status' in meta:
            lines.append(f"Status: {meta['status']}")
        lines.append("")
        
        # Conceptual Model
        if 'conceptual_model' in data:
            lines.append("## CONCEPTUAL MODEL")
            cm = data['conceptual_model']
            
            for section_name in sorted(cm.keys()):
                section = cm[section_name]
                lines.append(f"\n{section_name.upper()}:")
                
                if isinstance(section, dict):
                    if 'description' in section:
                        lines.append(f"{self.indent}{section['description']}")
                    
                    if 'guarantees' in section:
                        for g in section['guarantees']:
                            lines.append(f"{self.indent}✓ {g}")
                    
                    # Handle any other fields
                    for key in sorted(section.keys()):
                        if key not in ['description', 'guarantees']:
                            lines.append(f"{self.indent}{key}: {self._format_value(section[key])}")
            
            lines.append("")
        
        # StashKit section
        if 'stashkit' in data:
            lines.append("## STASHKIT")
            sk = data['stashkit']
            
            for component_name in sorted(sk.keys()):
                component = sk[component_name]
                lines.append(f"\n{component_name.upper()}:")
                
                if isinstance(component, dict):
                    if 'description' in component:
                        lines.append(f"{self.indent}{component['description']}")
                    
                    # Handle nested structures
                    for key in sorted(component.keys()):
                        if key == 'description':
                            continue
                        
                        value = component[key]
                        
                        if isinstance(value, list):
                            lines.append(f"{self.indent}{key}:")
                            for item in value:
                                lines.append(f"{self.indent}{self.indent}→ {item}")
                        
                        elif isinstance(value, dict):
                            lines.append(f"{self.indent}{key}:")
                            self._format_nested_dict(value, lines, depth=2)
                        
                        else:
                            lines.append(f"{self.indent}{key}: {value}")
        
        # Extension model
        if 'extension_model' in data:
            lines.append("\n## EXTENSION MODEL")
            em = data['extension_model']
            for key in sorted(em.keys()):
                lines.append(f"\n{key.upper()}:")
                self._format_nested_dict(em[key], lines, depth=1)
        
        return '\n'.join(lines)
    
    # ═══════════════════════════════════════════════════════
    # Generic Compaction (for any JSON)
    # ═══════════════════════════════════════════════════════
    
    def _compact_generic(self, data: Dict) -> str:
        """Compact any JSON into readable format"""
        lines = []
        
        # Try to find a title
        title = data.get('name') or data.get('title') or 'Document'
        version = data.get('version', '')
        if version:
            lines.append(f"# {title} v{version}")
        else:
            lines.append(f"# {title}")
        lines.append("")
        
        # Render all top-level keys
        for key in sorted(data.keys()):
            if key in ['name', 'title', 'version']:
                continue
            
            lines.append(f"## {key.upper().replace('_', ' ')}")
            self._format_nested_dict(data[key], lines, depth=0)
            lines.append("")
        
        return '\n'.join(lines)
    
    # ═══════════════════════════════════════════════════════
    # Formatting Helpers
    # ═══════════════════════════════════════════════════════
    
    def _format_nested_dict(self, d: Any, lines: List[str], depth: int):
        """Format nested dictionary structures"""
        prefix = self.indent * (depth + 1)
        
        if isinstance(d, dict):
            for key in sorted(d.keys()):
                value = d[key]
                
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    self._format_nested_dict(value, lines, depth + 1)
                
                elif isinstance(value, list):
                    if len(value) == 0:
                        lines.append(f"{prefix}{key}: []")
                    elif all(isinstance(x, str) for x in value):
                        # Inline simple lists
                        if sum(len(str(x)) for x in value) < 60:
                            lines.append(f"{prefix}{key}: {' | '.join(value)}")
                        else:
                            lines.append(f"{prefix}{key}:")
                            for item in value:
                                lines.append(f"{prefix}{self.indent}• {item}")
                    else:
                        lines.append(f"{prefix}{key}:")
                        for item in value:
                            if isinstance(item, dict):
                                self._format_nested_dict(item, lines, depth + 1)
                            else:
                                lines.append(f"{prefix}{self.indent}• {item}")
                
                else:
                    lines.append(f"{prefix}{key}: {value}")
        
        elif isinstance(d, list):
            for item in d:
                if isinstance(item, dict):
                    self._format_nested_dict(item, lines, depth)
                else:
                    lines.append(f"{prefix}• {item}")
        
        else:
            lines.append(f"{prefix}{d}")
    
    def _format_value(self, value: Any) -> str:
        """Format a single value"""
        if isinstance(value, list):
            if all(isinstance(x, str) for x in value):
                return ' | '.join(value)
            return str(value)
        elif isinstance(value, dict):
            # For small dicts, inline them
            if len(str(value)) < 60:
                return str(value)
            return "[dict]"
        return str(value)


def estimate_tokens(text: str) -> int:
    """Rough token estimate"""
    return len(text) // 4


def main():
    """CLI entry point with drag-and-drop support"""
    
    print("=" * 60)
    print("StashKit MetaDex Compactor")
    print("=" * 60)
    print()
    
    # Handle command line arguments (drag and drop)
    if len(sys.argv) < 2:
        print("Usage: Drag a JSON file onto this script")
        print("   or: python compact_metadex.py <input.json> [output.txt]")
        print()
        input("Press Enter to exit...")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    # Validate input
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.json':
        print(f"❌ Error: Not a JSON file: {input_path}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Determine output path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_stem(f"{input_path.stem}_compact").with_suffix('.txt')
    
    print(f"📄 Input:  {input_path}")
    print(f"📝 Output: {output_path}")
    print()
    
    try:
        # Load original
        with open(input_path, 'r', encoding='utf-8') as f:
            original_json = f.read()
        
        # Compact
        compactor = MetaDexCompactor()
        compact_text = compactor.compact(input_path)
        
        # Save
        output_path.write_text(compact_text, encoding='utf-8')
        
        # Stats
        original_size = len(original_json)
        compact_size = len(compact_text)
        original_tokens = estimate_tokens(original_json)
        compact_tokens = estimate_tokens(compact_text)
        reduction_pct = (1 - compact_size / original_size) * 100
        
        print("✅ Compaction complete!")
        print()
        print("Statistics:")
        print(f"  Original: {original_size:,} bytes (~{original_tokens:,} tokens)")
        print(f"  Compact:  {compact_size:,} bytes (~{compact_tokens:,} tokens)")
        print(f"  Savings:  {original_size - compact_size:,} bytes ({reduction_pct:.1f}%)")
        print(f"            {original_tokens - compact_tokens:,} tokens saved")
        print()
        
        # Session cost estimate
        sessions = [10, 30, 50]
        print("Session cost estimates (Sonnet 4 @ $3/1M input tokens):")
        for n_msgs in sessions:
            orig_cost = original_tokens * n_msgs * 0.000003
            comp_cost = compact_tokens * n_msgs * 0.000003
            savings = orig_cost - comp_cost
            print(f"  {n_msgs:3d} messages: ${orig_cost:.4f} → ${comp_cost:.4f} (save ${savings:.4f})")
        print()
        
        print(f"✨ Saved to: {output_path}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {input_path}")
        print(f"   {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Keep window open if double-clicked
    if len(sys.argv) == 2:  # Likely dragged onto script
        print()
        input("Press Enter to exit...")


if __name__ == '__main__':
    main()