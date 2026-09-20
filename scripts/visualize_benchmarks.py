"""Generate high-resolution PNG benchmark visualizations for Sabai-Rules.

Source Data:
1. docs/architecture_and_benchmark.md (Ollama Model Benchmarks & Hardware Profiling on RTX 3050)
2. docs/rag_evaluation_report.md & docs/eval_results.csv (RAG Quantitative Evaluation & Retrieval Ablation)

Outputs saved to docs/figures/*.png with 300 DPI publication quality.
"""

import os
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd

# Configure Thai-compatible modern fonts
matplotlib.rcParams["font.sans-serif"] = [
    "Leelawadee UI",
    "Tahoma",
    "Leelawadee",
    "Segoe UI",
    "DejaVu Sans",
    "sans-serif",
]
matplotlib.rcParams["axes.unicode_minus"] = False

# Palette
PRIMARY_GREEN = "#10B981"   # Winner / Qwen 2.5 3B
ACCENT_BLUE = "#2563EB"    # Relations / Hybrid
PURPLE = "#8B5CF6"         # Llama 3.2 3B
AMBER = "#F59E0B"          # Intermediate / Fair
CORAL = "#EF4444"          # Low / Warning
SLATE_DARK = "#0F172A"
SLATE_GRAY = "#64748B"
BG_LIGHT = "#F8FAFC"
CARD_BG = "#FFFFFF"

FIGURES_DIR = Path(__file__).resolve().parent.parent / "docs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def set_clean_style(ax, title=None, xlabel=None, ylabel=None):
    """Apply modern minimal card styling to an axis."""
    ax.set_facecolor("#FFFFFF")
    ax.grid(True, linestyle="--", alpha=0.35, color=SLATE_GRAY, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.tick_params(colors="#334155", labelsize=10.5)

    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=SLATE_DARK, pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, fontweight="bold", color="#334155", labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, fontweight="bold", color="#334155", labelpad=8)


# =====================================================================
# Chart 1: Information Extraction Capacity (Entities & Relations)
# =====================================================================
def plot_extraction_capacity():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300, facecolor=BG_LIGHT)
    set_clean_style(
        ax,
        title="ผลการทดสอบสกัด Entity และ Relationship จากระเบียบวินัย (ข้อ 28-29)",
        xlabel="โมเดลที่ทดสอบ (Ollama Local บน RTX 3050 6GB)",
        ylabel="จำนวนที่สกัดได้ถูกต้อง (Items)",
    )

    models = ["qwen2.5:3b\n(Selected)", "llama3.2:3b", "smollm2:1.7b", "llama3.2:1b", "qwen2.5:0.5b"]
    entities = [8, 6, 1, 1, 4]
    relations = [7, 3, 1, 2, 2]

    x = np.arange(len(models))
    width = 0.36

    rects1 = ax.bar(x - width / 2, entities, width, label="Entities (ประเภทความผิด & โทษ)", color="#0EA5E9", zorder=3)
    rects2 = ax.bar(x + width / 2, relations, width, label="Relations ([:SUBJECT_TO])", color="#6366F1", zorder=3)

    # Highlight winner bar border
    rects1[0].set_edgecolor("#0369A1")
    rects1[0].set_linewidth(2)
    rects2[0].set_edgecolor("#4338CA")
    rects2[0].set_linewidth(2)

    # Add data labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"{h}", xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color="#0369A1")

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h}", xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color="#4338CA")

    # Winner badge / annotation
    ax.annotate(
        "อันดับ 1 ผู้ชนะการทดสอบ: สกัดครบถ้วนสูงสุด 15 ข้อมูล\nภาษาไทยถูกต้อง 100% ไม่มีปัญหา Encoding",
        xy=(0, 8), xytext=(0.6, 7.6),
        arrowprops=dict(facecolor=PRIMARY_GREEN, shrink=0.08, width=1.8, headwidth=7),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ECFDF5", edgecolor=PRIMARY_GREEN, linewidth=1.5),
        fontsize=9.5, fontweight="bold", color="#065F46"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight="medium")
    ax.set_ylim(0, 9.5)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="upper right")

    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_extraction_capacity.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 2: Speed and Latency Comparison
