#!/usr/bin/env python3
"""
Convert Python pseudocode to D2 diagrams using Grok LLM
Usage: python pseudo_to_diagram.py <input.py> [options]
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    import openai
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv package not installed. Run: pip install python-dotenv")
    sys.exit(1)


def clean_d2_code(d2_code: str) -> str:
    """Clean and validate D2 code to ensure correct syntax"""
    lines = d2_code.split('\n')
    cleaned_lines = []

    for line in lines:
        # Remove markdown code fences
        if line.strip().startswith('```'):
            continue

        # Skip empty lines at the start
        if not cleaned_lines and not line.strip():
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


def convert_python_to_d2(python_code: str, api_key: str, use_pascal_case: bool = False) -> str:
    """Convert Python pseudocode to D2 format using Grok"""

    # Grok uses OpenAI-compatible API
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    naming_instruction = ""
    if use_pascal_case:
        naming_instruction = """
NAMING CONVENTION:
- Transform ALL snake_case to PascalCase in both node IDs AND labels
- Function calls like download_data() should become DownloadData() in labels
- Variables like process_data should become ProcessData
- Example: Instead of 'download: "data = download_data()"' use 'Download: "data = DownloadData()"'
- ALL text in labels must use PascalCase, no snake_case allowed

"""

    prompt = f"""Convert the following Python pseudocode into D2 diagram format.

STRICT SYNTAX RULES:
1. Define nodes like: node_id: "Label text" {{shape: rectangle}}
2. Connect nodes with simple arrows: node1 -> node2
3. For labeled edges, use: node1 -> node2: "label text"
4. For styled edges (dashed), use: node1 -> node2: "label" {{style.stroke-dash: 3}}
5. NO edge blocks with nested properties
6. NO scenarios or animation
7. All shapes must be rectangles
{naming_instruction}
EXAMPLE VALID D2 CODE:
download: "data = download_data()" {{shape: rectangle}}
process: "result = process(data)" {{shape: rectangle}}
loop_start: "for item in items" {{shape: rectangle}}
action: "handle(item)" {{shape: rectangle}}

download -> process
process -> loop_start
loop_start -> action
action -> loop_start: "next iteration" {{style.stroke-dash: 3}}

Python pseudocode to convert:
```python
{python_code}
```

Output ONLY valid D2 code following the syntax rules above. No explanations, no markdown fences."""

    # Measure prompt length
    prompt_length = len(prompt)
    prompt_tokens_estimate = prompt_length // 4  # Rough estimate: ~4 chars per token

    print(f"📏 Prompt length: {prompt_length} characters (~{prompt_tokens_estimate} tokens)")
    print(f"⏳ Calling Grok API...")

    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[
                {
                    "role": "system",
                    "content": "You are a diagram expert. Convert code to D2 diagram syntax. Output only D2 code, no markdown fences, no explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

        d2_code = response.choices[0].message.content.strip()

        # Clean the D2 code
        d2_code = clean_d2_code(d2_code)

        # Measure time
        elapsed_time = time.time() - start_time

        # Get token usage if available
        usage = response.usage
        prompt_tokens = usage.prompt_tokens if usage else "N/A"
        completion_tokens = usage.completion_tokens if usage else "N/A"
        total_tokens = usage.total_tokens if usage else "N/A"

        print(f"✓ Grok API call completed in {elapsed_time:.2f}s")
        print(f"📊 Tokens used: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total")

        return d2_code

    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"✗ Error calling Grok API after {elapsed_time:.2f}s: {e}")
        sys.exit(1)


def generate_diagram(d2_file: Path, output_file: Path, format: str = "png"):
    """Generate diagram from D2 file using d2 command"""

    d2_path = os.path.expanduser("~/.local/bin/d2")

    if not os.path.exists(d2_path):
        print(f"Error: D2 not found at {d2_path}")
        print("Please install D2 first")
        sys.exit(1)

    cmd = [d2_path, str(d2_file), str(output_file)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Diagram generated: {output_file}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating diagram: {e.stderr}")
        return False


def main():
    # Load environment variables from .env file
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Convert Python pseudocode to D2 diagrams using Grok"
    )
    parser.add_argument(
        "input_file",
        help="Path to Python pseudocode file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output diagram file (default: <input_name>.png)",
        default=None
    )
    parser.add_argument(
        "-f", "--format",
        help="Output format: png, svg, pdf (default: png)",
        choices=["png", "svg", "pdf"],
        default="png"
    )
    parser.add_argument(
        "-k", "--api-key",
        help="Grok API key (overrides .env file)",
        default=None
    )
    parser.add_argument(
        "--keep-d2",
        help="Keep the intermediate D2 file",
        action="store_true"
    )
    parser.add_argument(
        "--save-d2",
        help="Save the D2 file generated by Grok",
        action="store_true"
    )
    parser.add_argument(
        "--PascalCase",
        help="Transform function calls to PascalCase blocks (e.g., do_something() -> DoSomething)",
        action="store_true"
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Show the generated D2 code",
        action="store_true"
    )

    args = parser.parse_args()

    # Get API key (priority: command line > .env file > environment variable)
    api_key = args.api_key or os.getenv("GROK_API_KEY")
    if not api_key:
        print("Error: Grok API key not provided")
        print("Please set GROK_API_KEY in .env file or pass via --api-key flag")
        print("\nCreate a .env file with:")
        print("  GROK_API_KEY=your-api-key-here")
        sys.exit(1)

    # Read input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    print(f"Reading {input_path}...")
    python_code = input_path.read_text()

    # Convert to D2
    print("Converting to D2 format using Grok...")
    d2_code = convert_python_to_d2(python_code, api_key, args.PascalCase)

    if args.verbose:
        print("\nGenerated D2 code:")
        print("-" * 50)
        print(d2_code)
        print("-" * 50)

    # Save D2 file in current directory
    d2_file = Path(input_path.stem + ".d2")
    d2_file.write_text(d2_code)
    print(f"✓ D2 file saved: {d2_file}")

    # Determine output file (save in current directory)
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = Path(input_path.stem + f".{args.format}")

    # Generate diagram
    print(f"Generating {args.format.upper()} diagram...")
    success = generate_diagram(d2_file, output_file, args.format)

    # Cleanup
    if not args.keep_d2 and not args.save_d2 and success:
        d2_file.unlink()
        print(f"✓ Cleaned up temporary D2 file")

    if success:
        print(f"\n✓ Done! Diagram saved to: {output_file}")
    else:
        print("\n✗ Failed to generate diagram")
        sys.exit(1)


if __name__ == "__main__":
    main()
