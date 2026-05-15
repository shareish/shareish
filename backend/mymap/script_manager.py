from .scripts_parser import parser_conso_ecosociale, parser_liegeentransition, parser_murmurations, parser_tierslieux

SCRIPTS = {
    'liege_transition': parser_liegeentransition.main,
    'conso_ecosociale': parser_conso_ecosociale.main,
    'murmurations': parser_murmurations.main,
    'tiers_lieux': parser_tierslieux.main
}

def run_script(script_name):
    print("run script")
    script_run = SCRIPTS.get(script_name)
    if script_run:
        return script_run()
    return None