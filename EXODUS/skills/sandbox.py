import sys
import io
import contextlib

class CodeSandboxSkill:
    """
    A limited Python execution sandbox for math, data, and logic.
    """
    def __init__(self):
        # We define a limited set of globals to prevent easy system access
        self.safe_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "dict": dict,
                "set": set,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                "bool": bool,
                "any": any,
                "all": all
            },
            "math": __import__("math"),
            "datetime": __import__("datetime"),
            "json": __import__("json")
        }

    def run_code(self, code: str) -> str:
        """
        Executes a Python snippet and returns the captured output.
        """
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                # We use a clean dictionary for locals in every run
                safe_locals = {}
                exec(code, self.safe_globals, safe_locals)
                output = f.getvalue()
                if not output and safe_locals:
                    # If nothing was printed, return the variables defined
                    output = f"Code executed successfully. Context: {safe_locals}"
                elif not output:
                    output = "Code executed successfully (no output)."
                return f"```\n{output}\n```"
            except Exception as e:
                return f"❌ Sandbox Execution Error: {str(e)}"
