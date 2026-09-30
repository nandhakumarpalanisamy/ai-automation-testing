import json
import datetime
from pathlib import Path
from src.config import Config

REPORTS_DIR = Path(__file__).parent.parent / "reports"

def generate_reports(test_results: list, duration_seconds: float):
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # Calculate stats
    total = len(test_results)
    passed = len([t for t in test_results if t["status"] == "Passed"])
    ai_failed = len([t for t in test_results if t["status"] == "AI_Quality_Failure"])
    api_failed = len([t for t in test_results if t["status"] == "API_Failure"])
    
    pass_pct = (passed / total * 100) if total > 0 else 0
    
    categories = {}
    for t in test_results:
        cat = t.get("category", "Unknown")
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0, "failed": 0, "errors": 0}
        categories[cat]["total"] += 1
        if t["status"] == "Passed":
            categories[cat]["passed"] += 1
        elif t["status"] == "AI_Quality_Failure":
            categories[cat]["failed"] += 1
        else:
            categories[cat]["errors"] += 1

    execution_data = {
        "execution": {
            "timestamp": datetime.datetime.now().isoformat(),
            "model_under_test": Config.MODEL_UNDER_TEST_NAME,
            "evaluator_model": Config.EVALUATOR_MODEL_NAME,
            "total_tests": total,
            "passed": passed,
            "failed": ai_failed,
            "errors": api_failed,
            "duration_seconds": round(duration_seconds, 2),
            "pass_percentage": round(pass_pct, 2)
        },
        "categories": categories,
        "tests": test_results
    }
    
    # Generate JSON
    with open(REPORTS_DIR / "ai_test_report.json", "w") as f:
        json.dump(execution_data, f, indent=2)
        
    # Generate MD
    generate_markdown(execution_data)
    
    # Generate HTML
    generate_html(execution_data)


def generate_markdown(data: dict):
    md = [
        "# AI Model Test Report",
        "",
        "## Execution Summary",
        f"- **Timestamp:** {data['execution']['timestamp']}",
        f"- **Model Under Test:** {data['execution']['model_under_test']}",
        f"- **Evaluator Model:** {data['execution']['evaluator_model']}",
        f"- **Duration:** {data['execution']['duration_seconds']}s",
        f"- **Pass Rate:** {data['execution']['pass_percentage']}%",
        "",
        f"**Total:** {data['execution']['total_tests']} | **Passed:** {data['execution']['passed']} | **AI Failed:** {data['execution']['failed']} | **API Errors:** {data['execution']['errors']}",
        "",
        "## Test Categories",
        "| Category | Total | Passed | AI Failed | API Errors |",
        "|----------|-------|--------|-----------|------------|"
    ]
    for cat, stats in data["categories"].items():
        md.append(f"| {cat} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['errors']} |")
        
    md.extend(["", "## Detailed Results"])
    
    for t in data["tests"]:
        md.append(f"### {t['test_id']} - {t['status']}")
        md.append(f"- **Category:** {t['category']}")
        md.append(f"- **Question:** {t['question']}")
        if "expected" in t:
            md.append(f"- **Expected:** {t['expected']}")
        md.append(f"- **Response:**\n```text\n{t['response']}\n```")
        
        if t["metrics"]:
            md.append("- **Metrics:**")
            for m_name, m_res in t["metrics"].items():
                pass_str = "PASS" if m_res["success"] else "FAIL"
                md.append(f"  - {m_name}: {m_res['score']} ({pass_str}) - *{m_res['reason']}*")
        
        if t["error_message"]:
            md.append(f"- **Error:** {t['error_message']}")
            
        md.append("---")
        
    with open(REPORTS_DIR / "ai_test_report.md", "w") as f:
        f.write("\n".join(md))

