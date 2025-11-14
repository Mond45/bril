import * as bril from "./bril-ts/bril.ts";
import { readStdin } from "./bril-ts/util.ts";

async function main() {
  const args: string[] = Array.from(Deno.args);

  const trace = JSON.parse(await Deno.readTextFile(args[0])) as {
    instrs: bril.Instruction[];
    traceEndIdx: number;
  };
  const program = JSON.parse(await readStdin()) as bril.Program;

  const mainIdx = program.functions.findIndex((fn) => fn.name === "main");
  const mainFn = program.functions[mainIdx];

  mainFn.instrs.splice(trace.traceEndIdx, 0, {
    label: "__speculate_done",
  });
  const oldInstrs = [...mainFn.instrs];
  mainFn.instrs = [
    {
      op: "speculate",
    },
    ...trace.instrs,
    {
      op: "commit",
    },
    {
      labels: ["__speculate_done"],
      op: "jmp",
    },
    { label: "__speculate_aborted" },
    ...oldInstrs,
  ];

  console.log(JSON.stringify(program));
}

main();
