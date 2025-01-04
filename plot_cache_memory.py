import json
from pathlib import Path
import matplotlib.pyplot as plt

def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def plot_cache_memory_and_compression():
    # 获取benchmark_result目录下的所有json文件
    result_dir = Path("benchmark_result")
    json_files = list(result_dir.glob("output_max_cache_length_*.json"))
    
    # 提取数据
    cache_lengths = []
    cache_memories = []
    compression_ratios = []
    
    for file_path in json_files:
        data = load_json_data(file_path)
        cache_lengths.append(data["max_cache_length"])
        cache_memories.append(data["kv_cache_stats"]["cache_memory_gb"])
        compression_ratios.append(data["kv_cache_stats"]["compression_ratio_0"])
    
    # 按cache_length排序
    sorted_data = sorted(zip(cache_lengths, cache_memories, compression_ratios))
    cache_lengths, cache_memories, compression_ratios = zip(*sorted_data)
    
    # 创建两个子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
    
    # 第一个子图：Cache Memory
    for length, memory in zip(cache_lengths, cache_memories):
        ax1.vlines(x=length, ymin=0, ymax=memory, linestyles='--', colors='gray', alpha=0.5)
    
    ax1.plot(cache_lengths, cache_memories, 'bo-', linewidth=2, markersize=8)
    ax1.set_title('Cache Memory vs Max Cache Length', fontsize=14)
    ax1.set_ylabel('Cache Memory (GB)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 在第一个子图的数据点上添加标签
    for length, memory in zip(cache_lengths, cache_memories):
        ax1.annotate(f'{memory:.2f}GB', 
                    (length, memory),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center')
    
    # 第二个子图：Compression Ratio
    for length, ratio in zip(cache_lengths, compression_ratios):
        ax2.vlines(x=length, ymin=0, ymax=ratio, linestyles='--', colors='gray', alpha=0.5)
    
    ax2.plot(cache_lengths, compression_ratios, 'ro-', linewidth=2, markersize=8)
    ax2.set_title('Compression Ratio vs Max Cache Length', fontsize=14)
    ax2.set_xlabel('Max Cache Length', fontsize=12)
    ax2.set_ylabel('Compression Ratio', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # 在第二个子图的数据点上添加标签
    for length, ratio in zip(cache_lengths, compression_ratios):
        ax2.annotate(f'{ratio:.2f}', 
                    (length, ratio),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center')
    
    # 设置x轴刻度
    plt.xticks(cache_lengths, rotation=45)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    output_path = result_dir / 'cache_memory_and_compression.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    plot_cache_memory_and_compression() 