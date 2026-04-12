import requests
import gradio as gr

# Point this at your running FastAPI server
API_URL = "http://localhost:8000/jobs/"


def scrape_jobs(url: str):
    if not url.strip():
        return "Please enter a URL.", None

    try:
        response = requests.post(API_URL, json={"url": url.strip()})
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return "Could not connect to the API. Make sure the FastAPI server is running on http://localhost:8000.", None
    except requests.exceptions.Timeout:
        return "Request timed out. The page may have too many listings.", None
    except requests.exceptions.HTTPError as e:
        return f"API error: {e.response.status_code} — {e.response.text}", None

    data = response.json()

    if not isinstance(data, dict):
        return (
            f"Unexpected API response (expected a JSON object). Got {type(data).__name__}.",
            None,
        )

    if data.get("status") == 400:
        return data.get("message", "No jobs found."), None

    jobs = data.get("data") or []
    if not isinstance(jobs, list):
        jobs = []

    if not jobs:
        return "No job listings found on that page.", None

    rows = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        desc = job.get("job_description") or ""
        preview = (desc[:300] + "...") if desc else "—"
        rows.append([
            job.get("job_title") or "—",
            job.get("company_name") or "—",
            preview,
            job.get("apply_url") or "—",
        ])

    if not rows:
        return "No job listings found on that page.", None

    status_msg = f"Found {len(rows)} job listing{'s' if len(rows) != 1 else ''}."
    return status_msg, rows


with gr.Blocks(
    title="Job Scraper",
    theme=gr.themes.Base(
        primary_hue="violet",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter"),
    ),
    css="""
        .gradio-container { max-width: 1100px !important; }
        #title { text-align: center; margin-bottom: 0.25rem; }
        #subtitle { text-align: center; color: #94a3b8; margin-bottom: 2rem; }
    """
) as demo:

    gr.Markdown("# 🔍 Job Scraper", elem_id="title")
    gr.Markdown("Paste a company careers page URL and extract all job listings automatically.", elem_id="subtitle")

    with gr.Row():
        url_input = gr.Textbox(
            label="Careers Page URL",
            placeholder="https://example.com/careers",
            scale=4
        )
        submit_btn = gr.Button("Scrape Jobs", variant="primary", scale=1)

    status_output = gr.Textbox(label="Status", interactive=False, lines=1)

    results_table = gr.Dataframe(
        headers=["Job Title", "Company", "Description Preview", "Apply URL"],
        datatype=["str", "str", "str", "str"],
        label="Job Listings",
        wrap=True,
        interactive=False,
    )

    submit_btn.click(
        fn=scrape_jobs,
        inputs=[url_input],
        outputs=[status_output, results_table],
    )

    url_input.submit(
        fn=scrape_jobs,
        inputs=[url_input],
        outputs=[status_output, results_table],
    )

    gr.Markdown(
        "Powered by [FastAPI](https://fastapi.tiangolo.com) & [Amazon Bedrock](https://aws.amazon.com/bedrock/)",
        elem_id="subtitle"
    )

if __name__ == "__main__":
    demo.launch()
