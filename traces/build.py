# USAGE: python traces/build.py from top-level dir

import pathlib
import subprocess

programs = [
    ("benchmarks/core/factors.bril", "60", "100"),
    ("benchmarks/core/gcd.bril", "4 20", "5 35"),
    ("benchmarks/core/geometric-sum.bril", "2 3 5", "3 4 5"),
    ("benchmarks/core/loopfact.bril", "8", "5"),
    ("benchmarks/core/reverse.bril", "123", "321"),
    ("benchmarks/core/squares.bril", "30", "16"),
    ("benchmarks/core/sum-bits.bril", "42", "63"),
    ("benchmarks/core/sum-digits.bril", "987654321", "12345"),
]

if __name__ == "__main__":
    for source, args, new_args in programs:
        stem = pathlib.Path(source).stem

        trace_output_path = f"traces/{stem}.trace"
        new_program_path = f"traces/{stem}.bril"

        with open(source) as f_source:
            bril_source = open(source).read()
            bril_json = subprocess.check_output(
                "bril2json", input=bril_source, text=True
            )

        with open(trace_output_path, "w") as f_trace:
            trace_output = subprocess.check_output(
                ("deno run brili.ts -t " + args).split(), input=bril_json, text=True
            )
            f_trace.write(trace_output)

        with open(new_program_path, "w") as f_new:
            new_program = subprocess.check_output(
                f"deno run --allow-read trace-stitch.ts {trace_output_path}".split(),
                input=bril_json,
                text=True,
            )
            new_program = subprocess.check_output(
                "bril2txt", input=new_program, text=True
            )
            new_program = f"# ARGS: {new_args}\n" + new_program
            f_new.write(new_program)