# =====================================================================
def plot_speed_and_latency():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300, facecolor=BG_LIGHT)

    models = ["qwen2.5:3b\n(Selected)", "llama3.2:3b", "smollm2:1.7b", "llama3.2:1b", "qwen2.5:0.5b"]
    speed_tps = [63.2, 62.1, 62.4, 96.8, 213.6]
    latency_sec = [11.21, 17.57, 10.28, 9.67, 6.77]

    colors_speed = [PRIMARY_GREEN, PURPLE, SLATE_GRAY, SLATE_GRAY, AMBER]
    colors_latency = [PRIMARY_GREEN, CORAL, SLATE_GRAY, SLATE_GRAY, AMBER]

    # Subplot 1: Speed (Tokens / Sec)
    set_clean_style(ax1, title="1) ความเร็วในการประมวลผล (Inference Speed)", ylabel="Tokens ต่อวินาที (ยิ่งสูงยิ่งเร็ว)")
    bars1 = ax1.bar(models, speed_tps, color=colors_speed, width=0.55, zorder=3)
    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f"{h:.1f} t/s", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                     fontsize=9.5, fontweight="bold", color="#1E293B")
    ax1.set_ylim(0, 240)
    ax1.axhline(60, color="#10B981", linestyle=":", alpha=0.7, label="เป้าหมาย Real-time (>60 t/s)")
    ax1.legend(loc="upper left", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1")

    # Subplot 2: Latency (Seconds)
    set_clean_style(ax2, title="2) เวลาประมวลผลทั้งหมด (Total Latency)", ylabel="วินาที (ยิ่งน้อยยิ่งดี)")
    bars2 = ax2.bar(models, latency_sec, color=colors_latency, width=0.55, zorder=3)
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"{h:.2f} s", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                     fontsize=9.5, fontweight="bold", color="#1E293B")
    ax2.set_ylim(0, 20)

    # Note annotation
    ax2.annotate(
        "Llama 3.2:3B ช้ากว่า 56%\nเนื่องจากสับสนภาษาไทย",
        xy=(1, 17.57), xytext=(1.2, 14.5),
        arrowprops=dict(facecolor=CORAL, shrink=0.08, width=1.5, headwidth=6),
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor=CORAL, linewidth=1),
        fontsize=9, color="#991B1B"
    )

    plt.suptitle("เปรียบเทียบประสิทธิภาพความเร็วและเวลาตอบสนองของโมเดล (RTX 3050 6GB)",
                 fontsize=14, fontweight="bold", color=SLATE_DARK, y=0.98)
    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_speed_and_latency.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 3: Quality vs Speed Trade-off (Pareto Frontier)
# =====================================================================
def plot_quality_vs_speed():
    fig, ax = plt.subplots(figsize=(9.5, 6), dpi=300, facecolor=BG_LIGHT)
    set_clean_style(
        ax,
        title="Trade-off Matrix: ความเร็วในการประมวลผล vs คุณภาพการสกัดข้อมูล",
        xlabel="ความเร็วประมวลผล (Inference Speed: Tokens/s)",
        ylabel="ผลรวมข้อมูลที่สกัดได้ (Entities + Relations Count)",
    )

    data = [
        {"name": "qwen2.5:3b (Selected)", "speed": 63.2, "quality": 15, "color": PRIMARY_GREEN, "size": 350},
        {"name": "llama3.2:3b", "speed": 62.1, "quality": 9, "color": PURPLE, "size": 250},
        {"name": "smollm2:1.7b", "speed": 62.4, "quality": 2, "color": SLATE_GRAY, "size": 180},
        {"name": "llama3.2:1b", "speed": 96.8, "quality": 3, "color": "#38BDF8", "size": 180},
        {"name": "qwen2.5:0.5b", "speed": 213.6, "quality": 6, "color": AMBER, "size": 200},
    ]

    for d in data:
        ax.scatter(d["speed"], d["quality"], s=d["size"], color=d["color"], edgecolors="#0F172A",
                   linewidths=1.5, alpha=0.9, zorder=4)
        offset_y = 0.5 if d["name"].startswith("qwen2.5:3b") else -0.7
        offset_x = -15 if d["speed"] > 150 else 3
        ax.annotate(
            d["name"],
            xy=(d["speed"], d["quality"]),
            xytext=(d["speed"] + offset_x, d["quality"] + offset_y),
            fontsize=9.5, fontweight="bold", color="#1E293B",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", alpha=0.8)
        )

    # Sweet spot highlight zone
    ax.axvspan(55, 75, ymin=0.6, ymax=0.98, color="#D1FAE5", alpha=0.45, zorder=1)
    ax.text(65, 13.5, "[Sweet Spot Zone]\n(คุณภาพสูงสุด & ความเร็วเหมาะสม)",
            fontsize=9.5, color="#065F46", fontweight="bold", ha="center")

    # Fast but low quality zone
    ax.axvspan(85, 230, ymin=0.05, ymax=0.45, color="#FEF3C7", alpha=0.35, zorder=1)
    ax.text(150, 4.5, "[Ultra-Fast แต่สกัดข้อมูลไม่ครบถ้วน]\n(Low Semantic Depth)",
            fontsize=9.5, color="#92400E", fontweight="bold", ha="center")

    ax.set_xlim(40, 235)
    ax.set_ylim(0, 16.5)

    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_quality_vs_speed_tradeoff.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 4: Hardware Profiling & VRAM Budget (RTX 3050 6GB)
