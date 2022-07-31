import sys
import logging

from jinja2 import Environment, FileSystemLoader

CONFIGS_AMOUNT = 250
TEMPLATE_NAME = 'nmstate.yaml'
TEMPLATE_FOLDER = 'templates'

OUTPUT_NAME = 'nmstateconfig'
OUTPUT_SUFFIX = 'yaml'
OUTPUT_FOLDER = './output'

env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
template = env.get_template(TEMPLATE_NAME)

LOG = logging.getLogger(__name__)


def configure_logger(debug_mode):
    logging.basicConfig(
        level=logging.DEBUG if debug_mode is True else logging.INFO,
        format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s'
    )


def main():
    for i in range(1, CONFIGS_AMOUNT+1):
        c_octet = i
        d_octet = CONFIGS_AMOUNT+1-i

        mac_a = f'0{c_octet}' if c_octet < 10 else c_octet
        mac_a = str(mac_a)[1:] if len(str(mac_a)) > 2 else mac_a

        mac_b = f'0{d_octet}' if d_octet < 10 else d_octet
        mac_b = str(mac_b)[1:] if len(str(mac_b)) > 2 else mac_b

        output_from_parsed_template = template.render(
            i=i,
            c_octet=c_octet,
            d_octet=d_octet,
            mac_a=mac_a,
            mac_b=mac_b,
        )
        with open(f"{OUTPUT_FOLDER}/{OUTPUT_NAME}{i}.{OUTPUT_SUFFIX}", "w") as fh:
            fh.write(output_from_parsed_template)
            LOG.debug(f"Done writing {OUTPUT_FOLDER}/{OUTPUT_NAME}{i}.{OUTPUT_SUFFIX}")

    LOG.info(f"Created {CONFIGS_AMOUNT} NMStateConfig files at {OUTPUT_FOLDER}")


if __name__ == '__main__':
    configure_logger(False)
    sys.exit(main())
