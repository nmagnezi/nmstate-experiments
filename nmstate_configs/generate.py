from jinja2 import Environment, FileSystemLoader

CONFIGS_AMOUNT = 250
TEMPLATE_NAME = 'nmstate.yaml'
TEMPLATE_FOLDER = 'templates'

OUTPUT_NAME = 'nmstateconfig'
OUTPUT_SUFFIX = 'yaml'
OUTPUT_FOLDER = './output'

env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
template = env.get_template(TEMPLATE_NAME)

for i in range(1, CONFIGS_AMOUNT+1):
    output_from_parsed_template = template.render(foo=i)
    with open(f"{OUTPUT_FOLDER}/{OUTPUT_NAME}{i}.{OUTPUT_SUFFIX}", "w") as fh:
        fh.write(output_from_parsed_template)