# =====================================================================
def plot_vram_budget():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300, facecolor=BG_LIGHT)
    set_clean_style(
        ax,
        title="การจัดสรรงบประมาณหน่วยความจำ GPU VRAM บน NVIDIA RTX 3050 (6.0 GB)",
        xlabel="ระดับขนาดโมเดล (Model Tier)",
        ylabel="ปริมาณ VRAM ที่ต้องการ (Gigabytes)",
    )

    tiers = [
        "0.5B\n(qwen2.5:0.5b)",
        "1.0B\n(llama3.2:1b)",
        "1.7B\n(smollm2:1.7b)",
        "3.0B [Selected]\n(qwen2.5:3b)",
        "7.0B Q4\n(qwen2.5:7b)",
        "8.0B Q4\n(typhoon2:8b)"
    ]
    model_vram = [0.5, 1.1, 1.8, 2.1, 4.7, 5.2]
    context_vram = [0.4, 0.5, 0.6, 1.4, 0.7, 0.6]  # KV cache & workspace

    x = np.arange(len(tiers))
    width = 0.52

    p1 = ax.bar(x, model_vram, width, label="Model Weights (VRAM)", color="#3B82F6", zorder=3)
    p2 = ax.bar(x, context_vram, width, bottom=model_vram, label="KV Cache Context & Overhead", color="#93C5FD", zorder=3)

    # Highlight the chosen 3B model
    p1[3].set_color("#10B981")
    p2[3].set_color("#6EE7B7")
    p1[4].set_color("#8B5CF6")
    p2[4].set_color("#C4B5FD")

    # Threshold lines
    ax.axhline(6.0, color="#EF4444", linestyle="-", linewidth=1.8, label="Physical VRAM Ceiling (6.0 GB)", zorder=4)
    ax.axhline(5.4, color="#F59E0B", linestyle="--", linewidth=1.5, label="Usable VRAM Limit (~5.4 GB หัก OS/DWM)", zorder=4)

    # Total labels
    for i in range(len(tiers)):
        total = model_vram[i] + context_vram[i]
        ax.annotate(f"{total:.1f} GB", xy=(x[i], total), xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")

    # Annotate Sweet Spot
    ax.annotate(
        "[Sweet Spot สำหรับ LINE Chatbot]:\nโหลดเข้า VRAM 100% (ไร้ Offloading Penalty)\nเหลือ Headroom สำหรับ Context ถึง ~2.5 GB",
        xy=(3, 2.2), xytext=(1.2, 4.4),
        arrowprops=dict(facecolor=PRIMARY_GREEN, shrink=0.08, width=1.5, headwidth=6),
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor=PRIMARY_GREEN, linewidth=1.2),
        fontsize=9, color="#065F46", fontweight="bold"
    )

    # Annotate 7B usage
    ax.annotate(
        "[Offline Graph Extraction]:\nสกัดกฎหมาย 47 หน้าเชิงลึก ไม่ติด Real-time",
        xy=(4, 4.8), xytext=(3.2, 6.2),
        arrowprops=dict(facecolor=PURPLE, shrink=0.08, width=1.2, headwidth=5),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#F5F3FF", edgecolor=PURPLE, linewidth=1),
        fontsize=8.5, color="#5B21B6"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(tiers)
    ax.set_ylim(0, 7.2)
    ax.legend(loc="lower right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1")

    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_vram_budgeting.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 5: Radar Multi-Dimensional Model Evaluation
# =====================================================================
def plot_radar_comparison():
    categories = [
        "Thai Language\nQuality (ภาษาไทย)",
        "Entity Extraction\n(สกัดตัวตน)",
        "Relation Extraction\n(สกัดความสัมพันธ์)",
        "Speed Score\n(ความเร็ว Token/s)",
        "VRAM Fit\n(การประหยัด VRAM)"
    ]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Scores out of 10
    models_data = {
        "Qwen2.5:3b (Winner)": {
            "scores": [10.0, 10.0, 10.0, 6.5, 8.5],
            "color": PRIMARY_GREEN,
            "linewidth": 2.5,
            "fill": True,
            "alpha": 0.25
        },
        "Llama3.2:3b": {
            "scores": [4.0, 7.5, 4.3, 6.4, 8.0],
            "color": PURPLE,
            "linewidth": 1.8,
            "fill": False,
            "alpha": 0.05
        },
        "SmolLM2:1.7b": {
            "scores": [3.0, 1.25, 1.4, 6.5, 9.0],
            "color": SLATE_GRAY,
            "linewidth": 1.2,
            "fill": False,
            "alpha": 0.0
        },
        "Qwen2.5:0.5b": {
            "scores": [5.0, 5.0, 2.8, 10.0, 10.0],
            "color": AMBER,
            "linewidth": 1.5,
            "fill": False,
            "alpha": 0.05
        },
    }

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300, facecolor=BG_LIGHT)
    ax.set_facecolor("#FFFFFF")

    plt.xticks(angles[:-1], categories, color="#1E293B", size=10, fontweight="bold")
    ax.set_rlabel_position(30)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#64748B", size=8.5)
    plt.ylim(0, 10.5)

    for name, cfg in models_data.items():
        vals = cfg["scores"] + cfg["scores"][:1]
        ax.plot(angles, vals, color=cfg["color"], linewidth=cfg["linewidth"], label=name)
        if cfg["fill"]:
            ax.fill(angles, vals, color=cfg["color"], alpha=cfg["alpha"])

    plt.title("การเปรียบเทียบขีดความสามารถรอบด้าน 5 มิติ (Radar Evaluation)",
              size=13, fontweight="bold", color=SLATE_DARK, y=1.08)
    plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=True, facecolor="#FFFFFF")

    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_radar_comparison.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 6: Executive All-in-One Dashboard
