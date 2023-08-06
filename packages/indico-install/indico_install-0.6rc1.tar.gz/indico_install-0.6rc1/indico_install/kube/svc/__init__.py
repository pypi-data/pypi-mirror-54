import click
from indico_install.kube.svc.restart import restart
from indico_install.kube.svc.update import update
from indico_install.kube.svc.scale import scale

@click.group("svc")
@click.pass_context
def svc(ctx):
    """Commands for cluster services"""
    pass


for command in [restart, update, scale]:
    svc.add_command(command)
