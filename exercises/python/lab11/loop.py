"""Lab 11 - loop: prints 1..n"""
import sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
print("\t".join(str(i) for i in range(1, n+1)))
