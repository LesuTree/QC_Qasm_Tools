class QcQasmConverter:
    def __init__(self):
        self.qubit_map = {}
        self.inverse_map = {}
        self.original_map = {}
        self.max_index = -1

    def parse_qubits(self, v_line):
        """
        Parses the .v line from a QC file and builds qubit mappings.
        """
        tokens = v_line.strip().split()[1:]  # skip ".v"
        for tok in tokens:
            if tok.startswith("q") and tok[1:].isdigit():
                idx = int(tok[1:])
                self.qubit_map[tok] = idx
                self.inverse_map[idx] = tok
                self.original_map[tok] = idx
            elif tok.isdigit():
                idx = int(tok)
                name = f"q{tok}"
                self.qubit_map[name] = idx
                self.inverse_map[idx] = name
                self.original_map[tok] = idx
            else:
                raise ValueError(f"Unrecognized qubit format: {tok}")
        self.max_index = max(self.qubit_map.values())

    def qc_to_qasm(self, qc_lines):
        """
        Converts a list of QC-formatted lines to a QASM-formatted string.
        """
        qasm_lines = []
        begin_found = False

        for line in qc_lines:
            line = line.strip()
            if line.startswith(".v"):
                self.parse_qubits(line)
                break  # assume .v appears once and before BEGIN

        qasm_lines.append("OPENQASM 2.0;")
        qasm_lines.append("include \"qelib1.inc\";")
        qasm_lines.append(f"qreg q[{self.max_index + 1}];")

        for line in qc_lines:
            line = line.strip()
            if line == "BEGIN":
                begin_found = True
                continue
            if line == "END":
                break
            if not begin_found or not line or line.startswith("//"):
                continue

            parts = line.split()
            gate = parts[0].lower()

            if gate in {"x", "h", "t"}:
                name = parts[1]
                idx = self.original_map.get(name)
                if idx is not None:
                    qasm_lines.append(f"{gate} q[{idx}];")
            elif gate == "t*":
                name = parts[1]
                idx = self.original_map.get(name)
                if idx is not None:
                    qasm_lines.append(f"tdg q[{idx}];")
            elif gate == "cnot":
                ctrl = self.original_map.get(parts[1])
                tgt = self.original_map.get(parts[2])
                if ctrl is not None and tgt is not None:
                    qasm_lines.append(f"cx q[{ctrl}],q[{tgt}];")

        return "\n".join(qasm_lines)

    def convert_file(self, input_qc_path, output_qasm_path):
        """
        Loads QC file, converts, and writes QASM output to file.
        """
        with open(input_qc_path, "r") as f:
            qc_lines = f.readlines()
        qasm_output = self.qc_to_qasm(qc_lines)
        with open(output_qasm_path, "w") as f:
            f.write(qasm_output)

if __name__ == "__main__":
    input_qc_path = "test_SHA3_gates_12NOT_Layer_CliffordT.qc"
    output_qasm_path = "test_SHA3_gates_12NOT_Layer_CliffordT.qasm"
    converter = QcQasmConverter()
    converter.convert_file(input_qc_path, output_qasm_path)