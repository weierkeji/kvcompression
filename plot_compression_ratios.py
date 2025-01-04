import json
from pathlib import Path
import matplotlib.pyplot as plt

def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def plot_compression_ratios():
    result_dir = Path("results/Qwen2-7B-Instruct/recent_global")
    
    # 获取所有结果文件
    pattern_files = {
        'funnel': 'cache_bits=None__cache_length_pattern=funnel__cache_strategy_pattern=tile__global_tokens=1__max_cache_length=0.5/truthfulqa_metrics.json',
        'pyramid': 'cache_bits=None__cache_length_pattern=pyramid__cache_strategy_pattern=tile__global_tokens=1__max_cache_length=0.5/truthfulqa_metrics.json',
        'repeat': 'cache_bits=None__cache_length_pattern=repeat__cache_strategy_pattern=tile__global_tokens=1__max_cache_length=0.1,0.5/truthfulqa_metrics.json',
        'tile': 'cache_bits=None__cache_length_pattern=tile__cache_strategy_pattern=tile__global_tokens=1__max_cache_length=0.1,0.5/truthfulqa_metrics.json'
    }
    
    for pattern, file_path in pattern_files.items():
        data = load_json_data(result_dir / file_path)
        
        # 提取压缩率数据
        layers = list(range(28))  # 0-27层
        compression_ratios = [data[f'compression_ratio_{i}'] for i in layers]
        avg_ratio = data['compression_ratio_avg']
        cache_memory = data['cache_memory_gb']
        
        # 创建图表
        plt.figure(figsize=(10, 6))
        plt.plot(layers, compression_ratios, 'b-', linewidth=2, marker='o')
        
        # 添加平均压缩率的水平线
        plt.axhline(y=avg_ratio, color='r', linestyle='--', 
                   label=f'Avg Ratio: {avg_ratio:.3f}')
        
        # 设置标题和标签
        plt.title(f'Compression Ratio vs Layer ({pattern.capitalize()})\nCache Memory: {cache_memory:.3f} GB', 
                 pad=20)
        plt.xlabel('Layer')
        plt.ylabel('Compression Ratio')
        
        # 添加网格
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # 添加图例
        plt.legend()
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        output_path = result_dir / f'compression_ratio_{pattern}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {output_path}")
        plt.close()

if __name__ == "__main__":
    plot_compression_ratios() 