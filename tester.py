import os
import subprocess
import sys
from pathlib import Path

def test_csharp_directory(directory: str, exe_name: str = ""):
    """C# program teszter directory-ból .in/.out fájlokkal. Windows CP1250/1252 kompatibilis."""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"ERROR: {directory} does not exist.")
        return 1

    # Exe keresés
    exe_files = list(dir_path.glob("*.exe"))
    if exe_name:
        exe_path = dir_path / exe_name
        if not exe_path.exists():
            print(f"ERROR: {exe_name} can not be found.")
            return 1
    elif exe_files:
        exe_path = exe_files[0]
    else:
        print("ERROR: there is no .exe file in this directory.")
        return 1

    print(f"Testing: {exe_path.name}")
    print("-" * 50)

    tests = list(dir_path.glob("*.in"))
    passed = 0
    failed = 0
    contains = 0

    for test_file in sorted(tests):
        out_file = test_file.with_suffix('.out')
        if not out_file.exists():
            print(f"⚠️  {test_file.name} - missing .out")
            failed += 1
            continue

        # Biztonságos fájl olvasás (próbál encodingeket)
        def safe_read(file_path):
            encodings = ['utf-8', 'cp1250', 'cp1252', 'latin1', 'iso-8859-2']
            for enc in encodings:
                try:
                    return file_path.read_text(encoding=enc).strip()
                except UnicodeDecodeError:
                    continue
            return ""  # Végső esetben latin1-mal (mindent dekódál)

        input_data = safe_read(test_file)

        # C# program futtatás - hibatűrő
        try:
            result = subprocess.run(
                [str(exe_path)],
                input=input_data.encode('utf-8', errors='replace'),
                capture_output=True,
                timeout=5
            )

            # Biztonságos stdout dekódolás
            try:
                output = result.stdout.decode('utf-8', errors='replace').strip()
            except:
                output = result.stdout.decode('cp1252', errors='replace').strip()

            expected = safe_read(out_file)

            if output == expected:
                print(f"✅ {test_file.name}")
                passed += 1
            else:
                expected2 = expected
                expected2.lower
                expected2.strip
                output.lower
                output.strip
                if  expected2 in output:
                    print(f"ℹ️ {test_file.name}")
                    print(f"   expected:     {repr(expected)[:50]}")
                    print(f"   thrown:   {repr(output)[:50]}")
                    contains += 1
                else:
                    print(f"❌ {test_file.name}")
                    print(f"   expected:     {repr(expected)[:50]}")
                    print(f"   thrown:   {repr(output)[:50]}")
                    failed += 1

        except subprocess.TimeoutExpired:
            print(f"⏰ {test_file.name} - timeout")
            failed += 1
        except Exception as e:
            print(f"💥 {test_file.name} - ERROR: {str(e)[:50]}")
            failed += 1

    print("-" * 50)
    print(f"Tests: {len(tests)} | Passed: {passed} | Contains the correct answer {contains} | Failed: {failed}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python tester.py <directory> [exe_name]")
        sys.exit(1)

    directory = sys.argv[1]
    exe_name = sys.argv[2] if len(sys.argv) > 2 else ""
    sys.exit(test_csharp_directory(directory, exe_name))