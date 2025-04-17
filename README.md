# QC_Qasm_Tools

本项目包含一个量子电路处理流程，主要包括文件格式转换、量子电路优化、分割及张量文件生成的步骤。请按以下顺序操作：

### 1. QASM 转换为 QC 格式

使用 `qasm_convert2_qc.py` 脚本将原始的 QASM 文件转换为 QC 格式文件，作为后续处理的输入。

### 2. 量子电路优化

使用以下仓库中的优化工具对生成的 QC 文件进行优化处理：

> 🔗 仓库地址：[VivienVandaele/quantum-circuit-optimization](https://github.com/VivienVandaele/quantum-circuit-optimization/tree/6050896b9d36a47c62fcd98c481483b8c17b6a0d)

按照仓库中的说明运行优化脚本，输入为第 1 步中生成的 QC 文件。

### 3. 基于 H 门进行分割

使用 `qc_extractor.py` 脚本对优化后的 QC 文件按 H 门进行分割，生成多个子电路文件。

### 4. QC 转换回 QASM

通过 `qc_convert2_qasm.py` 脚本将第 3 步中生成的 QC 文件重新转换为 QASM 格式。

### 5. QASM 转换为张量表示

使用以下仓库提供的工具将生成的 QASM 文件转换为张量表示：

> 🔗 仓库地址：[tlaakkonen/circuit-to-tensor](https://github.com/tlaakkonen/circuit-to-tensor)

按照该仓库的使用说明进行转换，最终得到对应的量子张量表达文件

------

