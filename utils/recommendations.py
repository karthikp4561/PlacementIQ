from typing import Dict, List, Any

def generate_recommendations(
    inputs: Dict[str, float],
    prediction_result: str,
    placement_probability: float
) -> List[Dict[str, Any]]:
    """
    Generates personalized, actionable improvement suggestions based on student inputs
    and academic analytical rules.
    """
    recommendations: List[Dict[str, Any]] = []

    study_hours = inputs.get("study_hours", 0.0)
    attendance = inputs.get("attendance", 0.0)
    sleep_hours = inputs.get("sleep_hours", 0.0)
    internet_usage = inputs.get("internet_usage", 0.0)
    assignments = inputs.get("assignments_completed", 0.0)
    previous_score = inputs.get("previous_score", 0.0)
    exam_score = inputs.get("exam_score", 0.0)

    # 1. Exam Score Assessment (Major placement determinant in ML model)
    if exam_score < 75.0:
        recommendations.append({
            "category": "Academic Core",
            "priority": "High" if exam_score < 65 else "Medium",
            "title": "Intensive Exam & Technical Preparation",
            "current": f"{exam_score:.1f}%",
            "target": ">= 80.0%",
            "advice": (
                "Examination scores are the single largest statistical determinant for placement in this model. "
                "Schedule structured revision on core MCA and technical subjects (Data Structures, Algorithms, "
                "DBMS, Full-Stack Concepts) and practice timed mock assessments weekly."
            )
        })

    # 2. Attendance Compliance & Engagement
    if attendance < 75.0:
        recommendations.append({
            "category": "Attendance & Engagement",
            "priority": "High",
            "title": "Mandatory Attendance Regularization",
            "current": f"{attendance:.0f}%",
            "target": ">= 85.0%",
            "advice": (
                f"Current attendance ({attendance:.0f}%) is below the typical institutional 75% eligibility cutoff. "
                "Consistent classroom and lab participation directly correlates with stronger theoretical understanding "
                "and company recruitment eligibility."
            )
        })
    elif attendance < 85.0:
        recommendations.append({
            "category": "Attendance & Engagement",
            "priority": "Medium",
            "title": "Elevate Class & Seminar Attendance",
            "current": f"{attendance:.0f}%",
            "target": ">= 90.0%",
            "advice": (
                "Attending elective lectures, guest seminars, and training drives expands exposure to interview scenarios."
            )
        })

    # 3. Practical Assignments & Project Work
    if assignments < 10:
        recommendations.append({
            "category": "Practical Assignments",
            "priority": "High",
            "title": "Accelerate Assignment & Project Submissions",
            "current": f"{assignments:.0f} completed",
            "target": ">= 12 assignments",
            "advice": (
                "Completing practical programming assignments builds demonstrable GitHub portfolio artifacts, "
                "which are heavily probed during technical placement interviews."
            )
        })

    # 4. Study Hours & Routine
    if study_hours < 5.0:
        recommendations.append({
            "category": "Self-Study Routine",
            "priority": "Medium",
            "title": "Structured Daily Study Time",
            "current": f"{study_hours:.1f} hrs/day",
            "target": ">= 6.0 hrs/day",
            "advice": (
                "Establish a consistent 2-to-3 hour daily focused study block outside of regular lecture hours. "
                "Focus on competitive programming problems, system design basics, and aptitude tests."
            )
        })

    # 5. Previous Academic Foundations
    if previous_score < 65.0:
        recommendations.append({
            "category": "Foundational Concepts",
            "priority": "Medium",
            "title": "Bridge Remedial Subject Gaps",
            "current": f"{previous_score:.0f}%",
            "target": ">= 75.0%",
            "advice": (
                "Review foundational prerequisite topics where prior grades dipped. Companies frequently evaluate "
                "consistent semester-over-semester academic trajectory."
            )
        })

    # 6. Digital Balance & Screen Time
    if internet_usage > 7.0 and study_hours < internet_usage:
        recommendations.append({
            "category": "Digital Wellness",
            "priority": "Low",
            "title": "Channel Internet Time toward Targeted Upskilling",
            "current": f"{internet_usage:.1f} hrs/day",
            "target": "< 5.0 hrs non-academic",
            "advice": (
                "The ML model shows an inverse association with excessive unmonitored internet usage. "
                "Rechannel recreational browsing toward LeetCode, GitHub open-source PRs, and technical documentation."
            )
        })

    # 7. Sleep & Cognitive Rest
    if sleep_hours < 6.0:
        recommendations.append({
            "category": "Cognitive Performance",
            "priority": "Low",
            "title": "Restore Adequate Sleep Cycle",
            "current": f"{sleep_hours:.1f} hrs/night",
            "target": "7.0 - 8.0 hrs/night",
            "advice": (
                "Cognitive retention and problem-solving agility in placement tests depend heavily on regular sleep patterns."
            )
        })

    # If already performing exceptionally well:
    if not recommendations:
        recommendations.append({
            "category": "Excellence & Leadership",
            "priority": "Maintenance",
            "title": "Advanced Competitive Preparation & Mentorship",
            "current": "Optimal profile across all tracked metrics",
            "target": "Maintain current high trajectory",
            "advice": (
                "Your performance indicators are well above benchmark cohorts. Focus on mock HR interviews, "
                "soft-skills articulation, system architecture, and mentoring peer study groups."
            )
        })

    return recommendations