# =====================================================================
def plot_executive_dashboard():
    fig = plt.figure(figsize=(16, 10), dpi=300, facecolor=BG_LIGHT)
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.24)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    models_short = ["Qwen:3b (Win)", "Llama:3b", "Smol:1.7b", "Llama:1b", "Qwen:0.5b"]

    # 1. Extraction Capacity
    set_clean_style(ax1, title="A) ความสามารถในการสกัด Entities & Relations", ylabel="จำนวนรายการที่สกัดได้")
    x = np.arange(len(models_short))
    w = 0.35
    b1 = ax1.bar(x - w/2, [8, 6, 1, 1, 4], w, label="Entities", color="#0EA5E9")
    b2 = ax1.bar(x + w/2, [7, 3, 1, 2, 2], w, label="Relations", color="#6366F1")
    ax1.set_xticks(x)
    ax1.set_xticklabels(models_short, fontsize=9.5)
    ax1.set_ylim(0, 9)
    ax1.legend(loc="upper right", fontsize=8.5)

    # 2. Speed vs Latency
    set_clean_style(ax2, title="B) ความเร็วการประมวลผล (Tokens/s)", ylabel="Tokens ต่อวินาที")
    colors_speed = [PRIMARY_GREEN, PURPLE, SLATE_GRAY, SLATE_GRAY, AMBER]
    b_speed = ax2.bar(models_short, [63.2, 62.1, 62.4, 96.8, 213.6], color=colors_speed, width=0.5)
    for b in b_speed:
        h = b.get_height()
        ax2.annotate(f"{h:.1f}", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 2),
                     textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")
    ax2.set_ylim(0, 235)

    # 3. VRAM Budgeting
    set_clean_style(ax3, title="C) งบประมาณ VRAM บน GPU RTX 3050 6GB", ylabel="VRAM ที่ใช้ (GB)")
    tiers = ["0.5B", "1.0B", "1.7B", "3.0B [Win]", "7.0B Q4", "8.0B Q4"]
    m_vram = [0.5, 1.1, 1.8, 2.1, 4.7, 5.2]
    c_vram = [0.4, 0.5, 0.6, 1.4, 0.7, 0.6]
    xx = np.arange(len(tiers))
    ax3.bar(xx, m_vram, 0.5, label="Model Weights", color="#3B82F6")
    ax3.bar(xx, c_vram, 0.5, bottom=m_vram, label="KV Cache & Buffer", color="#93C5FD")
    ax3.axhline(6.0, color=CORAL, linestyle="-", linewidth=1.5, label="VRAM Cap (6GB)")
    ax3.axhline(5.4, color=AMBER, linestyle="--", linewidth=1.2, label="Safe Cap (5.4GB)")
    ax3.set_xticks(xx)
    ax3.set_xticklabels(tiers, fontsize=9.5)
    ax3.set_ylim(0, 6.8)
    ax3.legend(loc="upper left", fontsize=8)

    # 4. Workload Allocation
    set_clean_style(ax4, title="D) กลยุทธ์สถาปัตยกรรม Dual-Model Allocation")
    ax4.axis("off")
    table_data = [
        ["ภาระงาน (Workload)", "โมเดลที่เลือก", "ความเร็ว / ทรัพยากร", "เหตุผลทางสถาปัตยกรรม"],
        ["LINE Chatbot\n(Real-time RAG)", "Qwen2.5:3b\n(Sweet Spot)", "• 63.2 tok/s (< 2 วิ)\n• ใช้ VRAM 2.1 GB", "ไม่ติด Timeout 3 วินาทีของ LINE\nโหลดบน GPU 100% ไร้ Swapping"],
        ["Knowledge Graph\n(Deep Extraction)", "Qwen2.5:7b\n(Semantic Scale)", "• 22-26 tok/s\n• ใช้ VRAM 4.7 GB", "สกัดกฎหมายซับซ้อนครบทั้ง 47 หน้า\nแบ่ง 19 Slices สกัดแม่นยำ 100%"]
    ]
    tab = ax4.table(cellText=table_data, loc="center", cellLoc="left", colWidths=[0.24, 0.24, 0.24, 0.32])
    tab.auto_set_font_size(False)
    tab.set_fontsize(8.5)
    tab.scale(1, 2.3)
    for (r, c), cell in tab.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        if r == 0:
            cell.set_facecolor("#1E293B")
            cell.get_text().set_color("#FFFFFF")
            cell.get_text().set_fontweight("bold")
        elif r == 1:
            cell.set_facecolor("#ECFDF5")
        else:
            cell.set_facecolor("#F8FAFC")

    plt.suptitle("Sabai-Rules: Executive Model Benchmark & Hardware Profiling Dashboard",
                 fontsize=15, fontweight="bold", color=SLATE_DARK, y=0.98)
    out_path = FIGURES_DIR / "benchmark_executive_dashboard.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 7: RAG Quantitative Metrics (from eval_results.csv / report)
