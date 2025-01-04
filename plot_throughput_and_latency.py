import json
from pathlib import Path
import matplotlib.pyplot as plt

def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_metrics(data):
    prefill_tokens = data["detailed_performance"]["prefill_tokens"]
    decode_tokens = data["detailed_performance"]["decode_tokens"]
    total_seconds = data["detailed_performance"]["total_seconds"]
    decode_toks_per_sec = data["detailed_performance"]["decode_toks_per_sec"]
    prefill_seconds = data["detailed_performance"]["prefill_seconds"]
    
    # 计算throughput和latency    
    latency = (200 / decode_toks_per_sec) + prefill_seconds
    throughput = (prefill_tokens + 200) / latency
    
    return throughput, latency

def plot_throughput_and_latency():
    result_dir = Path("benchmark_result")
    json_files = list(result_dir.glob("output_max_cache_length_*.json"))
    
    cache_lengths = []
    throughputs = []
    latencies = []
    
    for file_path in json_files:
        data = load_json_data(file_path)
        cache_lengths.append(data["max_cache_length"])
        throughput, latency = calculate_metrics(data)
        throughputs.append(throughput)
        latencies.append(latency)
    
    # 按cache_length排序
    sorted_data = sorted(zip(cache_lengths, throughputs, latencies))
    cache_lengths, throughputs, latencies = zip(*sorted_data)
    
    # 创建三个子图
    fig = plt.figure(figsize=(12, 18))
    
    # 第一个子图：Throughput vs Cache Length
    ax1 = plt.subplot(311)
    for length, tp in zip(cache_lengths, throughputs):
        ax1.vlines(x=length, ymin=0, ymax=tp, linestyles='--', colors='gray', alpha=0.5)
    
    ax1.plot(cache_lengths, throughputs, 'bo-', linewidth=2, markersize=8)
    ax1.set_title('Throughput vs Max Cache Length', fontsize=14, pad=20)
    ax1.set_ylabel('Throughput (tokens/sec)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 在第一个子图的数据点上添加标签
    for i, (length, tp) in enumerate(zip(cache_lengths, throughputs)):
        if i % 2 == 0:
            y_offset = 10
        else:
            y_offset = -20
        ax1.annotate(f'{tp:.2f}', 
                    (length, tp),
                    textcoords="offset points",
                    xytext=(0, y_offset),
                    ha='center',
                    va='bottom' if y_offset > 0 else 'top')
    
    # 第二个子图：Latency vs Cache Length
    ax2 = plt.subplot(312)
    for length, lat in zip(cache_lengths, latencies):
        ax2.vlines(x=length, ymin=0, ymax=lat, linestyles='--', colors='gray', alpha=0.5)
    
    ax2.plot(cache_lengths, latencies, 'ro-', linewidth=2, markersize=8)
    ax2.set_title('Latency vs Max Cache Length', fontsize=14, pad=20)
    ax2.set_xlabel('Max Cache Length', fontsize=12)
    ax2.set_ylabel('Latency (seconds)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # 在第二个子图的数据点上添加标签
    for i, (length, lat) in enumerate(zip(cache_lengths, latencies)):
        if i % 2 == 0:
            y_offset = 10
        else:
            y_offset = -20
        ax2.annotate(f'{lat:.2f}s', 
                    (length, lat),
                    textcoords="offset points",
                    xytext=(0, y_offset),
                    ha='center',
                    va='bottom' if y_offset > 0 else 'top')
    
    # 第三个子图：Throughput vs Latency (Tradeoff)
    ax3 = plt.subplot(313)
    ax3.plot(latencies, throughputs, 'go-', linewidth=2, markersize=8)
    ax3.set_title('Throughput-Latency Tradeoff', fontsize=14, pad=20)
    ax3.set_xlabel('Latency (seconds)', fontsize=12)
    ax3.set_ylabel('Throughput (tokens/sec)', fontsize=12)
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # 在tradeoff图的数据点上添加cache length标签，交替放置在点的上方和下方
    for i, (length, lat, tp) in enumerate(zip(cache_lengths, latencies, throughputs)):
        if i % 2 == 0:
            y_offset = 10
            x_offset = 0
            ha = 'center'
            va = 'bottom'
        else:
            y_offset = -20
            x_offset = 0
            ha = 'center'
            va = 'top'
        
        ax3.annotate(f'len={length}', 
                    (lat, tp),
                    textcoords="offset points",
                    xytext=(x_offset, y_offset),
                    ha=ha,
                    va=va)
    
    # 调整x轴标签
    for ax in [ax1, ax2]:
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.margins(x=0.1)
    
    # 增加子图之间的间距
    plt.subplots_adjust(hspace=0.4)
    
    # 保存图表
    output_path = result_dir / 'throughput_latency_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {output_path}")

if __name__ == "__main__":
    plot_throughput_and_latency() 