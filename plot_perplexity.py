import json
from pathlib import Path
import matplotlib.pyplot as plt
import re

def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_ppl_data(data):
    # 提取所有ppl@数字格式的键值对
    ppl_pattern = re.compile(r'ppl@(\d+)')
    ppl_data = {}
    
    for key, value in data.items():
        match = ppl_pattern.match(key)
        if match:
            length = int(match.group(1))
            ppl_data[length] = value
    
    # 按长度排序
    sorted_items = sorted(ppl_data.items())
    lengths, ppls = zip(*sorted_items)
    
    return lengths, ppls

def plot_perplexity():
    # 加载数据
    result_dir = Path("results/Qwen2-7B-Instruct/heavy_hitter")
    file_path = result_dir / "attn_thresholding=False__cache_bits=None__cache_length_pattern=tile__cache_strategy_pattern=tile__global_tokens=4__history_window_size=1__max_cache_length=0.25__recent_window=10/pg19_metrics.json"
    
    data = load_json_data(file_path)
    lengths, ppls = extract_ppl_data(data)
    avg_ppl = data['ppl']  # 获取平均PPL
    
    # 创建图表
    plt.figure(figsize=(12, 6))
    
    # 绘制PPL曲线
    plt.plot(lengths, ppls, 'b-', linewidth=2, marker='o', label='Perplexity')
    
    # 添加平均PPL的水平线
    plt.axhline(y=avg_ppl, color='r', linestyle='--', 
                label=f'Average PPL: {avg_ppl:.3f}')
    
    # 设置标题和标签
    plt.title('Perplexity vs Text Length', pad=20)
    plt.xlabel('Text Length (tokens)')
    plt.ylabel('Perplexity')
    
    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 添加图例
    plt.legend()
    
    # 设置x轴刻度为所有的长度值
    plt.xticks(lengths, rotation=45)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    output_path = result_dir / 'perplexity_vs_length.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    plot_perplexity() 