# =====================================================================
def plot_rag_evaluation_metrics():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300, facecolor=BG_LIGHT)
    set_clean_style(
        ax,
        title="ผลการประเมินประสิทธิภาพ RAG เชิงปริมาณ (Evaluation Metrics: 25 Test Queries)",
        xlabel="ตัวชี้วัด (Evaluation Metric)",
        ylabel="คะแนนเฉลี่ย (Normalized Score: 0.0 - 1.0)",
    )

    metrics = [
        "SBERT Cosine\nSimilarity",
        "Faithfulness\n(Zero Hallucination)",
        "Answer\nRelevance",
        "BERTScore\nRecall",
        "BERTScore\nF1-Score",
        "Citation\nAccuracy"
    ]
    scores = [0.8237, 0.7177, 0.7364, 0.5685, 0.4428, 0.6000]
    benchmarks = [0.80, 0.85, 0.80, 0.70, 0.70, 0.90]

    x = np.arange(len(metrics))
    width = 0.45

    bars = ax.bar(x, scores, width, color=["#10B981", "#3B82F6", "#06B6D4", "#8B5CF6", "#F59E0B", "#6366F1"], zorder=3)

    for i, bar in enumerate(bars):
        h = bar.get_height()
        ax.annotate(f"{h:.3f}" if h < 1 else f"{h*100:.0f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color="#1E293B")

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9.5)
    ax.set_ylim(0, 1.05)

    # Reference benchmark guideline
    ax.axhline(0.80, color="#10B981", linestyle=":", label="Production Good Threshold (≥ 0.80)", zorder=2)
    ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1")

    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_rag_evaluation_metrics.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 8: Retrieval Strategy Ablation Study
# =====================================================================
def plot_retrieval_ablation():
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300, facecolor=BG_LIGHT)
    set_clean_style(
        ax,
        title="การทดสอบเปรียบเทียบกลยุทธ์การค้นหา (Retrieval Ablation Study)",
        xlabel="สถาปัตยกรรม Retrieval",
        ylabel="อัตราค้นพบบริบทหน้าเอกสารตรงเป้า (Top-3 Hit Rate %)",
    )

    strategies = [
        "Dense Only\n(FAISS BGE-M3)",
        "Sparse Only\n(BM25 Thai Tokenized)",
        "Hybrid Search (RRF)\n(FAISS + BM25 + Reciprocal Rank Fusion) [Win]"
    ]
    hit_rates = [68.0, 68.0, 100.0]
    colors = [SLATE_GRAY, AMBER, PRIMARY_GREEN]

    bars = ax.bar(strategies, hit_rates, width=0.48, color=colors, zorder=3)
    bars[2].set_edgecolor("#065F46")
    bars[2].set_linewidth(2)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                     fontsize=11, fontweight="bold", color="#1E293B")

    ax.annotate(
        "Hybrid Search ผสานพลังความหมาย (Semantic)\nเข้ากับคำค้นกฎหมายเฉพาะ (Lexical) ค้นพบบริบท 100%",
        xy=(2, 85), xytext=(0.4, 85),
        arrowprops=dict(facecolor=PRIMARY_GREEN, shrink=0.08, width=1.5, headwidth=6),
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor=PRIMARY_GREEN, linewidth=1.2),
        fontsize=9, color="#065F46", fontweight="bold"
    )

    ax.set_ylim(0, 115)
    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_rag_retrieval_ablation.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 9: BERT & Embedding Models Hit Rates (Top-1 vs Top-3)
