import os
import subprocess

# ANSI codes for colors
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def main():
    print()

    # Get the .j files from ./tests directory
    test_dir = 'tests'
    j_files = [f for f in os.listdir(test_dir) if f.endswith('.j')]

    if not j_files:
        print(f"\n{YELLOW}[INFO]{RESET} No .j file found\n")
        return

    for j_file in j_files:
        base, _ = os.path.splitext(j_file)
        out_file = base + '.out'

        j_path = os.path.join(test_dir, j_file)
        out_path = os.path.join(test_dir, out_file)

        # Verify that the corresponding .out exists
        if not os.path.exists(out_path):
            print(f"{YELLOW}[INFO]{RESET} No .out file found for '{j_file}'.")
            continue

        # Run the test capturing the output
        try:
            result = subprocess.run(
                ['python3', 'g.py', j_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
        except Exception as e:
            print(f"{RED}[ERROR]{RESET} While running 'python3 g.py {j_file}': {e}")
            continue

        # Read the .out
        try:
            with open(out_path, 'r', encoding='utf-8') as f:
                expected_output = f.read()
        except Exception as e:
            print(f"{RED}[ERROR]{RESET} Could not read '{out_file}': {e}")
            continue

        # Compare the obtained output with the expected one
        generated = result.stdout
        if generated == expected_output:
            print(f"{GREEN}[ OK ]{RESET} Correct result: '{j_file}'.")
        else:
            print(f"{RED}[FAIL]{RESET} Incorrect result: '{j_file}'.")

            # Show the line-by-line differences
            print("  >> Differences found:")
            gen_lines = generated.splitlines()
            exp_lines = expected_output.splitlines()
            max_lines = max(len(gen_lines), len(exp_lines))
            for i in range(max_lines):
                g_line = gen_lines[i] if i < len(gen_lines) else "<empty line>"
                e_line = exp_lines[i] if i < len(exp_lines) else "<empty line>"
                if g_line != e_line:
                    print(f"    Line {i+1}:\n"
                          f"      - Obtained: {repr(g_line)}\n"
                          f"      - Expected : {repr(e_line)}")
            print()

    print()

if __name__ == "__main__":
    main()
