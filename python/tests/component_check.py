
from appbuilder.tests.base_rules import register_component_check_rule
from appbuilder.tests.base_rules import ManifestValidRule, MainfestMatchToolEvalRule, ToolEvalInputNameRule, ToolEvalOutputJsonRule
from component_tool_eval_cases import component_tool_eval_cases


register_component_check_rule("ManifestValidRule", ManifestValidRule, {})
register_component_check_rule("MainfestMatchToolEvalRule", MainfestMatchToolEvalRule, {})
register_component_check_rule("ToolEvalInputNameRule", ToolEvalInputNameRule, {})
register_component_check_rule("ToolEvalOutputJsonRule", ToolEvalOutputJsonRule, \
    {"component_tool_eval_cases": component_tool_eval_cases})