# =====================================================================
def plot_bert_embedding_hit_rates():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300, facecolor=BG_LIGHT)
    set_clean_style(
        ax,
        title="เปรียบเทียบอัตราการค้นพบเอกสาร (Hit Rate) ของโมเดลตระกูล BERT และ Embedding",
        xlabel="โมเดล Embedding / สถาปัตยกรรม",
        ylabel="อัตราค้นพบบริบทถูกต้อง (Hit Rate %)",
    )

    models = [
        "BGE-M3 (Selected)\n[XLM-RoBERTa / BERT SOTA]",
        "TF-IDF (Baseline)\n[Sparse Character N-grams]",
        "Nomic-Embed-Text\n[BERT-based / 768d]",
        "All-MiniLM\n[MiniLM / BERT 384d]"
    ]
    top1 = [50.0, 30.0, 10.0, 10.0]
    top3 = [60.0, 60.0, 10.0, 10.0]

    x = np.arange(len(models))
    width = 0.35

    b1 = ax.bar(x - width/2, top1, width, label="Top-1 Hit Rate (ดึงถูกตั้งแต่อันดับแรก)", color="#10B981", zorder=3)
    b2 = ax.bar(x + width/2, top3, width, label="Top-3 Hit Rate (ติด 3 อันดับแรก)", color="#3B82F6", zorder=3)

    # Highlight winner
    b1[0].set_edgecolor("#065F46")
    b1[0].set_linewidth(2)
    b2[0].set_edgecolor("#1E40AF")
    b2[0].set_linewidth(2)

    for bar in b1:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                     fontsize=9.5, fontweight="bold", color="#065F46")

    for bar in b2:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                     fontsize=9.5, fontweight="bold", color="#1E40AF")

    ax.annotate(
        "[อันดับ 1]: BGE-M3 (BERT SOTA) ดึงถูกตั้งแต่อันดับ 1 สูงถึง 50.0%\nเข้าใจคำพ้องภาษาไทย เช่น 'ท้อง/ลาคลอด' -> 'การลาเพื่อคลอดบุตร'",
        xy=(0, 50), xytext=(0.4, 72),
        arrowprops=dict(facecolor=PRIMARY_GREEN, shrink=0.08, width=1.5, headwidth=6),
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor=PRIMARY_GREEN, linewidth=1.2),
        fontsize=9, color="#065F46", fontweight="bold"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=9.5)
    ax.set_ylim(0, 95)
    ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1")

    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_bert_embedding_hit_rates.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 10: MRR Ranking Quality (Mean Reciprocal Rank)
# =====================================================================
def plot_bert_mrr_ranking():
    fig, ax = plt.subplots(figsize=(9.5, 5.2), dpi=300, facecolor=BG_LIGHT)
    set_clean_style(
        ax,
        title="คุณภาพการจัดอันดับผลลัพธ์เฉลี่ย (Mean Reciprocal Rank: MRR)",
        xlabel="โมเดล Embedding",
        ylabel="คะแนน MRR (1/Rank เฉลี่ย: ยิ่งสูงยิ่งติดอันดับต้น)",
    )

    models = [
        "BGE-M3 (Winner)\n[XLM-RoBERTa / 1024d]",
        "TF-IDF (Baseline)\n[Sparse N-grams]",
        "All-MiniLM\n[MiniLM / 384d]",
        "Nomic-Embed-Text\n[Nomic / 768d]"
    ]
    mrr_scores = [0.6083, 0.4733, 0.1200, 0.1200]
    colors = [PRIMARY_GREEN, AMBER, SLATE_GRAY, SLATE_GRAY]

    bars = ax.bar(models, mrr_scores, width=0.48, color=colors, zorder=3)
    bars[0].set_edgecolor("#065F46")
    bars[0].set_linewidth(2)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.4f}", xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                     fontsize=10.5, fontweight="bold", color="#1E293B")

    ax.annotate(
        "BGE-M3 ได้ MRR สูงถึง 0.6083 เหนือกว่า TF-IDF 28.5%\nและทิ้งห่างโมเดลอังกฤษล้วนอย่างเห็นได้ชัด",
        xy=(0, 0.6083), xytext=(0.5, 0.66),
        arrowprops=dict(facecolor=PRIMARY_GREEN, shrink=0.08, width=1.5, headwidth=6),
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor=PRIMARY_GREEN, linewidth=1.2),
        fontsize=9, color="#065F46", fontweight="bold"
    )

    ax.set_ylim(0, 0.85)
    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_bert_mrr_ranking.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 11: BERT Semantic Resolution: Real Case Studies
