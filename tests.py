import os
import subprocess

# Codis ANSI per colors
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def main():
    print()

    # Obtenim els .j del directori
    j_files = [f for f in os.listdir('.') if f.endswith('.j')]

    if not j_files:
        print(f"\n{YELLOW}[INFO]{RESET} No s'ha trobat cap arxiu .j\n")
        return

    for j_file in j_files:
        base, _ = os.path.splitext(j_file)
        out_file = base + '.out'

        # Verifiquem que existeixi el .out corresponent
        if not os.path.exists(out_file):
            print(f"{YELLOW}[INFO]{RESET} No s'ha trobat arxiu .out per a '{j_file}'.")
            continue

        # Executem el joc de proves capturant l'output
        try:
            result = subprocess.run(
                ['python3', 'g.py', j_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
        except Exception as e:
            print(f"{RED}[ERROR]{RESET} En executar 'python3 g.py {j_file}': {e}")
            continue

        # Llegim el .out
        try:
            with open(out_file, 'r', encoding='utf-8') as f:
                expected_output = f.read()
        except Exception as e:
            print(f"{RED}[ERROR]{RESET} No s'ha pogut llegir '{out_file}': {e}")
            continue

        # Comparem la sortida obtinguda amb l'esperada
        generated = result.stdout
        if generated == expected_output:
            print(f"{GREEN}[ OK ]{RESET} Resultat correcte: '{j_file}'.")
        else:
            print(f"{RED}[FAIL]{RESET} Resultat incorrecte: '{j_file}'.")

            # Mostrem les diferències línia a línia
            print("  >> Diferències trobades:")
            gen_lines = generated.splitlines()
            exp_lines = expected_output.splitlines()
            max_lines = max(len(gen_lines), len(exp_lines))
            for i in range(max_lines):
                g_line = gen_lines[i] if i < len(gen_lines) else "<línia buida>"
                e_line = exp_lines[i] if i < len(exp_lines) else "<línia buida>"
                if g_line != e_line:
                    print(f"    Línia {i+1}:\n"
                          f"      - Generat: {repr(g_line)}\n"
                          f"      - Esperat: {repr(e_line)}")
            print()

    print()

if __name__ == "__main__":
    main()
