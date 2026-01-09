from datetime import date
from final_api_1.services.blend_ratio import run_blend_ratio
from final_api_1.services.bias import apply_bias_and_rerank

def run_feedback_recommend(req):
    scored_items = run_blend_ratio(req)
    final_items = apply_bias_and_rerank(
        model_type="BLEND_RATIO",
        scored_items=scored_items,
    )
    return {
        "date": date.today().strftime("%Y-%m-%d"),
        "results": final_items,
    }