def compute_target_profile(inputs: Dict[str, float]) -> Dict[str, Any]:
    """
    Computes an optimal target profile calibrated to achieve >= 85% placement probability,
    and calculates metric-by-metric gaps for graphical representation.
    """
    current_study = float(inputs.get("study_hours", 0.0))
    current_att = float(inputs.get("attendance", 0.0))
    current_sleep = float(inputs.get("sleep_hours", 0.0))
    current_net = float(inputs.get("internet_usage", 0.0))
    current_assign = float(inputs.get("assignments_completed", 0.0))
    current_prev = float(inputs.get("previous_score", 0.0))
    current_exam = float(inputs.get("exam_score", 0.0))

    # Recommended target parameters calibrated for model probability >= 85%
    target_study = max(current_study, 6.0)
    target_att = max(current_att, 82.0)
    target_sleep = 7.0 if current_sleep < 6.0 else (current_sleep if current_sleep <= 8.5 else 7.5)
    target_net = min(current_net, 4.5)
    target_assign = max(current_assign, 12.0)
    target_prev = current_prev  # Historical; remains baseline
    target_exam = max(current_exam, 82.5)

    target_inputs = {
        "study_hours": target_study,
        "attendance": target_att,
        "sleep_hours": target_sleep,
        "internet_usage": target_net,
        "assignments_completed": target_assign,
        "previous_score": target_prev,
        "exam_score": target_exam
    }

    gaps = [
        {
            "feature": "exam_score",
            "label": "Examination Score",
            "current": current_exam,
            "target": target_exam,
            "delta": round(target_exam - current_exam, 1),
            "unit": "%",
            "priority": "Critical" if (target_exam - current_exam) > 5 else "Satisfied",
            "action": f"Elevate by +{target_exam - current_exam:.1f}% through mock tests & technical revision" if target_exam > current_exam else "Maintain performance"
        },
        {
            "feature": "attendance",
            "label": "College Attendance",
            "current": current_att,
            "target": target_att,
            "delta": round(target_att - current_att, 1),
            "unit": "%",
            "priority": "High" if (target_att - current_att) > 5 else "Satisfied",
            "action": f"Regularize class presence by +{target_att - current_att:.0f}%" if target_att > current_att else "Attendance on track"
        },
        {
            "feature": "assignments_completed",
            "label": "Assignments & Projects",
            "current": current_assign,
            "target": target_assign,
            "delta": round(target_assign - current_assign, 0),
            "unit": " completed",
            "priority": "High" if (target_assign - current_assign) > 0 else "Satisfied",
            "action": f"Submit +{target_assign - current_assign:.0f} additional coding assignments" if target_assign > current_assign else "Assignment quota fulfilled"
        },
        {
            "feature": "study_hours",
            "label": "Daily Study Hours",
            "current": current_study,
            "target": target_study,
            "delta": round(target_study - current_study, 1),
            "unit": " hrs/day",
            "priority": "Medium" if (target_study - current_study) > 0 else "Satisfied",
            "action": f"Increase focused preparation by +{target_study - current_study:.1f} hrs/day" if target_study > current_study else "Study volume sufficient"
        },
        {
            "feature": "internet_usage",
            "label": "Recreational Internet Usage",
            "current": current_net,
            "target": target_net,
            "delta": round(target_net - current_net, 1),
            "unit": " hrs/day",
            "priority": "Medium" if (current_net - target_net) > 1.5 else "Satisfied",
            "action": f"Re-channel {current_net - target_net:.1f} hrs of non-academic browsing to coding" if current_net > target_net else "Balanced digital footprint"
        },
        {
            "feature": "sleep_hours",
            "label": "Restorative Sleep",
            "current": current_sleep,
            "target": target_sleep,
            "delta": round(target_sleep - current_sleep, 1),
            "unit": " hrs/night",
            "priority": "Low",
            "action": "Ensure 7 hours nightly sleep for cognitive acuity"
        }
    ]

    return {
        "target_inputs": target_inputs,
        "gaps": gaps
    }
