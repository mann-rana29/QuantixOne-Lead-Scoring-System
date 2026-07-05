from app.models.scoring_rule import Condition, ConditionOperator, ScoringRuleResponse, ScoreType
from app.db.connect import get_collection
from app.models.score_threshold import BucketName
from bson import ObjectId
from datetime import datetime
from app.util import convert_to_scoring_rule

def matches_condition(condition : Condition | None, payload : dict) -> bool:
    if condition is None:
        return True
    
    actual_value = payload.get(condition.field)
    if actual_value is None:
        return False
    
    if condition.operator == ConditionOperator.equals:
        return actual_value == condition.value
    elif condition.operator == ConditionOperator.not_equals:
        return actual_value != condition.value
    elif condition.operator == ConditionOperator.contains:
        return condition.value in actual_value
    elif condition.operator == ConditionOperator.greater_than:
        return actual_value > condition.value
    elif condition.operator == ConditionOperator.less_than:
        return actual_value < condition.value
    
    return False

def get_score_delta(rule : ScoringRuleResponse) -> tuple[str,int]:
    if rule.score_type == ScoreType.fit:
        return ("fit_score", rule.points)
    elif rule.score_type == ScoreType.engagement:
        return ("engagement_score", rule.points)
    elif rule.score_type == ScoreType.negative:
        return ("negative_score", rule.points)
    elif rule.score_type == ScoreType.decay:
        return ("negative_score", rule.points)
    
async def get_or_create_lead_score(workspace_id : str, lead_id : str) -> dict:
    collection = await get_collection("lead_scores")
    
    lead_score_doc = await collection.find_one(
        {
            "lead_id" : lead_id,
            "workspace_id" : workspace_id
        }
    )

    if lead_score_doc is None:
        new_lead_score = {
            "fit_score" : 0,
            "engagement_score" : 0,
            "negative_score" : 0,
            "total_score" : 0
        }

        return new_lead_score

    return lead_score_doc

def apply_delta(current_scores : dict, field : str, delta : int) -> dict:
    current_scores[field] = current_scores.get(field,0) + delta

    current_scores["total_score"] = (current_scores.get("fit_score",0) + current_scores.get("engagement_score",0) - current_scores.get("negative_score",0))

    return current_scores

async def get_bucket_for_score(workspace_id : str, total_score : int) -> str:
    collection = await get_collection("score_thresholds")

    score_threshold_doc = await collection.find_one(
        {
            "workspace_id" : workspace_id,
            "from_score" : {"$lte" : total_score},
            "to_score" : {"$gte" : total_score}
        }
    )

    if score_threshold_doc is None:
        return BucketName.cold
    
    return score_threshold_doc.get("bucket_name", BucketName.cold)

async def evaluate_signal(signal_id: str):
    # 1. Fetch the signal
    lead_signal_collection = await get_collection("lead_signals")
    lead_signal_doc = await lead_signal_collection.find_one({"_id": ObjectId(signal_id)})
    if lead_signal_doc is None:
        return

    workspace_id = lead_signal_doc["workspace_id"]
    lead_id = lead_signal_doc["lead_id"]

    # 2. Fetch matching active rules
    scoring_rules_collection = await get_collection("scoring_rules")
    cursor = scoring_rules_collection.find({
        "workspace_id": workspace_id,
        "source_module": lead_signal_doc["source"],
        "trigger_event": lead_signal_doc["event_type"],
        "status": "active",
    })
    raw_rules = [rule async for rule in cursor]

    # 3. Get current lead score state (starting point)
    lead_score = await get_or_create_lead_score(workspace_id, lead_id)
    
    old_bucket = await get_bucket_for_score(workspace_id,lead_score["total_score"])

    fired_rules = []  # track (rule_obj, field, delta, old_total) for history entries


    # 4. Evaluate each rule
    for raw_rule in raw_rules:
        rule_obj = convert_to_scoring_rule(raw_rule)

        if matches_condition(rule_obj.condition, lead_signal_doc["payload"]):
            old_total = lead_score.get("total_score", 0)
            field, delta = get_score_delta(rule_obj)
            lead_score = apply_delta(lead_score, field, delta)
            fired_rules.append((rule_obj, field, delta, old_total))

    # 5. Determine final bucket based on new total_score
    new_bucket = await get_bucket_for_score(workspace_id, lead_score.get("total_score", 0))

    # 6. Upsert lead_scores
    lead_score["workspace_id"] = workspace_id
    lead_score["lead_id"] = lead_id
    lead_score["bucket"] = new_bucket
    lead_score["updated_at"] = datetime.utcnow()

    lead_score_collection = await get_collection("lead_scores")
    await lead_score_collection.update_one(
        {"lead_id": lead_id, "workspace_id": workspace_id},
        {"$set": lead_score},
        upsert=True,
    )

    # 7. Write score_history entries, one per rule that fired
    if fired_rules:
        score_history_collection = await get_collection("score_history")
        history_entries = []
        for rule_obj, field, delta, old_total in fired_rules:
            history_entries.append({
                "workspace_id": workspace_id,
                "lead_id": lead_id,
                "signal_id": signal_id,
                "rule_id": rule_obj.id,
                "old_score": old_total,
                "score_change": delta,
                "new_score": lead_score["total_score"],
                "old_bucket": old_bucket,
                "new_bucket": new_bucket,
                "created_at": datetime.utcnow(),
            })
        await score_history_collection.insert_many(history_entries)

    # 8. Mark the signal processed
    await lead_signal_collection.update_one(
        {"_id": ObjectId(signal_id)},
        {"$set": {"status": "processed", "processed_at": datetime.utcnow()}}
    )