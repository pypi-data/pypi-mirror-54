import argparse
import hubploy
from hubploy import helm, auth


def main():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest='command')
    build_parser = subparsers.add_parser('build', help='Build an image from given path')

    build_parser.add_argument(
        'deployment',
        help='Path to directory with dockerfile'
    )

    trigger_change_group = build_parser.add_mutually_exclusive_group()
    trigger_change_group.add_argument(
        '--commit-range',
        help='Trigger image rebuilds only if files in image directory have changed in this git commit range'
    )
    # FIXME: Needs a better name?
    trigger_change_group.add_argument(
        '--check-registry',
        action='store_true',
        help="Trigger image rebuild if image with expected name and tag is not in upstream registry."
    )
    build_parser.add_argument(
        '--push',
        action='store_true',
    )

    deploy_parser = subparsers.add_parser('deploy', help='Deploy a chart to the given environment')

    deploy_parser.add_argument(
        'deployment'
    )
    deploy_parser.add_argument(
        'chart'
    )
    deploy_parser.add_argument(
        'environment',
        choices=['develop', 'staging', 'prod']
    )
    deploy_parser.add_argument(
        '--namespace',
        default=None
    )
    deploy_parser.add_argument(
        '--set',
        action='append',
    )
    deploy_parser.add_argument(
        '--version',
    )

    args = argparser.parse_args()

    config = hubploy.config.get_config(args.deployment)

    if args.command == 'build':

        if args.push or args.check_registry:
            auth.registry_auth(args.deployment)

        for image in config.get('images', {}).get('images', {}):
            if image.needs_building(check_registry=args.check_registry, commit_range=args.commit_range):
                image.fetch_parent_image()
                image.build()
                if args.push:
                    image.push()

    elif args.command == 'deploy':
        auth.cluster_auth(args.deployment)
        helm.deploy(args.deployment, args.chart, args.environment, args.namespace, args.set, args.version)