def generate_html(data: dict):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Model Test Report</title>
<style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; background: #f4f4f9; color: #333; }}
    h1, h2, h3 {{ color: #2c3e50; }}
    .summary-card {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; display: flex; gap: 20px; flex-wrap: wrap; }}
    .stat-box {{ background: #ecf0f1; padding: 15px; border-radius: 5px; flex: 1; min-width: 150px; text-align: center; }}
    .stat-box.passed {{ border-bottom: 4px solid #2ecc71; }}
    .stat-box.failed {{ border-bottom: 4px solid #e74c3c; }}
    .stat-box.errors {{ border-bottom: 4px solid #f39c12; }}
    .stat-number {{ font-size: 24px; font-weight: bold; margin-top: 5px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
    th {{ background-color: #34495e; color: #fff; }}
    .test-card {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #ccc; }}
    .test-card.Passed {{ border-left-color: #2ecc71; }}
    .test-card.AI_Quality_Failure {{ border-left-color: #e74c3c; }}
    .test-card.API_Failure {{ border-left-color: #f39c12; }}
    .code-block {{ background: #eee; padding: 10px; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }}
</style>
</head>
<body>
    <h1>AI Model Test Report</h1>
    
    <h2>Execution Summary</h2>
    <div class="summary-card">
        <div class="stat-box"><div>Model Under Test</div><div class="stat-number">{data['execution']['model_under_test']}</div></div>
        <div class="stat-box"><div>Evaluator Judge</div><div class="stat-number">{data['execution']['evaluator_model']}</div></div>
        <div class="stat-box"><div>Total Tests</div><div class="stat-number">{data['execution']['total_tests']}</div></div>
        <div class="stat-box passed"><div>Passed</div><div class="stat-number">{data['execution']['passed']}</div></div>
        <div class="stat-box failed"><div>AI Failed</div><div class="stat-number">{data['execution']['failed']}</div></div>
        <div class="stat-box errors"><div>API Errors</div><div class="stat-number">{data['execution']['errors']}</div></div>
        <div class="stat-box"><div>Pass Rate</div><div class="stat-number">{data['execution']['pass_percentage']}%</div></div>
        <div class="stat-box"><div>Duration</div><div class="stat-number">{data['execution']['duration_seconds']}s</div></div>
    </div>
    
    <h2>Test Categories</h2>
    <table>
        <tr><th>Category</th><th>Total</th><th>Passed</th><th>AI Failed</th><th>API Errors</th></tr>"""
        
    for cat, stats in data["categories"].items():
        html += f"<tr><td>{cat}</td><td>{stats['total']}</td><td>{stats['passed']}</td><td>{stats['failed']}</td><td>{stats['errors']}</td></tr>"
        
    html += """</table>
    <h2>Detailed Results</h2>"""
    
    for t in data["tests"]:
        html += f"""
        <div class="test-card {t['status']}">
            <h3>[{t['test_id']}] - {t['status'].replace('_', ' ')}</h3>
            <p><strong>Category:</strong> {t['category']}</p>
            <p><strong>Question:</strong> {t['question']}</p>"""
        if "expected" in t:
            html += f"<p><strong>Expected:</strong> {t['expected']}</p>"
        
        html += f"""<p><strong>Model Response:</strong></p><div class="code-block">{t['response']}</div>"""
        
        if t["error_message"]:
            html += f"<p style='color: #e74c3c;'><strong>Error:</strong> {t['error_message']}</p>"
            
        if t["metrics"]:
            html += "<h4>Evaluation Metrics:</h4><ul>"
            for m_name, m_res in t["metrics"].items():
                color = "green" if m_res["success"] else "red"
                html += f"<li><strong>{m_name}</strong>: {m_res['score']} (<span style='color: {color}; font-weight: bold;'>{'PASS' if m_res['success'] else 'FAIL'}</span>)<br><em>{m_res['reason']}</em></li>"
            html += "</ul>"
            
        html += "</div>"
        
    html += """
</body>
</html>"""

    with open(REPORTS_DIR / "ai_test_report.html", "w", encoding="utf-8") as f:
        f.write(html)
