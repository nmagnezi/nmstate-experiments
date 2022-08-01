import os
import random
import shutil
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


def delete_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            LOG.error('Failed to delete %s. Reason: %s' % (file_path, e))


def generate_files(config_amount, folder, output_name, output_suffix):
    for i in range(1, config_amount+1):
        c_octet = random.randint(1, 254)
        d_octet = random.randint(1, 254)
        mac_a = hex(c_octet)[2:]
        mac_b = hex(d_octet)[2:]
        mac_a = f'0{mac_a}' if len(mac_a) == 1 else mac_a  # pad with 0 if needed
        mac_b = f'0{mac_b}' if len(mac_b) == 1 else mac_b  # pad with 0 if needed

        LOG.debug(f"c_octet: {c_octet} ; d_octet: {d_octet} ; mac_a: {mac_a} ; mac_b: {mac_b}")

        output_from_parsed_template = template.render(
            i=i,
            c_octet=c_octet,
            d_octet=d_octet,
            mac_a=mac_a,
            mac_b=mac_b,
        )
        with open(f"{folder}/{output_name}{i}.{output_suffix}", "w") as fh:
            fh.write(output_from_parsed_template)
            LOG.debug(f"Done writing {folder}/{output_name}{i}.{output_suffix}")


def main():
    delete_files(OUTPUT_FOLDER)
    generate_files(CONFIGS_AMOUNT, OUTPUT_FOLDER, OUTPUT_NAME, OUTPUT_SUFFIX)
    LOG.info(f"Created {CONFIGS_AMOUNT} NMStateConfig files at {OUTPUT_FOLDER}")


if __name__ == '__main__':
    configure_logger(False)
    sys.exit(main())
