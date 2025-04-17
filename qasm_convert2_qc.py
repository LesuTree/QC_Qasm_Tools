def qasm_to_qc(qasm_lines):
    qc_lines = []
    qubit_indices = set()

    # Parse all lines, gather qubit indices
    for line in qasm_lines:
        line = line.strip()
        if line.startswith(("x", "h", "t", "tdg", "cx")):
            parts = line.split()
            if parts[0] == "cx":
                ctrl, tgt = parts[1].split(",")
                cidx = int(ctrl[2:-1])
                tidx = int(tgt[2:-2])
                qubit_indices.update([cidx, tidx])
            else:
                idx= int(parts[1][2:-2])
                qubit_indices.add(idx)

    # Sort qubit indices and map to names
    qubits = sorted(list(qubit_indices))
    qubit_map = {q: f"q{q}" for q in qubits}
    qc_lines.append(".v " + " ".join(qubit_map[q] for q in qubits))
    qc_lines.append("BEGIN")

    # Now parse instructions
    for line in qasm_lines:
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        parts = line.split()
        gate = parts[0]

        if gate == "x":
            idx = int(parts[1][2:-2])
            qc_lines.append(f"X {qubit_map[idx]}")
        elif gate == "h":
            idx = int(parts[1][2:-2])
            qc_lines.append(f"H {qubit_map[idx]}")
        elif gate == "t":
            idx = int(parts[1][2:-2])
            qc_lines.append(f"T {qubit_map[idx]}")
        elif gate == "tdg":
            idx = int(parts[1][2:-2])
            qc_lines.append(f"T* {qubit_map[idx]}")
        elif gate == "cx":
            ctrl, tgt = parts[1].split(",")
            cidx = int(ctrl[2:-1])
            tidx = int(tgt[2:-2])
            qc_lines.append(f"cnot {qubit_map[cidx]} {qubit_map[tidx]}")

    qc_lines.append("END")
    return "\n".join(qc_lines)


input_file_path = "SHA3_gates_12NOT_Layer_CliffordT.qasm"
# 读取输入文件
with open(input_file_path, "r") as f:
    real_qasm_input = f.readlines()
# 转换
qc_output = qasm_to_qc(real_qasm_input)

# 输出结果
output_file_path = input_file_path.replace(".qasm", ".qc")
with open(output_file_path, "w") as f:
    f.write(qc_output)