# =====================================================================
def plot_bert_case_studies():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300, facecolor=BG_LIGHT)

    # Case 1: Paraphrased Query
    set_clean_style(ax1, title="กรณีศึกษา 1: คำถามภาษาพูด / คำพ้องความหมาย\n'ท้อง ลาคลอดได้กี่วัน ได้รับค่าจ้างไหม'",
                    ylabel="อันดับที่พบ (Rank: อันดับ 1 คือดีที่สุด)")
    models_c1 = ["BGE-M3 (BERT)", "TF-IDF (Baseline)"]
    ranks_c1 = [1, 2]  # Rank 1 vs Rank 2
    colors_c1 = [PRIMARY_GREEN, CORAL]
    b_c1 = ax1.bar(models_c1, ranks_c1, width=0.42, color=colors_c1, zorder=3)
    ax1.set_ylim(0, 3.5)
    ax1.invert_yaxis()  # Invert so rank 1 is on top
    ax1.set_yticks([1, 2, 3])
    ax1.set_yticklabels(["อันดับ 1 (ถูกต้อง)", "อันดับ 2", "อันดับ 3"])

    ax1.text(0, 1.25, "ดึงหน้า 15 (การลาคลอด 98 วัน)\nScore: 0.7196 [ถูกต้อง 100%]",
             ha="center", fontsize=9, fontweight="bold", color="#065F46",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ECFDF5", edgecolor=PRIMARY_GREEN))
    ax1.text(1, 2.25, "ดึงหน้า 22 (ค่าทำงานวันหยุด)\nเพราะติดคำว่า 'จ้าง' กับ 'วัน' [พลาด]",
             ha="center", fontsize=9, fontweight="bold", color="#991B1B",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF2F2", edgecolor=CORAL))

    # Case 2: Table of Contents Noise
    set_clean_style(ax2, title="กรณีศึกษา 2: การตัดขยะหน้าสารบัญ (TOC Noise)\n'การจ่ายเงินชดเชยการเลิกจ้าง'",
                    ylabel="ความเกี่ยวข้องของเนื้อหาที่ดึงได้ (Content Relevance)")
    models_c2 = ["BGE-M3 (BERT)", "TF-IDF (Baseline)"]
    quality_c2 = [100, 25]  # Percentage content usefulness
    colors_c2 = [PRIMARY_GREEN, AMBER]
    b_c2 = ax2.bar(models_c2, quality_c2, width=0.42, color=colors_c2, zorder=3)
    ax2.set_ylim(0, 120)

    ax2.annotate("100% เนื้อหากฎหมายจริง", xy=(0, 100), xytext=(0, 104), ha="center",
                 fontsize=10, fontweight="bold", color="#065F46")
    ax2.annotate("25% ขยะสารบัญ", xy=(1, 25), xytext=(1, 29), ha="center",
                 fontsize=10, fontweight="bold", color="#92400E")

    ax2.text(0, 50, "ดึงหน้า 35 (หมวด 10)\nตารางอัตราจ่ายชดเชยตามอายุงาน\nให้ข้อมูลพร้อมตอบทันที",
             ha="center", fontsize=8.5, color="#065F46",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ECFDF5", edgecolor=PRIMARY_GREEN))
    ax2.text(1, 65, "ดึงหน้า 3 (สารบัญระเบียบ)\nมีแต่หัวข้อ ไม่มีตารางกฎหมาย\nทำให้ LLM ไม่มีข้อมูลตอบ",
             ha="center", fontsize=8.5, color="#92400E",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFBEB", edgecolor=AMBER))

    plt.suptitle("การแก้ปัญหาเฉพาะหน้าด้วย BERT Semantic Representation (BGE-M3 vs TF-IDF)",
                 fontsize=13, fontweight="bold", color=SLATE_DARK, y=0.99)
    plt.tight_layout()
    out_path = FIGURES_DIR / "benchmark_bert_case_studies.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


# =====================================================================
# Chart 12: Executive BERT / Embedding Benchmark Dashboard
# =====================================================================
def plot_bert_executive_dashboard():
    fig = plt.figure(figsize=(16, 10), dpi=300, facecolor=BG_LIGHT)
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.24)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    models = ["BGE-M3 [Win]", "TF-IDF", "Nomic", "All-MiniLM"]

    # 1. Hit Rates
    set_clean_style(ax1, title="A) อัตราค้นพบบริบทถูกต้อง (Top-1 & Top-3 Hit Rate)", ylabel="Hit Rate (%)")
    x = np.arange(len(models))
    w = 0.35
    ax1.bar(x - w/2, [50, 30, 10, 10], w, label="Top-1 Hit Rate", color="#10B981")
    ax1.bar(x + w/2, [60, 60, 10, 10], w, label="Top-3 Hit Rate", color="#3B82F6")
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=9.5)
    ax1.set_ylim(0, 85)
    ax1.legend(loc="upper right", fontsize=8.5)

    # 2. MRR Scores
    set_clean_style(ax2, title="B) คุณภาพการจัดอันดับ (Mean Reciprocal Rank)", ylabel="MRR Score (1.0 = ดีที่สุด)")
    b_mrr = ax2.bar(models, [0.6083, 0.4733, 0.1200, 0.1200], color=[PRIMARY_GREEN, AMBER, SLATE_GRAY, SLATE_GRAY], width=0.45)
    for b in b_mrr:
        h = b.get_height()
        ax2.annotate(f"{h:.4f}", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 2),
                     textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")
    ax2.set_ylim(0, 0.75)

    # 3. Vector Dimension vs Model Size
    set_clean_style(ax3, title="C) ขนาดมิติเวกเตอร์ (Vector Dimensions)", ylabel="Dimensions")
    b_dims = ax3.bar(["BGE-M3 (BERT)", "Nomic", "All-MiniLM"], [1024, 768, 384],
                     color=["#10B981", "#64748B", "#94A3B8"], width=0.45)
    for b in b_dims:
        h = b.get_height()
        ax3.annotate(f"{int(h)} dims", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 2),
                     textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")
    ax3.set_ylim(0, 1250)

    # 4. Summary Table of Decisions
    set_clean_style(ax4, title="D) สรุปเหตุผลการเลือกสถาปัตยกรรม BGE-M3 (BERT-based)")
    ax4.axis("off")
    table_data = [
        ["คุณสมบัติหลัก", "BGE-M3 (XLM-RoBERTa)", "TF-IDF Baseline", "MiniLM / Nomic"],
        ["Thai Tokenization", "สมบูรณ์แบบ (100+ ภาษา)", "อิงตัวอักษร 3-5 กรัม", "ไม่รองรับภาษาไทย"],
        ["ความเข้าใจความหมาย", "เข้าใจคำพ้อง / ภาษาพูด", "ตรงตามตัวอักษรเท่านั้น", "สับสนบริบทภาษาไทย"],
        ["การตัดขยะสารบัญ", "คัดแยกสารบัญออกได้ 100%", "ติดหน้าสารบัญเป็นอันดับ 1", "ค้นหาผิดพลาดสูง"],
        ["ความเข้ากันได้ FAISS", "IndexFlatIP (<0.1 ms)", "Sparse Scikit-learn", "FAISS รองรับ"]
    ]
    tab = ax4.table(cellText=table_data, loc="center", cellLoc="left", colWidths=[0.24, 0.28, 0.24, 0.24])
    tab.auto_set_font_size(False)
    tab.set_fontsize(8.5)
    tab.scale(1, 2.1)
    for (r, c), cell in tab.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        if r == 0:
            cell.set_facecolor("#1E293B")
            cell.get_text().set_color("#FFFFFF")
            cell.get_text().set_fontweight("bold")
        elif c == 1:
            cell.set_facecolor("#ECFDF5")
        else:
            cell.set_facecolor("#F8FAFC")

    plt.suptitle("Sabai-Rules: BERT / Embedding Model Benchmark Executive Dashboard",
                 fontsize=14, fontweight="bold", color=SLATE_DARK, y=0.98)
    out_path = FIGURES_DIR / "benchmark_bert_executive_dashboard.png"
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved: {out_path}")


def main():
    print("Generating all benchmark visual figures...")
    # LLM & Hardware Benchmarks
    plot_extraction_capacity()
    plot_speed_and_latency()
    plot_quality_vs_speed()
    plot_vram_budget()
    plot_radar_comparison()
    plot_executive_dashboard()

    # RAG Evaluation Benchmarks
    plot_rag_evaluation_metrics()
    plot_retrieval_ablation()

    # BERT & Embedding Benchmarks
    plot_bert_embedding_hit_rates()
    plot_bert_mrr_ranking()
    plot_bert_case_studies()
    plot_bert_executive_dashboard()
    print(f"All figures generated successfully in: {FIGURES_DIR}")


if __name__ == "__main__":
    main()

