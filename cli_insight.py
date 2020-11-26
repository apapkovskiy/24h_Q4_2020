import time
import click
import json

from be import InsightBE, AssetType

client = InsightBE()


@click.group()
def cli():
  pass


@click.command(help='Udate Mark FW')
@click.option('--gw', required=True, type=(str), help='Gateway ID')
@click.option('--version', required=True, type=(str), help='FW version')
def mark(gw, version):
    url = client.get_url(AssetType.MARK_FIRMWARE, version)
    resp = client.update_mark_be(gw, url)
    resp = json.loads(resp)
    print(json.dumps(resp, indent=4))


@click.command(help='Udate Gateway FW')
@click.option('--gw', required=True, type=(str), help='Gateway ID')
@click.option('--version', required=True, type=(str), help='FW version')
def gw(gw, version):
    url = client.get_url(AssetType.GATEWAY1_APPLICATION, version)
    resp = client.update_gw_be(gw, url)
    resp = json.loads(resp)
    print(json.dumps(resp, indent=4))


@click.command(help='Udate Gateway configuration')
@click.option('--gw', required=True, type=(str), help='Gateway ID')
@click.option('--name', required=True, type=(str), help='FW version')
def conf(gw, name):
    url = client.get_url(AssetType.GATEWAY1_APPLICATION, name)
    resp = client.update_gw_config(gw, url)
    resp = json.loads(resp)
    print(json.dumps(resp, indent=4))


@click.command(help='Get info about a Gateway')
@click.option('--gw', required=True, type=(str), help='Gateway ID')
def info(gw):
    info = client.get_gateway_info(gw)
    print(json.dumps(info, indent=4))

if __name__ == '__main__':
    cli.add_command(mark)
    cli.add_command(gw)
    cli.add_command(info)
    cli.add_command(conf)
    cli()
