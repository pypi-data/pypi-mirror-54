import click
from indico_install.utils import run_cmd, options_wrapper
from indico_install.config import ConfigsHolder, merge_dicts


@click.command("scale")
@click.pass_context
@click.argument("service", required=True, type=str)
@click.argument("amount", required=True, type=int)
@options_wrapper()
def scale(ctx, service, amount, *, input_yaml, yes, **kwargs):
    """
    Scale a K8S cluster deployment or statefulset

    ARGS:
        <SERVICE> grep string of deployments and statefulsets to scale

        <AMOUNT> number of pods to create
    """
    updated_svcs = []
    for svc_type in ["deployment", "statefulset"]:
        out = run_cmd(
            """kubectl get %s --no-headers | grep "%s" | awk '{print $1}'"""
            % (svc_type, service),
            silent=True,
        )
        if not out:
            continue
        for _svc in out.splitlines():
            click.secho(
                run_cmd(f"kubectl scale --replicas={amount} {svc_type} {_svc}"),
                fg="green",
            )
            updated_svcs.append(_svc)

    if updated_svcs and yes:
        if not input_yaml.is_file():
            click.secho(
                f"Could not find {input_yaml}. Unable to save new scale", fg="yellow"
            )
            return
        conf = ConfigsHolder(config=input_yaml)
        updated_svcs_dict = {
            _svc: {"values": {"replicas": amount}} for _svc in updated_svcs
        }
        conf["services"] = merge_dicts(conf.get("services", {}), updated_svcs_dict)
        conf.save()
