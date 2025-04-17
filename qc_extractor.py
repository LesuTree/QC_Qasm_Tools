import os
from typing import List, Set


class QcExtractor:
    def __init__(self, input_path: str, output_dir: str):
        self.input_path = input_path
        self.output_dir = output_dir
        self.raw_lines = []
        self.variables = []
        self.variable_set = set()
        self.blocks = []

    def load_file(self):
        """读取原始qc文件"""
        with open(self.input_path, 'r') as f:
            lines = f.readlines()

        in_gate_section = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('.v'):
                self.variables = stripped.split()[1:]  # 不保留 `.v`
                self.variable_set = set(self.variables)
            elif stripped == 'BEGIN':
                in_gate_section = True
            elif in_gate_section:
                self.raw_lines.append(stripped)

    def split_by_H(self):
        """根据H门划分为多个区块（不包括H门）"""
        current_block = []
        for line in self.raw_lines:
            if line.startswith('H'):
                if current_block:
                    self.blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(line)
        if current_block:
            self.blocks.append(current_block)

    def extract_and_write(self):
        """从每个区块中提取 cnot 和 T，并写入新文件"""
        os.makedirs(self.output_dir, exist_ok=True)
        for idx, block in enumerate(self.blocks):
            filtered = [line for line in block if self.is_target_gate(line)]
            if not filtered:
                continue

            used_vars = self.extract_used_variables(filtered)
            reduced_vars = [v for v in self.variables if v in used_vars]

            filename = os.path.join(self.output_dir, f"sub_{idx}.qc")
            with open(filename, 'w') as f:
                f.write('.v ' + ' '.join(reduced_vars) + '\n')
                f.write('BEGIN\n')
                for line in filtered:
                    f.write(line + '\n')
                f.write('END\n')
            print(f"[INFO] Written: {filename}")

    @staticmethod
    def is_target_gate(line: str) -> bool:
        """判断是否是目标门（cnot 或 T）"""
        tokens = line.split()
        if len(tokens) < 2:
            return False
        return tokens[0] == 'cnot' or tokens[0] == 'T'

    @staticmethod
    def extract_used_variables(gates: List[str]) -> Set[str]:
        """提取门列表中使用到的变量"""
        used = set()
        for gate in gates:
            tokens = gate.split()
            used.update(tokens[1:])
        return used

    def run(self):
        """运行整个流程"""
        self.load_file()
        self.split_by_H()
        self.extract_and_write()


if __name__ == '__main__':
    input_path = 'test_SHA3_gates_12NOT_Layer_CliffordT.qc'
    output_dir = 'output'
    extractor = QcExtractor(input_path, output_dir)
    extractor.run()
